from typing import Optional

from vaultx import exceptions, utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


class Health(AsyncVaultApiBase):
    """
    Reference: https://www.vaultproject.io/api-docs/system/health
    """

    async def read_health_status(
        self,
        standby_ok: Optional[bool] = None,
        active_code: Optional[int] = None,
        standby_code: Optional[int] = None,
        dr_secondary_code: Optional[int] = None,
        performance_standby_code: Optional[int] = None,
        sealed_code: Optional[int] = None,
        uninit_code: Optional[int] = None,
        method: str = "HEAD",
    ) -> VaultxResponse:
        """
        Read the health status of Vault.
        This matches the semantics of a Consul HTTP health check and provides a simple way to monitor the health of a
        Vault instance.

        :param standby_ok: Specifies if being a standby should still return the active status code instead of the
            standby status code. This is useful when Vault is behind a non-configurable load balance that just wants a
            200-level response.
        :param active_code: The status code that should be returned for an active node.
        :param standby_code: Specifies the status code that should be returned for a standby node.
        :param dr_secondary_code: Specifies the status code that should be returned for a DR secondary node.
        :param performance_standby_code: Specifies the status code that should be returned for a performance standby
            node.
        :param sealed_code: Specifies the status code that should be returned for a sealed node.
        :param uninit_code: Specifies the status code that should be returned for an uninitialized node.
        :param method: Supported methods:
            HEAD: /sys/health. Produces: 000 (empty body)
            GET: /sys/health. Produces: 000 application/json
        :return: The VaultxResponse of the request.
        :rtype: requests.Response
        """
        params = utils.remove_nones(
            {
                "standbyok": standby_ok,
                "activecode": active_code,
                "standbycode": standby_code,
                "drsecondarycode": dr_secondary_code,
                "performancestandbycode": performance_standby_code,
                "sealedcode": sealed_code,
                "uninitcode": uninit_code,
            }
        )

        if method == "HEAD":
            api_path = "/v1/sys/health"
            return await self._adapter.head(
                url=api_path,
                raise_exception=False,
            )
        if method == "GET":
            api_path = "/v1/sys/health"
            return await self._adapter.get(
                url=api_path,
                params=params,
                raise_exception=False,
            )
        error_message = f'"method" parameter provided invalid value; HEAD or GET allowed, "{method}" provided'
        raise exceptions.VaultxError(error_message)
