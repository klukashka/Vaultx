from typing import Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


class Quota(AsyncVaultApiBase):
    async def read_quota(self, name: str) -> VaultxResponse:
        """
        Read quota. Only works when calling on the root namespace.

        Supported methods:
            GET: /sys/quotas/rate-limit/:name. Produces: 200 application/json

        :param name: the name of the quota to look up.
        :return: VaultxResponse from API request.
        """
        api_path = f"/v1/sys/quotas/rate-limit/{name}"
        return await self._adapter.get(url=api_path)

    async def list_quotas(self) -> VaultxResponse:
        """
        Retrieve a list of quotas by name. Only works when calling on the root namespace.

        Supported methods:
            LIST: /sys/quotas/rate-limit. Produces: 200 application/json

        :return: VaultxResponse from API request.
        """
        api_path = "/v1/sys/quotas/rate-limit"
        return await self._adapter.list(
            url=api_path,
        )

    async def create_or_update_quota(
        self,
        name: str,
        rate: float,
        path: Optional[str] = None,
        interval: Optional[str] = "1s",
        block_interval: Optional[str] = None,
        role: Optional[str] = None,
        rate_limit_type: Optional[str] = None,
        inheritable: Optional[bool] = None,
    ) -> VaultxResponse:
        """Create quota if it doesn't exist or update if already created. Only works when calling on the root namespace.

        Supported methods:
            POST: /sys/quotas/rate-limit. Produces: 204 (empty body)

        :param name: The name of the quota to create or update.
        :param path: Path of the mount or namespace to apply the quota.
        :param rate: The maximum number of requests in a given interval to be allowed. Must be positive.
        :param interval: The duration to enforce rate limit. Default is "1s".
        :param block_interval: If rate limit is reached, how long before client can send requests again.
        :param role: If quota is set on an auth mount path, restrict login requests that are made with a specified role.
        :param rate_limit_type: Type of rate limit quota. Can be lease-count or rate-limit.
        :param inheritable: If set to true on a path that is a namespace, quota will be applied to all child namespaces
        :return: API status code from request.
        """
        api_path = f"/v1/sys/quotas/rate-limit/{name}"
        params = utils.remove_nones(
            {
                "name": name,
                "path": path,
                "rate": rate,
                "interval": interval,
                "block_interval": block_interval,
                "role": role,
                "type": rate_limit_type,
                "inheritable": inheritable,
            }
        )
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def delete_quota(self, name: str) -> VaultxResponse:
        """
        Delete a given quota. Only works when calling on the root namespace.

        Supported methods:
            DELETE: /sys/quotas/rate-limit. Produces: 204 (empty body)

        :param name: Name of the quota to delete
        :return: API status code from request.
        """
        api_path = f"/v1/sys/quotas/rate-limit/{name}"
        return await self._adapter.delete(
            url=api_path,
        )
