import json
from typing import Optional, Union

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase
from vaultx.constants.aws import (
    ALLOWED_CREDS_ENDPOINTS,
    ALLOWED_CREDS_TYPES,
    DEFAULT_MOUNT_POINT,
)
from vaultx.exceptions import VaultxError


class Aws(VaultApiBase):
    """
    AWS Secrets Engine (API).

    Reference: https://www.vaultproject.io/api/secret/aws/index.html
    """

    def configure_root_iam_credentials(
        self,
        access_key: str,
        secret_key: str,
        region: Optional[str] = None,
        iam_endpoint: Optional[str] = None,
        sts_endpoint: Optional[str] = None,
        max_retries: Optional[int] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure the root IAM credentials to communicate with AWS.
        There are multiple ways to pass root IAM credentials to the Vault server, specified below with the highest
        precedence first. If credentials already exist, this will overwrite them.

        The official AWS SDK is used for sourcing credentials from env vars, shared files, or IAM/ECS instances.

            * Static credentials provided to the API as a payload
            * Credentials in the AWS_ACCESS_KEY, AWS_SECRET_KEY, and AWS_REGION environment variables on the server
            * Shared credentials files
            * Assigned IAM role or ECS task role credentials

        At present, this endpoint does not confirm that the provided AWS credentials are valid AWS credentials with
        proper permissions.

        Supported methods:
            POST: /{mount_point}/config/root. Produces: 204 (empty body)

        :param access_key: Specifies the AWS access key ID.
        :param secret_key: Specifies the AWS secret access key.
        :param region: Specifies the AWS region. If not set it will use the AWS_REGION env var, AWS_DEFAULT_REGION env
            var, or us-east-1 in that order.
        :param iam_endpoint: Specifies a custom HTTP IAM endpoint to use.
        :param sts_endpoint: Specifies a custom HTTP STS endpoint to use.
        :param max_retries: Number of max retries the client should use for recoverable errors. The default (-1) falls
            back to the AWS SDK's default behavior.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = {
            "access_key": access_key,
            "secret_key": secret_key,
            "max_retries": max_retries,
        }
        params.update(
            utils.remove_nones(
                {
                    "region": region,
                    "iam_endpoint": iam_endpoint,
                    "sts_endpoint": sts_endpoint,
                }
            )
        )
        api_path = f"/v1/{mount_point}/config/root"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def rotate_root_iam_credentials(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Rotate static root IAM credentials.

        When you have configured Vault with static credentials, you can use this endpoint to have Vault rotate the
        access key it used. Note that, due to AWS eventual consistency, after calling this endpoint, subsequent calls
        from Vault to AWS may fail for a few seconds until AWS becomes consistent again.

        In order to call this endpoint, Vault's AWS access key MUST be the only access key on the IAM user; otherwise,
        generation of a new access key will fail. Once this method is called, Vault will now be the only entity that
        knows the AWS secret key is used to access AWS.

        Supported methods:
            POST: /{mount_point}/config/rotate-root. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config/rotate-root"
        return self._adapter.post(
            url=api_path,
        )

    def configure_lease(self, lease: str, lease_max: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Configure lease settings for the AWS secrets engine.

        It is optional, as there are default values for lease and lease_max.

        Supported methods:
            POST: /{mount_point}/config/lease. Produces: 204 (empty body)

        :param lease: Specifies the lease value provided as a string duration with time suffix. "h" (hour) is the
            largest suffix.
        :param lease_max: Specifies the maximum lease value provided as a string duration with time suffix. "h" (hour)
            is the largest suffix.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = {
            "lease": lease,
            "lease_max": lease_max,
        }
        api_path = f"/v1/{mount_point}/config/lease"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_lease_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """Read the current lease settings for the AWS secrets engine.

        Supported methods:
            GET: /{mount_point}/config/lease. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config/lease"
        return self._adapter.get(
            url=api_path,
        )

    def create_or_update_role(
        self,
        name: str,
        credential_type: str,
        policy_document: Optional[Union[dict, str]] = None,
        default_sts_ttl: Optional[str] = None,
        max_sts_ttl: Optional[str] = None,
        role_arns: Optional[Union[list, str]] = None,
        policy_arns: Optional[list] = None,
        iam_tags: Optional[list[str]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update the role with the given name.

        If a role with the name does not exist, it will be created. If the role exists, it will be updated with the new
        attributes.

        Supported methods:
            POST: /{mount_point}/roles/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the role to create. This is part of the request URL.
        :param credential_type: Specifies the type of credential to be used when retrieving credentials from the role.
            Must be one of iam_user, assumed_role, or federation_token.
        :param policy_document: The IAM policy document for the role. The behavior depends on the credential type. With
            iam_user, the policy document will be attached to the IAM user generated and augment the permissions the IAM
            user has. With assumed_role and federation_token, the policy document will act as a filter on what the
            credentials can do.
        :param default_sts_ttl: The default TTL for STS credentials. When a TTL is not specified when STS credentials
            are requested, and a default TTL is specified on the role, then this default TTL will be used. Valid only
            when credential_type is one of assumed_role or federation_token.
        :param max_sts_ttl: The max allowed TTL for STS credentials (credentials TTL are capped to max_sts_ttl). Valid
            only when credential_type is one of assumed_role or federation_token.
        :param role_arns: Specifies the ARNs of the AWS roles this Vault role is allowed to assume. Required when
            credential_type is assumed_role and prohibited otherwise. This is a comma-separated string or JSON array.
            String types supported for Vault legacy parameters.
        :param policy_arns: Specifies the ARNs of the AWS managed policies to be attached to IAM users when they are
            requested. Valid only when credential_type is iam_user. When credential_type is iam_user, at least one of
            policy_arns or policy_document must be specified. This is a comma-separated string or JSON array.
        :param iam_tags: A list of strings representing a key/value pair to be used for any IAM user that is created by
            this role. Format is a key and value separated by an =.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        if credential_type not in ALLOWED_CREDS_TYPES:
            raise VaultxError(
                f'invalid credential_type argument provided "{credential_type}", supported types: '
                f'"{", ".join(ALLOWED_CREDS_TYPES)}"'
            )
        if isinstance(policy_document, dict):
            policy_document = json.dumps(policy_document, indent=4, sort_keys=True)

        params = {
            "credential_type": credential_type,
        }
        params.update(
            utils.remove_nones(
                {
                    "policy_document": policy_document,
                    "default_sts_ttl": default_sts_ttl,
                    "max_sts_ttl": max_sts_ttl,
                    "role_arns": role_arns,
                    "policy_arns": policy_arns,
                    "iam_tags": iam_tags,
                }
            )
        )
        api_path = f"/v1/{mount_point}/roles/{name}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query an existing role by the given name.

        If the role does not exist, a 404 is returned.

        Supported methods:
            GET: /{mount_point}/roles/{name}. Produces: 200 application/json

        :param name: Specifies the name of the role to read. This is part of the request URL.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def list_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List all existing roles in the secrets engine.

        Supported methods:
            LIST: /{mount_point}/roles. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/roles"
        return self._adapter.list(
            url=api_path,
        )

    def delete_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an existing role by the given name.

        If the role does not exist, a 404 is returned.

        Supported methods:
            DELETE: /{mount_point}/roles/{name}. Produces: 204 (empty body)

        :param name: the name of the role to delete. This
            is part of the request URL.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        :rtype: requests.Response
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        return self._adapter.delete(
            url=api_path,
        )

    def generate_credentials(
        self,
        name: str,
        role_arn: Optional[str] = None,
        ttl: Optional[str] = None,
        endpoint: str = "creds",
        mount_point: str = DEFAULT_MOUNT_POINT,
        role_session_name: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Generate credential based on the named role.

        This role must be created before queried.

        The ``/aws/creds`` and ``/aws/sts`` endpoints are almost identical. The exception is when
        retrieving credentials for a role that was specified with the legacy arn or policy parameter.
        In this case, credentials retrieved through ``/aws/sts`` must be of either the ``assumed_role`` or
        ``federation_token`` types, and credentials retrieved through ``/aws/creds`` must be of the ``iam_user`` type.

        :param name: Specifies the name of the role to generate credentials against. This is part of the request URL.
        :param role_arn: The ARN of the role to assume if ``credential_type`` on the Vault role is assumed_role.
            Must match one of the allowed role ARNs in the Vault role. Optional if the Vault role only allows
            a single AWS role ARN; required otherwise.
        :param ttl: Specifies the TTL for the use of the STS token. This is specified as a string
            with a duration suffix. Valid only when ``credential_type`` is ``assumed_role`` or ``federation_token``.
            When not specified, the async default sts_ttl set for the role will be used. If that is also not set,
            then the async default value of ``3600s`` will be used. AWS places limits on the maximum TTL allowed.
            See the AWS documentation on the ``DurationSeconds`` parameter for
            AssumeRole (for ``assumed_role`` credential types) and
            GetFederationToken (for ``federation_token`` credential types) for more details.
        :param endpoint: Supported endpoints are ``creds`` and ``sts``:
            GET: ``/{mount_point}/creds/{name}``. Produces: 200 application/json
            POST: ``/{mount_point}/sts/{name}``. Produces: 200 application/json
        :param mount_point: The "path" the method/backend was mounted on.
        :param role_session_name: The role session name to attach to the assumed role ARN.
            ``role_session_name`` is limited to 64 characters; if exceeded, the ``role_session_name``
            in the assumed role ARN will be truncated to 64 characters. If ``role_session_name`` is not provided,
            then it will be generated dynamically by async default.

        :return: The VaultxResponse of the request.
        """
        if endpoint not in ALLOWED_CREDS_ENDPOINTS:
            raise VaultxError(
                f'invalid endpoint argument provided "{endpoint}", '
                f'supported types: "{", ".join(ALLOWED_CREDS_ENDPOINTS)}"'
            )

        params = {}
        params.update(
            utils.remove_nones(
                {
                    "role_arn": role_arn,
                    "role_session_name": role_session_name,
                    "ttl": ttl,
                }
            )
        )
        api_path = f"/v1/{mount_point}/{endpoint}/{name}"

        if endpoint == "sts":
            return self._adapter.post(
                url=api_path,
                json=params,
            )
        return self._adapter.get(
            url=api_path,
            params=params,
        )
