from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


class Leader(AsyncVaultApiBase):
    async def read_leader_status(self) -> VaultxResponse:
        """
        Read the high availability status and current leader instance of Vault.

        Supported methods:
            GET: /sys/leader. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        api_path = "/v1/sys/leader"
        return await self._adapter.get(
            url=api_path,
        )

    async def step_down(self) -> VaultxResponse:
        """
        Force the node to give up active status.
        When executed against a non-active node, i.e. a standby or performance
        standby node, the request will be forwarded to the active node.
        Note that the node will sleep for ten seconds before attempting to grab
        the active lock again, but if no standby nodes grab the active lock in
        the interim, the same node may become the active node again. Requires a
        token with root policy or sudo capability on the path.

        :return: The VaultxResponse of the request.
        """
        api_path = "/v1/sys/step-down"
        return await self._adapter.put(
            url=api_path,
        )
