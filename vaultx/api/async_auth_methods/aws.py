import hmac
import json
from base64 import b64encode
from datetime import datetime, timezone
from hashlib import sha256
from typing import Optional, Union

import httpx

from vaultx import exceptions, utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase
from vaultx.constants.aws import ALLOWED_EC2_ALIAS_TYPES, ALLOWED_IAM_ALIAS_TYPES
from vaultx.constants.aws import DEFAULT_MOUNT_POINT as AWS_DEFAULT_MOUNT_POINT


class SigV4Auth:
    def __init__(
        self, access_key: str, secret_key: str, session_token: Optional[str] = None, region: str = "us-east-1"
    ) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.session_token = session_token
        self.region = region

    def add_auth(self, request: httpx.Request) -> None:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        request.headers["X-Amz-Date"] = timestamp

        if self.session_token:
            request.headers["X-Amz-Security-Token"] = self.session_token

        # https://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html
        canonical_headers = "".join(f"{k.lower()}:{request.headers[k]}\n" for k in sorted(request.headers))
        signed_headers = ";".join(k.lower() for k in sorted(request.headers))
        payload_hash = sha256(request.content).hexdigest()
        canonical_request = "\n".join([request.method, "/", "", canonical_headers, signed_headers, payload_hash])

        # https://docs.aws.amazon.com/general/latest/gr/sigv4-create-string-to-sign.html
        algorithm = "AWS4-HMAC-SHA256"
        credential_scope = "/".join([timestamp[0:8], self.region, "sts", "aws4_request"])
        canonical_request_hash = sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = "\n".join([algorithm, timestamp, credential_scope, canonical_request_hash])

        # https://docs.aws.amazon.com/general/latest/gr/sigv4-calculate-signature.html
        key = f"AWS4{self.secret_key}".encode()
        key = hmac.new(key, timestamp[0:8].encode("utf-8"), sha256).digest()
        key = hmac.new(key, self.region.encode("utf-8"), sha256).digest()
        key = hmac.new(key, b"sts", sha256).digest()
        key = hmac.new(key, b"aws4_request", sha256).digest()
        signature = hmac.new(key, string_to_sign.encode("utf-8"), sha256).hexdigest()

        # https://docs.aws.amazon.com/general/latest/gr/sigv4-add-signature-to-request.html
        authorization = "{} Credential={}/{}, SignedHeaders={}, Signature={}".format(
            algorithm, self.access_key, credential_scope, signed_headers, signature
        )
        request.headers["Authorization"] = authorization


def generate_sigv4_auth_request(header_value: Optional[str] = None) -> httpx.Request:
    """
    Helper function to prepare an AWS API request to subsequently generate an "AWS Signature Version 4" header.

    :param header_value: Vault allows you to require an additional header, X-Vault-AWS-IAM-Server-ID, to be present
        to mitigate against different types of replay attacks. Depending on the configuration of the AWS auth
        backend, providing an argument to this optional parameter may be required.
    :return: A PreparedRequest instance, optionally containing the provided header value under an
        'X-Vault-AWS-IAM-Server-ID' header name pointed to AWS's simple token service with action "GetCallerIdentity"
    """
    request = httpx.Request(
        method="POST",
        url="https://sts.amazonaws.com/",
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Host": "sts.amazonaws.com",
        },
        data={"Action": "GetCallerIdentity&Version=2011-06-15"},
    )

    if header_value:
        request.headers["X-Vault-AWS-IAM-Server-ID"] = header_value

    return request


