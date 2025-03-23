import json
from typing import Any, Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase
from vaultx.constants.azure import VALID_ENVIRONMENTS
from vaultx.exceptions import VaultxError


DEFAULT_MOUNT_POINT = "azure"


class Azure(VaultApiBase):
    """
    Azure Secrets Engine (API).

    Reference: https://www.vaultproject.io/api/secret/azure/index.html
    """

    def configure(
        self,
        subscription_id: str,
        tenant_id: str,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        environment: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure the credentials required for the plugin to perform API calls to Azure.

        These credentials will be used to query roles and create/delete service principals. Environment variables will
        override any parameters set in the config.

        Supported methods:
            POST: /{mount_point}/config. Produces: 204 (empty body)


        :param subscription_id: The subscription id for the Azure Active Directory
        :param tenant_id: The tenant id for the Azure Active Directory.
        :param client_id: The OAuth2 client id to connect to Azure.
        :param client_secret: The OAuth2 client secret to connect to Azure.
        :param environment: The Azure environment. If not specified, Vault will use Azure Public Cloud.
        :param mount_point: The OAuth2 client secret to connect to Azure.
        :return: The response of the request.
        """
        if environment is not None and environment not in VALID_ENVIRONMENTS:
            raise VaultxError(
                f'invalid environment argument provided "{environment}", supported environments: '
                f'"{",".join(VALID_ENVIRONMENTS)}"'
            )

        params = {
            "subscription_id": subscription_id,
            "tenant_id": tenant_id,
        }
        params.update(
            utils.remove_nones(
                {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "environment": environment,
                }
            )
        )
        api_path = f"/v1/{mount_point}/config"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> Any:
        """
        Read the stored configuration, omitting client_secret.

        Supported methods:
            GET: /{mount_point}/config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The data key from the VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config"
        response = self._adapter.get(
            url=api_path,
        )
        if isinstance(response, dict):
            return response.get("data")
        raise VaultxError("Unexpected return of non-dict response")

    def delete_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete the stored Azure configuration and credentials.

        Supported methods:
            DELETE: /auth/{mount_point}/config. Produces: 204 (empty body)


        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/config"
        return self._adapter.delete(
            url=api_path,
        )

    def create_or_update_role(
        self,
        name: str,
        azure_roles: list[dict],
        ttl: Optional[str] = None,
        max_ttl: Optional[str] = None,
        mount_point=DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update a Vault role.

        The provided Azure roles must exist for this call to succeed. See the Azure secrets roles docs for more
        information about roles.

        Supported methods:
            POST: /{mount_point}/roles/{name}. Produces: 204 (empty body)


        :param name: Name of the role.
        :param azure_roles:  List of Azure roles to be assigned to the generated service principal.
        :param ttl: Specifies the default TTL for service principals generated using this role. Accepts time suffixed
            strings ("1h") or an integer number of seconds. Defaults to the system/engine default TTL time.
        :param max_ttl: Specifies the maximum TTL for service principals generated using this role. Accepts time
            suffixed strings ("1h") or an integer number of seconds. Defaults to the system/engine max TTL time.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = {
            "azure_roles": json.dumps(azure_roles),
        }
        params.update(
            utils.remove_nones(
                {
                    "ttl": ttl,
                    "max_ttl": max_ttl,
                }
            )
        )
        api_path = f"/v1/{mount_point}/roles/{name}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def list_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> Any:
        """
        List all the roles that are registered with the plugin.

        Supported methods:
            LIST: /{mount_point}/roles. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The data key from the VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/roles"
        response = self._adapter.list(
            url=api_path,
        )
        if isinstance(response, dict):
            return response.get("data")
        raise VaultxError("Unexpected return of non-dict response")

    def generate_credentials(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> Any:
        """Generate a new service principal based on the named role.

        Supported methods:
            GET: /{mount_point}/creds/{name}. Produces: 200 application/json

        :param name: Specifies the name of the role to create credentials against.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The data key from the VaultxResponse of the request.
        :rtype: dict
        """
        api_path = f"/v1/{mount_point}/creds/{name}"
        response = self._adapter.get(
            url=api_path,
        )
        if isinstance(response, dict):
            return response.get("data")
        raise VaultxError("Unexpected return of non-dict response")
