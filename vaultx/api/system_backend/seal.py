from typing import Optional

from vaultx import exceptions
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase


class Seal(VaultApiBase):
    def is_sealed(self) -> bool:
        """
        Determine if  Vault is sealed.

        :return: True if Vault is seal, False otherwise.
        """
        seal_status = self.read_seal_status()
        if isinstance(seal_status, dict):
            return seal_status["sealed"]
        raise exceptions.VaultxError("Unexpected return of non-json response")

    def read_seal_status(self) -> VaultxResponse:
        """
        Read the seal status of the Vault.
        This is an unauthenticated endpoint.

        Supported methods:
            GET: /sys/seal-status. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        api_path = "/v1/sys/seal-status"
        return self._adapter.get(
            url=api_path,
        )

    def seal(self) -> VaultxResponse:
        """
        Seal the Vault.
        In HA mode, only an active node can be sealed. Standby nodes should be restarted to get the same effect.
        Requires a token with root policy or sudo capability on the path.

        Supported methods:
            PUT: /sys/seal. Produces: 204 (empty body)

        :return: The response of the request.
        """
        api_path = "/v1/sys/seal"
        return self._adapter.put(
            url=api_path,
        )

    def submit_unseal_key(
        self, key: Optional[str] = None, reset: bool = False, migrate: bool = False
    ) -> VaultxResponse:
        """
        Enter a single master key share to progress the unsealing of the Vault.

        If the threshold number of master key shares is reached, Vault will attempt to unseal the Vault. Otherwise, this
        API must be called multiple times until that threshold is met.

        Either the key or reset parameter must be provided; if both are provided, reset takes precedence.

        Supported methods:
            PUT: /sys/unseal. Produces: 200 application/json

        :param key: Specifies a single master key share. This is required unless reset is true.
        :param reset: Specifies if previously-provided unseal keys are discarded and the unseal process is reset.
        :param migrate: Available in 1.0 Beta - Used to migrate the seal from shamir to autoseal or autoseal to shamir.
            Must be provided on all unseal key calls.
        :return: The VaultxResponse of the request.
        """

        params: dict = {
            "migrate": migrate,
        }
        if not reset and key is not None:
            params["key"] = key
        elif reset:
            params["reset"] = reset

        api_path = "/v1/sys/unseal"
        return self._adapter.put(
            url=api_path,
            json=params,
        )

    def submit_unseal_keys(self, keys: list[str], migrate: bool = False) -> Optional[VaultxResponse]:
        """
        Enter multiple master key share to progress the unsealing of the Vault.

        :param keys: List of master key shares.
        :param migrate: Available in 1.0 Beta - Used to migrate the seal from shamir to autoseal or autoseal to shamir.
            Must be provided on all unseal key calls.
        :return: The VaultxResponse of the last unseal request.
        """
        result = None

        for key in keys:
            result = self.submit_unseal_key(
                key=key,
                migrate=migrate,
            )
            if isinstance(result, dict) and not result["sealed"]:
                break

        return result