class Aws(AsyncVaultApiBase):
    """
    AWS Auth Method (API).

    Reference: https://www.vaultproject.io/api/auth/aws/index.html
    """

    async def configure(
        self,
        max_retries: Optional[int] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        iam_endpoint: Optional[str] = None,
        sts_endpoint: Optional[str] = None,
        iam_server_id_header_value: Optional[str] = None,
        mount_point: Optional[str] = AWS_DEFAULT_MOUNT_POINT,
        sts_region: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Configure the credentials required to perform API calls to AWS as well as custom endpoints to talk to AWS API.

        The instance identity document fetched from the PKCS#7 signature will provide the EC2 instance ID.
        The credentials configured using this endpoint will be used to query the status of the instances via
        DescribeInstances API. If static credentials are not provided using this endpoint, then the credentials will be
        retrieved from the environment variables AWS_ACCESS_KEY, AWS_SECRET_KEY and AWS_REGION respectively.
        If the credentials are still not found and if the method is configured on an EC2 instance with metadata querying
        capabilities, the credentials are fetched automatically

        Supported methods:
            POST: /auth/{mount_point}/config Produces: 204 (empty body)

        :param max_retries: Number of max retries the client should use for recoverable errors.
            The default (-1) falls back to the AWS SDK's default behavior
        :param access_key: AWS Access key with permissions to query AWS APIs. The permissions required depend on the
            specific configurations. If using the iam auth method without inferencing, then no credentials are
            necessary. If using the ec2 auth method or using the iam auth method with inferencing, then these
            credentials need access to ec2:DescribeInstances. If additionally a bound_iam_role is specified, then
            these credentials also need access to iam:GetInstanceProfile. If, however, an alternate sts configuration
            is set for the target account, then the credentials must be permissioned to call sts:AssumeRole on the
            configured role, and that role must have the permissions described here
        :param secret_key: AWS Secret key with permissions to query AWS APIs
        :param endpoint: URL to override the default generated endpoint for making AWS EC2 API calls
        :param iam_endpoint: URL to override the default generated endpoint for making AWS IAM API calls
        :param sts_endpoint: URL to override the default generated endpoint for making AWS STS API calls
        :param iam_server_id_header_value: The value to require in the X-Vault-AWS-IAM-Server-ID header as part of
            GetCallerIdentity requests that are used in the iam auth method. If not set, then no value is required or
            validated. If set, clients must include an X-Vault-AWS-IAM-Server-ID header in the headers of login
            requests, and further this header must be among the signed headers validated by AWS. This is to protect
            against different types of replay attacks, for example a signed request sent to a dev server being resent
            to a production server
        :param mount_point: The path the AWS auth method was mounted on.
        :param sts_region: Region to override the default region for making AWS STS API calls. Should only be set if
            sts_endpoint is set. If so, should be set to the region in which the custom sts_endpoint resides
        :return: The response of the request.
        """

        params = utils.remove_nones(
            {
                "max_retries": max_retries,
                "access_key": access_key,
                "secret_key": secret_key,
                "endpoint": endpoint,
                "iam_endpoint": iam_endpoint,
                "sts_endpoint": sts_endpoint,
                "iam_server_id_header_value": iam_server_id_header_value,
                "sts_region": sts_region,
            }
        )
        api_path = f"/v1/auth/{mount_point}/config/client"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_config(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT):
        """
        Read previously configured AWS access credentials.

        Supported methods:
            GET: /auth/{mount_point}/config. Produces: 200 application/json

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The data key from the VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/client"
        response = await self._adapter.get(
            url=api_path,
        )
        return response.value["data"]

    async def delete_config(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT):
        """
        Delete previously configured AWS access credentials,

        Supported methods:
            DELETE: /auth/{mount_point}/config Produces: 204 (empty body)

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/client"
        return await self._adapter.delete(url=api_path)

    async def configure_identity_integration(
        self,
        iam_alias: Optional[str] = None,
        ec2_alias: Optional[str] = None,
        mount_point: Optional[str] = AWS_DEFAULT_MOUNT_POINT,
        iam_metadata: Optional[str] = None,
        ec2_metadata: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Configure the way that Vault interacts with the Identity store.

        The default (as of Vault 1.0.3) is role_id for both values.

        Supported methods:
            POST: /auth/{mount_point}/config/identity Produces: 204 (empty body)

        :param iam_alias: How to generate the identity alias when using the iam auth method. Valid choices are role_id,
            unique_id, and full_arn When role_id is selected, the randomly generated ID of the role is used. When
            unique_id is selected, the IAM Unique ID of the IAM principal (either the user or role) is used as the
            identity alias name. When full_arn is selected, the ARN returned by the sts:GetCallerIdentity call is used
            as the alias name. This is either arn:aws:iam::<account_id>:user/<optional_path/><user_name> or
            arn:aws:sts::<account_id>:assumed-role/<role_name_without_path>/<role_session_name>. Note: if you
            select full_arn and then delete and recreate the IAM role, Vault won't be aware and any identity aliases
            set up for the role name will still be valid
        :param iam_metadata: The metadata to include on the token returned by the login endpoint.
            This metadata will be added to both audit logs, and on the ``iam_alias``. By default, it includes
            ``account_id`` and ``auth_type``. Additionally, ``canonical_arn``, ``client_arn``, ``client_user_id``,
            ``inferred_aws_region``, ``inferred_entity_id``, and ``inferred_entity_type`` are available.
            To include no metadata, set to an empty list ``[]``. To use only particular fields,
            select the explicit fields. To restore to defaults, send only a field of ``default``. Only select fields
            that will have a low rate of change for your ``iam_alias`` because each change triggers a storage
            write and can have a performance impact at scale.
        :param ec2_alias: Configures how to generate the identity alias when using the ec2 auth method. Valid choices
            are role_id, instance_id, and image_id. When role_id is selected, the randomly generated ID of the role is
            used. When instance_id is selected, the instance identifier is used as the identity alias name. When
            image_id selected, AMI ID of the instance used as the identity alias name
        :param ec2_metadata: The metadata to include on the token returned by the login endpoint. This metadata will be
            added to both audit logs, and on the ``ec2_alias``.
            By default, it includes ``account_id`` and ``auth_type``. Additionally, ``ami_id``, ``instance_id``,
            and ``region`` are available. To include no metadata, set to an empty list ``[]``.
            To use only particular fields, select the explicit fields. To restore to defaults,
            send only a field of ``default``. Only select fields that will have a low rate of change for your
            ``ec2_alias`` because each change triggers a storage write and can have a performance impact at scale.
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request
        """
        if iam_alias is not None and iam_alias not in ALLOWED_IAM_ALIAS_TYPES:
            error_msg = (
                f"invalid iam alias type provided: '{iam_alias}' - "
                f"supported iam alias types: '{','.join(ALLOWED_IAM_ALIAS_TYPES)}'"
            )
            raise exceptions.VaultxError(error_msg)
        if ec2_alias is not None and ec2_alias not in ALLOWED_EC2_ALIAS_TYPES:
            error_msg = (
                f"invalid ec2 alias type provided: '{ec2_alias}' - "
                f"supported ec2 alias types: '{','.join(ALLOWED_EC2_ALIAS_TYPES)}'"
            )
            raise exceptions.VaultxError(error_msg)

        params = utils.remove_nones(
            {
                "iam_alias": iam_alias,
                "ec2_alias": ec2_alias,
                "ec2_metadata": ec2_metadata,
                "iam_metadata": iam_metadata,
            }
        )
        api_auth = f"/v1/auth/{mount_point}/config/identity"
        return await self._adapter.post(
            url=api_auth,
            json=params,
        )

    async def read_identity_integration(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Return previously configured identity integration configuration.

        Supported methods:
            GET: /auth/{mount_point}/config/identity. Produces: 200 application/json

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The data key from the VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/identity"
        response = await self._adapter.get(
            url=api_path,
        )
        return response.value["data"]

    async def create_certificate_configuration(
        self,
        cert_name: str,
        aws_public_cert: str,
        document_type: Optional[str] = None,
        mount_point: str = AWS_DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Register AWS public key to be used to verify the instance identity documents.

        While the PKCS#7 signature of the identity documents have DSA digest, the identity signature will have RSA
        digest, and hence the public keys for each type varies respectively. Indicate the type of the public key using
        the "type" parameter

        Supported methods:
            POST: /auth/{mount_point}/config/certificate/:cert_name Produces: 204 (empty body)

        :param cert_name: Name of the certificate
        :param aws_public_cert: Base64 encoded AWS Public key required to verify PKCS7 signature of the EC2 instance
            metadata
        :param document_type: Takes the value of either "pkcs7" or "identity", indicating the type of document
            which can be verified using the given certificate
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request
        """
        params = {
            "cert_name": cert_name,
            "aws_public_cert": aws_public_cert,
        }
        params.update(
            utils.remove_nones(
                {
                    "document_type": document_type,
                }
            )
        )
        api_path = f"/v1/auth/{mount_point}/config/certificate/{cert_name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_certificate_configuration(
        self, cert_name: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Return previously configured AWS public key.

        Supported methods:
            GET: /v1/auth/{mount_point}/config/certificate/:cert_name Produces: 200 application/json

        :param cert_name: Name of the certificate
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The data key from the VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/certificate/{cert_name}"
        response = await self._adapter.get(
            url=api_path,
        )
        return response.value["data"]

    async def delete_certificate_configuration(self, cert_name: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT):
        """
        Remove previously configured AWS public key.

        Supported methods:
            DELETE: /auth/{mount_point}/config/certificate/:cert_name Produces: 204 (empty body)

        :param cert_name: Name of the certificate
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request
        """
        api_path = f"/v1/auth/{mount_point}/config/certificate/{cert_name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def list_certificate_configurations(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT):
        """
        List AWS public certificates that are registered with the method.

        Supported methods
            LIST: /auth/{mount_point}/config/certificates Produces: 200 application/json

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/certificates"
        response = await self._adapter.list(
            url=api_path,
        )
        return response.value["data"]

    async def create_sts_role(
        self, account_id: str, sts_role: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Allow the explicit association of STS roles to satellite AWS accounts (i.e. those which are not the
        account in which the Vault server is running.)

        Vault will use credentials obtained by assuming these STS roles when validating IAM principals or EC2
        instances in the particular AWS account

        Supported methods:
            POST: /v1/auth/{mount_point}/config/sts/:account_id Produces: 204 (empty body)

        :param account_id: AWS account ID to be associated with STS role.
            If set, Vault will use assumed credentials to verify any login attempts from EC2 instances in this account.
        :param sts_role: AWS ARN for STS role to be assumed when interacting with the account specified.
            The Vault server must have permissions to assume this role.
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/sts/{account_id}"
        params = {
            "account_id": account_id,
            "sts_role": sts_role,
        }
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_sts_role(self, account_id: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> dict:
        """
        Return previously configured STS role.

        :param account_id: AWS account ID that has been previously associated with STS role.
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/sts/{account_id}"
        response = await self._adapter.get(
            url=api_path,
        )
        return response.value["data"]

    async def list_sts_roles(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> dict:
        """
        List AWS Account IDs for which an STS role is registered.

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/sts"
        response = await self._adapter.list(url=api_path)
        return response.value["data"]

    async def delete_sts_role(self, account_id: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete a previously configured AWS account/STS role association.

        :param account_id:
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/sts/{account_id}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def configure_identity_whitelist_tidy(
        self,
        safety_buffer: Optional[str] = None,
        disable_periodic_tidy: Optional[bool] = None,
        mount_point: str = AWS_DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure the periodic tidying operation of the whitelisted identity entries.

        :param safety_buffer: The amount of extra time that must have passed beyond the roletag expiration, before
            it is removed from the method storage.
        :param disable_periodic_tidy: If set to 'true', disables the periodic tidying of
            the identity-whitelist/<instance_id> entries.
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/tidy/identity-whitelist"
        params = utils.remove_nones(
            {
                "safety_buffer": safety_buffer,
                "disable_periodic_tidy": disable_periodic_tidy,
            }
        )
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_identity_whitelist_tidy(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> dict:
        """
        Read previously configured periodic whitelist tidying settings.

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/tidy/identity-whitelist"
        response = await self._adapter.get(url=api_path)
        return response.value["data"]

    async def delete_identity_whitelist_tidy(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """Delete previously configured periodic whitelist tidying settings.

        :param mount_point: The path the AWS auth method was mounted on.
        :type mount_point: str
        :return: The response of the request.
        :rtype: requests.Response
        """
        api_path = f"/v1/auth/{mount_point}/config/tidy/identity-whitelist"
        return await self._adapter.delete(
            url=api_path,
        )

    async def configure_role_tag_blacklist_tidy(
        self,
        safety_buffer: Optional[str] = None,
        disable_periodic_tidy: Optional[bool] = None,
        mount_point: str = AWS_DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure the periodic tidying operation of the blacklisted role tag entries.

        :param safety_buffer: The amount of extra time that must have passed beyond the roletag expiration, before
            it is removed from the method storage.
        :param disable_periodic_tidy: If set to 'true',
            disables the periodic tidying of the roletag-blacklist/<instance_id> entries.
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/tidy/roletag-blacklist"
        params = utils.remove_nones(
            {
                "safety_buffer": safety_buffer,
                "disable_periodic_tidy": disable_periodic_tidy,
            }
        )
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_role_tag_blacklist_tidy(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> dict:
        """
        Read previously configured periodic blacklist tidying settings.

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/tidy/roletag-blacklist"
        response = await self._adapter.get(url=api_path)
        return response.value["data"]

    async def delete_role_tag_blacklist_tidy(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete previously configured periodic blacklist tidying settings.

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config/tidy/roletag-blacklist"
        return await self._adapter.delete(url=api_path)

    async def create_role(
        self,
        role: str,
        auth_type: str = "iam",
        bound_ami_id: Optional[list[str]] = None,
        bound_account_id: Optional[list[str]] = None,
        bound_region: Optional[list[str]] = None,
        bound_vpc_id: Optional[list[str]] = None,
        bound_subnet_id: Optional[list[str]] = None,
        bound_iam_role_arn: Optional[list[str]] = None,
        bound_iam_instance_profile_arn: Optional[list[str]] = None,
        bound_ec2_instance_id: Optional[list] = None,
        role_tag: Optional[str] = None,
        bound_iam_principal_arn: Optional[list[str]] = None,
        inferred_entity_type: Optional[str] = None,
        inferred_aws_region: Optional[str] = None,
        resolve_aws_unique_ids: Optional[bool] = None,
        ttl: Optional[Union[str, int]] = None,
        max_ttl: Optional[Union[str, int]] = None,
        period: Optional[Union[str, int]] = None,
        policies: Optional[Union[list, str]] = None,
        allow_instance_migration: Optional[bool] = None,
        disallow_reauthentication: Optional[bool] = None,
        mount_point: str = AWS_DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Register a role in the method.

        https://developer.hashicorp.com/vault/api-docs/auth/aws#create-update-role

        :param role:
        :param auth_type:
        :param bound_ami_id:
        :param bound_account_id:
        :param bound_region:
        :param bound_vpc_id:
        :param bound_subnet_id:
        :param bound_iam_role_arn:
        :param bound_iam_instance_profile_arn:
        :param bound_ec2_instance_id:
        :param role_tag:
        :param bound_iam_principal_arn:
        :param inferred_entity_type:
        :param inferred_aws_region:
        :param resolve_aws_unique_ids:
        :param ttl:
        :param max_ttl:
        :param period:
        :param policies:
        :param allow_instance_migration:
        :param disallow_reauthentication:
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/role/{role}"
        params = {
            "role": role,
        }
        params.update(
            utils.remove_nones(
                {
                    "auth_type": auth_type,
                    "resolve_aws_unique_ids": resolve_aws_unique_ids,
                    "bound_ami_id": bound_ami_id,
                    "bound_account_id": bound_account_id,
                    "bound_region": bound_region,
                    "bound_vpc_id": bound_vpc_id,
                    "bound_subnet_id": bound_subnet_id,
                    "bound_iam_role_arn": bound_iam_role_arn,
                    "bound_iam_instance_profile_arn": bound_iam_instance_profile_arn,
                    "bound_ec2_instance_id": bound_ec2_instance_id,
                    "role_tag": role_tag,
                    "bound_iam_principal_arn": bound_iam_principal_arn,
                    "inferred_entity_type": inferred_entity_type,
                    "inferred_aws_region": inferred_aws_region,
                    "ttl": ttl,
                    "max_ttl": max_ttl,
                    "period": period,
                    "policies": policies,
                    "allow_instance_migration": allow_instance_migration,
                    "disallow_reauthentication": disallow_reauthentication,
                }
            )
        )
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_role(self, role: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> dict:
        """
        Return the previously registered role configuration

        :param role:
        :param mount_point: The path the AWS auth method was mounted on.
        :type mount_point: str
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/role/{role}"
        response = await self._adapter.get(url=api_path)
        return response.value["data"]

    async def list_roles(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> dict:
        """
        List all the roles that are registered with the method

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/roles"
        response = await self._adapter.list(
            url=api_path,
        )
        return response.value["data"]

    async def delete_role(self, role: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete the previously registered role

        :param role:
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/role/{role}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def create_role_tags(
        self,
        role: str,
        policies: Optional[list] = None,
        max_ttl: Optional[str] = None,
        instance_id: Optional[str] = None,
        allow_instance_migration: Optional[bool] = None,
        disallow_reauthentication: Optional[bool] = None,
        mount_point: str = AWS_DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create a role tag on the role, which helps in restricting the capabilities that are set on the role.

        Role tags are not tied to any specific ec2 instance unless specified explicitly using the
        instance_id parameter. By default, role tags are designed to be used across all instances that
        satisfies the constraints on the role. Regardless of which instances have role tags on them, capabilities
        defined in a role tag must be a strict subset of the given role's capabilities. Note that, since adding
        and removing a tag is often a widely distributed privilege, care needs to be taken to ensure that the
        instances are attached with correct tags to not let them gain more privileges than what were intended.
        If a role tag is changed, the capabilities inherited by the instance will be those defined on the new role
        tag. Since those must be a subset of the role capabilities, the role should never provide more capabilities
        than any given instance can be allowed to gain in a worst-case scenario

        :param role: Name of the role.
        :param policies: Policies to be associated with the tag. If set, must be a subset of the role's policies. If
            set, but set to an empty value, only the 'default' policy will be given to issued tokens.
        :param max_ttl: The maximum allowed lifetime of tokens issued using this role.
        :param instance_id: Instance ID for which this tag is intended for. If set, the created tag can only be used by
            the instance with the given ID.
        :param disallow_reauthentication: If set, only allows a single token to be granted per instance ID. This can be
            cleared with the auth/aws/identity-whitelist endpoint. Defaults to 'false'. Mutually exclusive with
            allow_instance_migration.
        :param allow_instance_migration: If set, allows migration of the underlying instance where the client resides.
            This keys off of pendingTime in the metadata document, so essentially, this disables the client nonce check
            whenever the instance is migrated to a new host and pendingTime is newer than the previously-remembered
            time. Use with caution. Defaults to 'false'. Mutually exclusive with disallow_reauthentication.
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The create_role_tag response.
        """
        api_path = f"/v1/auth/{mount_point}/role/{role}/tag"

        params = utils.remove_nones(
            {
                "disallow_reauthentication": disallow_reauthentication,
                "policies": policies,
                "max_ttl": max_ttl,
                "instance_id": instance_id,
                "allow_instance_migration": allow_instance_migration,
            }
        )
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def iam_login(
        self,
        access_key: str,
        secret_key: str,
        session_token: Optional[str] = None,
        header_value: Optional[str] = None,
        role: Optional[str] = None,
        use_token: bool = True,
        region: str = "us-east-1",
        mount_point: str = AWS_DEFAULT_MOUNT_POINT,
    ):
        """
        Fetch a token

        This endpoint verifies the pkcs7 signature of the instance identity document or the signature of the
        signed GetCallerIdentity request. With the ec2 auth method, or when inferring an EC2 instance,
        verifies that the instance is actually in a running state. Cross checks the constraints defined on the
        role with which the login is being performed. With the ec2 auth method, as an alternative to pkcs7
        signature, the identity document along with its RSA digest can be supplied to this endpoint

        :param access_key:
        :param secret_key:
        :param session_token:
        :param header_value:
        :param role: Name of the role against which the login is being attempted.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.Adapter` instance under the _adapter Client attribute.
        :param region:
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/login"

        request = generate_sigv4_auth_request(header_value=header_value)
        auth = SigV4Auth(access_key, secret_key, session_token, region)
        auth.add_auth(request)

        # https://github.com/hashicorp/vault/blob/master/builtin/credential/aws/cli.go
        headers = json.dumps({k: [request.headers[k]] for k in request.headers})
        params = {
            "iam_http_request_method": request.method,
            "iam_request_url": b64encode(str(request.url).encode("utf-8")).decode("utf-8"),
            "iam_request_headers": b64encode(headers.encode("utf-8")).decode("utf-8"),
            "iam_request_body": b64encode(request.content).decode("utf-8"),
            "role": role,
        }

        return await self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )

    async def ec2_login(
        self,
        pkcs7: str,
        nonce: Optional[str] = None,
        role: Optional[str] = None,
        use_token: bool = True,
        mount_point: str = AWS_DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Retrieve a Vault token using an AWS authentication method mount's EC2 role.

        :param pkcs7: PKCS7 signature of the identity document with all newline characters removed.
        :param nonce: The nonce to be used for subsequent login requests.
        :param role: Name of the role against which the login is being attempted.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.Adapter` instance under the _adapter Client attribute.
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/login"
        params = {"pkcs7": pkcs7}
        if nonce:
            params["nonce"] = nonce
        if role:
            params["role"] = role

        return await self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )

    async def place_role_tags_in_blacklist(self, role_tag, mount_point=AWS_DEFAULT_MOUNT_POINT):
        """
        Place a valid role tag in a blacklist

        This ensures that the role tag cannot be used by any instance to perform a login operation again. Note
        that if the role tag was previously used to perform a successful login, placing the tag in the blacklist
        does not invalidate the already issued token

        :param role_tag:
        :param mount_point: The path the AWS auth method was mounted on.
        :type mount_point: str
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/roletag-blacklist/{role_tag}"
        return await self._adapter.post(url=api_path)

    async def read_role_tag_blacklist(self, role_tag: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> dict:
        """
        Return the blacklist entry of a previously blacklisted role tag

        :param role_tag:
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/roletag-blacklist/{role_tag}"
        response = await self._adapter.get(url=api_path)
        return response.value["data"]

    async def list_blacklist_tags(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> dict:
        """
        List all the role tags that are blacklisted

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/roletag-blacklist"
        response = await self._adapter.list(
            url=api_path,
        )
        return response.value["data"]

    async def delete_blacklist_tags(self, role_tag: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete a blacklisted role tag

        :param role_tag:
        :param mount_point: The path the AWS auth method was mounted on.
        :type mount_point: str
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/roletag-blacklist/{role_tag}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def tidy_blacklist_tags(
        self, safety_buffer: str = "72h", mount_point: str = AWS_DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Clean up the entries in the blacklist based on expiration time on the entry and safety_buffer

        :param safety_buffer:
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/tidy/roletag-blacklist"
        params = {
            "safety_buffer": safety_buffer,
        }
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_identity_whitelist(self, instance_id: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> dict:
        """
        Return an entry in the whitelist. An entry will be created/updated by every successful login

        :param instance_id:
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/identity-whitelist/{instance_id}"
        response = await self._adapter.get(url=api_path)
        return response.value["data"]

    async def list_identity_whitelist(self, mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> dict:
        """
        List all the instance IDs that are in the whitelist of successful logins

        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/identity-whitelist"
        response = await self._adapter.list(
            url=api_path,
        )
        return response.value["data"]

    async def delete_identity_whitelist_entries(
        self, instance_id: str, mount_point: str = AWS_DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Delete a cache of the successful login from an instance

        :param instance_id:
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/identity-whitelist/{instance_id}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def tidy_identity_whitelist_entries(
        self, safety_buffer: str = "72h", mount_point: str = AWS_DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Clean up the entries in the whitelist based on expiration time and safety_buffer

        :param safety_buffer:
        :param mount_point: The path the AWS auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/tidy/identity-whitelist"
        params = {
            "safety_buffer": safety_buffer,
        }
        return await self._adapter.post(url=api_path, json=params)
