from typing import Optional

from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


class Wrapping(AsyncVaultApiBase):
    async def unwrap(self, token: Optional[str] = None) -> VaultxResponse:
        """
        Return the original response inside the given wrapping token.

        Unlike simply reading cubbyhole/response (which is deprecated), this endpoint provides additional validation
        checks on the token, returns the original value on the wire rather than a JSON string representation of it, and
        ensures that the response is properly audit-logged.

        Supported methods:
            POST: /sys/wrapping/unwrap. Produces: 200 application/json

        :param token: Specifies the wrapping token ID. This is required if the client token is not the wrapping token.
            Do not use the wrapping token in both locations.
        :return: The VaultxResponse of the request.
        """
        params = {}
        if token is not None:
            params["token"] = token

        api_path = "/v1/sys/wrapping/unwrap"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def wrap(self, payload: Optional[dict] = None, ttl: int = 60) -> VaultxResponse:
        """
        Wraps a serializable dictionary inside a wrapping token.

        Supported methods:
            POST: /sys/wrapping/wrap. Produces: 200 application/json

        :param payload: Specifies the data that should be wrapped inside the token.
        :param ttl: The TTL of the returned wrapping token.
        :return: The VaultxResponse of the request.
        """

        if payload is None:
            payload = {}

        api_path = "/v1/sys/wrapping/wrap"
        return await self._adapter.post(url=api_path, json=payload, headers={"X-Vault-Wrap-TTL": f"{ttl}"})
