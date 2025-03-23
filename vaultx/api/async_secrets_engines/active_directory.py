from typing import Optional, Union

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


DEFAULT_MOUNT_POINT = "ad"


class ActiveDirectory(AsyncVaultApiBase):
    """
    Active Directory Secrets Engine (API).
    Reference: https://www.vaultproject.io/api/secret/ad/index.html
    """

    async def configure(
        self,
        binddn: Optional[str] = None,
        bindpass: Optional[str] = None,
        url: Optional[str] = None,
        userdn: Optional[str] = None,
        upndomain: Optional[str] = None,
        ttl: Optional[Union[str, int]] = None,
        max_ttl: Optional[Union[str, int]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        **kwargs,
    ) -> VaultxResponse:
        """
        Configure shared information for the ad secrets engine.

        Supported methods:
            POST: /{mount_point}/config. Produces: 204 (empty body)

        :param binddn: Distinguished name of object to bind when performing user and group search.
        :param bindpass: Password to use along with binddn when performing user search.
        :param url: Base DN under which to perform user search.
        :param userdn: Base DN under which to perform user search.
        :param upndomain: userPrincipalDomain used to construct the UPN string for the authenticating user.
        :param ttl: – The default password time-to-live in seconds. Once the ttl has passed,
            a password will be rotated the next time it's requested.
        :param max_ttl: The maximum password time-to-live in seconds.
            No role will be allowed to set a custom ttl greater than the max_ttl
            integer number of seconds or Go duration format string.**
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = utils.remove_nones(
            {
                "binddn": binddn,
                "bindpass": bindpass,
                "url": url,
                "userdn": userdn,
                "upndomain": upndomain,
                "ttl": ttl,
                "max_ttl": max_ttl,
            }
        )

        params.update(kwargs)

        api_path = f"/v1/{mount_point}/config"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the configured shared information for the ad secrets engine.

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

    async def create_or_update_role(
        self,
        name: str,
        service_account_name: Optional[str] = None,
        ttl: Optional[Union[str, int]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint creates or updates the ad role definition.

        :param name: Specifies the name of an existing role against which to create this ad credential.
        :param service_account_name: The name of a pre-existing service account in Active Directory
            that maps to this role. This value is required on create and optional on update.
        :param ttl: Specifies the TTL for this role.
            This is provided as a string duration with a time suffix like "30s" or "1h" or as seconds.
            If not provided, the default Vault TTL is used.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ad).
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        params = {
            "name": name,
        }
        params.update(
            utils.remove_nones(
                {
                    "service_account_name": service_account_name,
                    "ttl": ttl,
                }
            )
        )
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint queries for information about an ad role with the given name.
        If no role exists with that name, a 404 is returned.
        :param name: Specifies the name of the role to query.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ad).
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint lists all existing roles in the secrets engine.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/roles"
        return await self._adapter.list(
            url=api_path,
        )

    async def delete_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint deletes a ad role with the given name.
        Even if the role does not exist, this endpoint will still return a successful response.
        :param name: Specifies the name of the role to delete.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ad).
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def generate_credentials(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint retrieves the previous and current LDAP password for
           the associated account (or rotate if required)

        :param name: Specifies the name of the role to request credentials from.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ad).
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/creds/{name}"
        return await self._adapter.get(
            url=api_path,
        )
