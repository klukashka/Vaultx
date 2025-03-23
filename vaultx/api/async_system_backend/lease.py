from typing import Optional

from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


class Lease(AsyncVaultApiBase):
    async def read_lease(self, lease_id: str) -> VaultxResponse:
        """
        Retrieve lease metadata.

        Supported methods:
            PUT: /sys/leases/lookup. Produces: 200 application/json

        :param lease_id: the ID of the lease to lookup.
        :return: Parsed VaultxResponse from the leases PUT request
        """
        params = {"lease_id": lease_id}
        api_path = "/v1/sys/leases/lookup"
        return await self._adapter.put(url=api_path, json=params)

    async def list_leases(self, prefix: str) -> VaultxResponse:
        """
        Retrieve a list of lease ids.

        Supported methods:
            LIST: /sys/leases/lookup/{prefix}. Produces: 200 application/json

        :param prefix: Lease prefix to filter list by.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/sys/leases/lookup/{prefix}"
        return await self._adapter.list(
            url=api_path,
        )

    async def renew_lease(self, lease_id: str, increment: Optional[int] = None) -> VaultxResponse:
        """Renew a lease, requesting to extend the lease.

        Supported methods:
            PUT: /sys/leases/renew. Produces: 200 application/json

        :param lease_id: The ID of the lease to extend.
        :param increment: The requested amount of time (in seconds) to extend the lease.
        :return: The VaultxResponse of the request
        """
        params = {
            "lease_id": lease_id,
            "increment": increment,
        }
        api_path = "/v1/sys/leases/renew"
        return await self._adapter.put(
            url=api_path,
            json=params,
        )

    async def revoke_lease(self, lease_id: str) -> VaultxResponse:
        """
        Revoke a lease immediately.

        Supported methods:
            PUT: /sys/leases/revoke. Produces: 204 (empty body)

        :param lease_id: Specifies the ID of the lease to revoke.
        :return: The response of the request.
        """
        params = {
            "lease_id": lease_id,
        }
        api_path = "/v1/sys/leases/revoke"
        return await self._adapter.put(
            url=api_path,
            json=params,
        )

    async def revoke_prefix(self, prefix: str) -> VaultxResponse:
        """
        Revoke all secrets (via a lease ID prefix) or tokens (via the tokens' path property) generated under a given
        prefix immediately.
        This requires sudo capability and access to it should be tightly controlled as it can be used to revoke very
        large numbers of secrets/tokens at once.

        Supported methods:
            PUT: /sys/leases/revoke-prefix/{prefix}. Produces: 204 (empty body)


        :param prefix: The prefix to revoke.
        :return: The response of the request.
        """
        params = {
            "prefix": prefix,
        }
        api_path = f"/v1/sys/leases/revoke-prefix/{prefix}"
        return await self._adapter.put(
            url=api_path,
            json=params,
        )

    async def revoke_force(self, prefix: str) -> VaultxResponse:
        """
        Revoke all secrets or tokens generated under a given prefix immediately.
        Unlike revoke_prefix, this path ignores backend errors encountered during revocation. This is potentially very
        dangerous and should only be used in specific emergency situations where errors in the backend or the connected
        backend service prevent normal revocation.

        Supported methods:
            PUT: /sys/leases/revoke-force/{prefix}. Produces: 204 (empty body)

        :param prefix: The prefix to revoke.
        :return: The response of the request.
        """
        params = {
            "prefix": prefix,
        }
        api_path = f"/v1/sys/leases/revoke-force/{prefix}"
        return await self._adapter.put(
            url=api_path,
            json=params,
        )
