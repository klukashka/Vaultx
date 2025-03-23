from typing import Optional

from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase


class Capabilities(VaultApiBase):
    def get_capabilities(
        self, paths: list[str], token: Optional[str] = None, accessor: Optional[str] = None
    ) -> VaultxResponse:
        """
        Get the capabilities associated with a token.

        Supported methods:
            POST: /sys/capabilities-self. Produces: 200 application/json
            POST: /sys/capabilities. Produces: 200 application/json
            POST: /sys/capabilities-accessor. Produces: 200 application/json

        :param paths: Paths on which capabilities are being queried.
        :param token: Token for which capabilities are being queried.
        :param accessor: Accessor of the token for which capabilities are being queried.
        :return: The VaultxResponse of the request.
        """
        params: dict = {
            "paths": paths,
        }

        if token and accessor:
            raise ValueError("You can specify either token or accessor, not both.")
        if token:
            # https://www.vaultproject.io/api/system/capabilities.html
            params["token"] = token
            api_path = "/v1/sys/capabilities"
        elif accessor:
            # https://www.vaultproject.io/api/system/capabilities-accessor.html
            params["accessor"] = accessor
            api_path = "/v1/sys/capabilities-accessor"
        else:
            # https://www.vaultproject.io/api/system/capabilities-self.html
            api_path = "/v1/sys/capabilities-self"

        return self._adapter.post(
            url=api_path,
            json=params,
        )
