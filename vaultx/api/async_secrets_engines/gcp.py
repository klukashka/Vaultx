import json
import logging
from typing import Optional, Union

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase
from vaultx.constants.gcp import (
    ALLOWED_SECRETS_TYPES,
    SERVICE_ACCOUNT_KEY_ALGORITHMS,
    SERVICE_ACCOUNT_KEY_TYPES,
)
from vaultx.exceptions import VaultxError


DEFAULT_MOUNT_POINT = "gcp"


class Gcp(AsyncVaultApiBase):
    """
    Google Cloud Secrets Engine (API).

    Reference: https://www.vaultproject.io/api/secret/gcp/index.html
    """

    async def configure(
        self,
        credentials: Optional[str] = None,
        ttl: Optional[Union[str, int]] = None,
        max_ttl: Optional[Union[str, int]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure shared information for the Gcp secrets engine.

        Supported methods:
            POST: /{mount_point}/config. Produces: 204 (empty body)

        :param credentials: JSON credentials (either file contents or '@path/to/file') See docs for alternative ways to
            pass in to this parameter, as well as the required permissions.
        :param ttl: – Specifies default config TTL for long-lived credentials (i.e. service account keys). Accepts
            integer number of seconds or Go duration format string.
        :param max_ttl: Specifies the maximum config TTL for long-lived credentials (i.e. service account keys). Accepts
            integer number of seconds or Go duration format string.**
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = utils.remove_nones(
            {
                "credentials": credentials,
                "ttl": ttl,
                "max_ttl": max_ttl,
            }
        )
        api_path = f"/v1/{mount_point}/config"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def rotate_root_credentials(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Rotate the GCP service account credentials used by Vault for this mount.

        A new key will be generated for the service account, replacing the internal value, and then a deletion of the
        old service account key is scheduled. Note that this does not create a new service account, only a new version
        of the service account key.

        Supported methods:
            POST: /{mount_point}/config/rotate-root. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config/rotate-root"
        return await self._adapter.post(
            url=api_path,
        )

    async def read_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the configured shared information for the Gcp secrets engine.

        Credentials will be omitted from returned data.

        Supported methods:
            GET: /{mount_point}/config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config"
        return await self._adapter.get(
            url=api_path,
        )

    async def create_or_update_roleset(
        self,
        name: str,
        project: str,
        bindings: str,
        secret_type: Optional[str] = None,
        token_scopes: Optional[list[str]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ):
        """
        Create a roleset or update an existing roleset.

        See roleset docs for the GCP secrets backend to learn more about what happens when you create or update a
        roleset.

        Supported methods:
            POST: /{mount_point}/roleset/{name}. Produces: 204 (empty body)

        :param name: Name of the role. Cannot be updated.
        :param project: Name of the GCP project that this roleset's service account will belong to. Cannot be updated.
        :param bindings: Bindings configuration string (expects HCL or JSON format in raw or base64-encoded string)
        :param secret_type: Cannot be updated.
        :param token_scopes: List of OAuth scopes to assign to access_token secrets generated under this role set
            (access_token role sets only)
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        if secret_type is not None and secret_type not in ALLOWED_SECRETS_TYPES:
            raise VaultxError(
                f'unsupported secret_type argument provided "{secret_type}", '
                f'supported types: "{",".join(ALLOWED_SECRETS_TYPES)}"'
            )

        if isinstance(bindings, dict):
            bindings = json.dumps(bindings).replace(" ", "")
            logging.debug("bindings: %s" % bindings)

        params = {
            "project": project,
            "bindings": bindings,
        }
        params.update(
            utils.remove_nones(
                {
                    "secret_type": secret_type,
                    "token_scopes": token_scopes,
                }
            )
        )

        api_path = f"/v1/{mount_point}/roleset/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def rotate_roleset_account(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Rotate the service account this roleset uses to generate secrets.

        This also replaces the key access_token roleset. This can be used to invalidate old secrets generated by the
        roleset or fix issues if a roleset's service account (and/or keys) was changed outside of Vault (i.e.
        through GCP APIs/cloud console).

        Supported methods:
            POST: /{mount_point}/roleset/{name}/rotate. Produces: 204 (empty body)

        :param name: Name of the role.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/roleset/{name}/rotate"
        return await self._adapter.post(
            url=api_path,
        )

    async def rotate_roleset_account_key(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Rotate the service account key this roleset uses to generate access tokens.

        This does not recreate the roleset service account.

        Supported methods:
            POST: /{mount_point}/roleset/{name}/rotate-key. Produces: 204 (empty body)

        :param name: Name of the role.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/roleset/{name}/rotate-key"
        return await self._adapter.post(
            url=api_path,
        )

    async def read_roleset(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read a roleset.

        Supported methods:
            GET: /{mount_point}/roleset/{name}. Produces: 200 application/json

        :param name: Name of the role.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/roleset/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_rolesets(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List configured rolesets.

        Supported methods:
            LIST: /{mount_point}/rolesets. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/rolesets"
        return await self._adapter.list(
            url=api_path,
        )

    async def delete_roleset(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an existing roleset by the given name.

        Supported methods:
            DELETE: /{mount_point}/roleset/{name} Produces: 200 application/json

        :param name: Name of the role.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/roleset/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def generate_oauth2_access_token(
        self, roleset: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Generate an OAuth2 token with the scopes defined on the roleset.

        This OAuth access token can be used in GCP API calls, e.g. curl -H "Authorization: Bearer $TOKEN" ...

        Supported methods:
            GET: /{mount_point}/token/{roleset}. Produces: 200 application/json

        :param roleset: Name of a roleset with secret type access_token to generate access_token under.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/token/{roleset}"
        return await self._adapter.get(
            url=api_path,
        )

    async def generate_service_account_key(
        self,
        roleset: str,
        key_algorithm: str = "KEY_ALG_RSA_2048",
        key_type: str = "TYPE_GOOGLE_CREDENTIALS_FILE",
        method: str = "POST",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Generate Secret (IAM Service Account Creds): Service Account Key

        If using GET ('read'), the  optional parameters will be set to their defaults. Use POST if you want to specify
        different values for these params.

        :param roleset: Name of a roleset with secret type service_account_key to generate key under.
        :param key_algorithm: Key algorithm used to generate key. Defaults to 2k RSA key You probably should not choose
            other values (i.e. 1k),
        :param key_type: Private key type to generate. Defaults to JSON credentials file.
        :param method: Supported methods:
            POST: /{mount_point}/key/{roleset}. Produces: 200 application/json
            GET: /{mount_point}/key/{roleset}. Produces: 200 application/json
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/key/{roleset}"
        return await self._generate_service_account_key(api_path, key_algorithm, key_type, method)

    async def create_or_update_static_account(
        self,
        name: str,
        service_account_email: str,
        bindings: Optional[str] = None,
        secret_type: Optional[str] = None,
        token_scopes: Optional[list[str]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create a static account or update an existing static account.

        See static account docs for the GCP secrets backend to learn more about what happens when you create or update a
        static account.

        Supported methods:
            POST: /{mount_point}/static-account/{name}. Produces: 204 (empty body)

        :param name: Name of the static account. Cannot be updated.
        :param service_account_email: Email of the GCP service account to manage. Cannot be updated.
        :param bindings: Bindings configuration string (expects HCL or JSON format in raw or base64-encoded string)
        :param secret_type: Type of secret generated for this static account. Accepted values: access_token,
            service_account_key. Cannot be updated.
        :param token_scopes: List of OAuth scopes to assign to access_token secrets generated under this static account
            (access_token static accounts only)
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        if secret_type is not None and secret_type not in ALLOWED_SECRETS_TYPES:
            raise VaultxError(
                'unsupported secret_type argument provided "{secret_type}", '
                'supported types: "{",".join(ALLOWED_SECRETS_TYPES)}"'
            )

        if isinstance(bindings, dict):
            bindings = json.dumps(bindings).replace(" ", "")
            logging.debug("bindings: %s" % bindings)

        params = {
            "service_account_email": service_account_email,
        }
        params.update(
            utils.remove_nones(
                {
                    "bindings": bindings,
                    "secret_type": secret_type,
                    "token_scopes": token_scopes,
                }
            )
        )
        api_path = f"/v1/{mount_point}/static-account/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def rotate_static_account_key(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Rotate the service account key this static account uses to generate access tokens.

        This does not recreate the service account.

        Supported methods:
            POST: /{mount_point}/static-account/{name}/rotate-key. Produces: 204 (empty body)

        :param name: Name of the static account.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/static-account/{name}/rotate-key"
        return await self._adapter.post(
            url=api_path,
        )

    async def read_static_account(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read a static account.

        Supported methods:
            GET: /{mount_point}/static-account/{name}. Produces: 200 application/json

        :param name: Name of the static account.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/static-account/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_static_accounts(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List configured static accounts.

        Supported methods:
            LIST: /{mount_point}/static-accounts. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/static-accounts"
        return await self._adapter.list(
            url=api_path,
        )

    async def delete_static_account(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an existing static account by the given name.

        Supported methods:
            DELETE: /{mount_point}/static-account/{name} Produces: 204 (empty body)

        :param name: Name of the static account.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/static-account/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def generate_static_account_oauth2_access_token(
        self, name: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Generate an OAuth2 token with the scopes defined on the static account.

        This OAuth access token can be used in GCP API calls, e.g. curl -H "Authorization: Bearer $TOKEN" ...

        Supported methods:
            GET: /{mount_point}/static-account/{name}/token. Produces: 200 application/json

        :param name: Name of a static account with secret type access_token to generate access_token under.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/static-account/{name}/token"
        return await self._adapter.get(
            url=api_path,
        )

    async def generate_static_account_service_account_key(
        self,
        name: str,
        key_algorithm: str = "KEY_ALG_RSA_2048",
        key_type: str = "TYPE_GOOGLE_CREDENTIALS_FILE",
        method: str = "POST",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ):
        """
        Generate Secret (IAM Service Account Creds): Service Account Key

        If using GET ('read'), the  optional parameters will be set to their defaults. Use POST if you want to specify
        different values for these params.

        :param name: Name of a static account with secret type service_account_key to generate key under.
        :param key_algorithm: Key algorithm used to generate key. Defaults to 2k RSA key You probably should not choose
            other values (i.e. 1k),
        :param key_type: Private key type to generate. Defaults to JSON credentials file.
        :param method: Supported methods:
            POST: /v1/{mount_point}/static-account/{name}/key. Produces: 200 application/json
            GET: /v1/{mount_point}/static-account/{name}/key. Produces: 200 application/json
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """

        api_path = f"/v1/{mount_point}/static-account/{name}/key"
        return await self._generate_service_account_key(api_path, key_algorithm, key_type, method)

    async def create_or_update_impersonated_account(
        self,
        name: str,
        service_account_email: str,
        token_scopes: Optional[list[str]] = None,
        ttl: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create an impersonated account or update an existing impersonated account.

        See impersonated account docs for the GCP secrets backend to learn more about what happens
            when you create or update an impersonated account.

        Supported methods:
            POST: /{mount_point}/impersonated-account/{name}. Produces: 204 (empty body)

        :param name: Name of the impersonated account. Cannot be updated.
        :param service_account_email: Email of the GCP service account to manage. Cannot be updated.
        :param token_scopes: List of OAuth scopes to assign to access tokens generated under this impersonated account
        :param ttl: Lifetime of the token generated. Defaults to 1 hour and is limited to a maximum of 12 hours.
            Uses duration format strings.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = {
            "service_account_email": service_account_email,
        }
        params.update(
            utils.remove_nones(
                {
                    "token_scopes": token_scopes,
                    "ttl": ttl,
                }
            )
        )
        api_path = f"/v1/{mount_point}/impersonated-account/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_impersonated_account(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read an impersonated account.

        Supported methods:
            GET: /{mount_point}/impersonated-account/{name}. Produces: 200 application/json

        :param name: Name of the impersonated account.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/impersonated-account/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_impersonated_accounts(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List configured impersonated accounts.

        Supported methods:
            LIST: /{mount_point}/impersonated-accounts. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/impersonated-accounts"
        return await self._adapter.list(
            url=api_path,
        )

    async def delete_impersonated_account(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an existing impersonated account by the given name.

        Supported methods:
            DELETE: /{mount_point}/impersonated-account/{name} Produces: 204 (empty body)

        :param name: Name of the impersonated account.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/impersonated-account/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def generate_impersonated_account_oauth2_access_token(
        self, name: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Generate an OAuth2 token with the scopes defined on the impersonated account.

        This OAuth access token can be used in GCP API calls, e.g. curl -H "Authorization: Bearer $TOKEN" ...

        Supported methods:
            GET: /{mount_point}/impersonated-account/{name}/token. Produces: 200 application/json

        :param name: Name of the impersonated account to generate an access token under.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/impersonated-account/{name}/token"
        return await self._adapter.get(
            url=api_path,
        )

    async def _generate_service_account_key(
        self,
        api_path: str,
        key_algorithm: str = "KEY_ALG_RSA_2048",
        key_type: str = "TYPE_GOOGLE_CREDENTIALS_FILE",
        method: str = "POST",
    ) -> VaultxResponse:
        if method == "POST":
            if key_algorithm not in SERVICE_ACCOUNT_KEY_ALGORITHMS:
                raise VaultxError(
                    f'unsupported key_algorithm argument provided "{key_algorithm}", '
                    f'supported algorithms: "{",".join(SERVICE_ACCOUNT_KEY_ALGORITHMS)}"'
                )

            if key_type not in SERVICE_ACCOUNT_KEY_TYPES:
                raise VaultxError(
                    f'unsupported key_algorithm argument provided "{key_type}", '
                    f'supported algorithms: "{",".join(SERVICE_ACCOUNT_KEY_TYPES)}"'
                )

            params = {
                "key_algorithm": key_algorithm,
                "key_type": key_type,
            }

            response = await self._adapter.post(
                url=api_path,
                json=params,
            )
        elif method == "GET":
            response = await self._adapter.get(
                url=api_path,
            )
        else:
            raise VaultxError(f'"method" parameter provided invalid value; POST or GET allowed, "{method}" provided')

        return response
