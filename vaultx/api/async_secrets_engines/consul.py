from typing import Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


DEFAULT_MOUNT_POINT = "consul"


class Consul(AsyncVaultApiBase):
    """
    Consul Secrets Engine (API).

    Reference: https://www.vaultproject.io/api/secret/consul/index.html
    """

    async def configure_access(
        self, address: str, token: str, scheme: Optional[str] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        This endpoint configures the access information for Consul.
        This access information is used so that Vault can communicate with Consul and generate Consul tokens.

        :param address: Specifies the address of the Consul instance, provided as "host:port" like "127.0.0.1:8500".
        :param token: Specifies the Consul ACL token to use. This must be a management type token.
        :param scheme:  Specifies the URL scheme to use.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: consul).
        :return: The response of the request.
        """
        params = {
            "address": address,
            "token": token,
        }
        params.update(
            utils.remove_nones(
                {
                    "scheme": scheme,
                }
            )
        )

        api_path = f"/v1/{mount_point}/config/access"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def create_or_update_role(
        self,
        name: str,
        policy: Optional[str] = None,
        policies: Optional[list[str]] = None,
        token_type: Optional[str] = None,
        local: Optional[bool] = None,
        ttl: Optional[str] = None,
        max_ttl: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint creates or updates the Consul role definition.
        If the role does not exist, it will be created.
        If the role already exists, it will receive updated attributes.

        :param name: Specifies the name of an existing role against which to create this Consul credential.
        :param token_type:  Specifies the type of token to create when using this role.
        Valid values are "client" or "management".
        :param policy: Specifies the base64 encoded ACL policy.
        The ACL format can be found in the Consul ACL documentation (https://www.consul.io/docs/internals/acl.html).
        This is required unless the token_type is management.
        :param policies: The list of policies to assign to the generated token.
        This is only available in Consul 1.4 and greater.
        :param local: Indicates that the token should not be replicated globally
        and instead be local to the current datacenter. Only available in Consul 1.4 and greater.
        :param ttl: Specifies the TTL for this role.
        This is provided as a string duration with a time suffix like "30s" or "1h" or as seconds.
        If not provided, the default Vault TTL is used.
        :param max_ttl: Specifies the max TTL for this role.
        This is provided as a string duration with a time suffix like "30s" or "1h" or as seconds.
        If not provided, the default Vault Max TTL is used.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: consul).
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"

        params = utils.remove_nones(
            {
                "token_type": token_type,
                "policy": policy,
                "policies": policies,
                "local": local,
                "ttl": ttl,
                "max_ttl": max_ttl,
            }
        )

        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint queries for information about a Consul role with the given name.
        If no role exists with that name, a 404 is returned.

        :param name: Specifies the name of the role to query.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: consul).
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
        This endpoint deletes a Consul role with the given name.
        Even if the role does not exist, this endpoint will still return a successful response.

        :param name: Specifies the name of the role to delete.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: consul).
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def generate_credentials(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint generates a dynamic Consul token based on the given role definition.

        :param name: Specifies the name of an existing role against which to create this Consul credential.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: consul).
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/creds/{name}"

        return await self._adapter.get(
            url=api_path,
        )
