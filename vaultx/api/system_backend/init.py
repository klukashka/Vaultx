from typing import Optional

from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase
from vaultx.exceptions import VaultxError


class Init(VaultApiBase):
    def read_init_status(self) -> VaultxResponse:
        """
        Read the initialization status of Vault.

        Supported methods:
            GET: /sys/init. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        api_path = "/v1/sys/init"
        return self._adapter.get(
            url=api_path,
        )

    def is_initialized(self) -> bool:
        """
        Determine is Vault is initialized or not.

        :return: True if Vault is initialized, False otherwise.
        """
        status = self.read_init_status()
        if isinstance(status, dict):
            return status["initialized"]
        raise VaultxError("Unexpected return of non-json response")

    def initialize(
        self,
        secret_shares: Optional[int] = None,
        secret_threshold: Optional[int] = None,
        pgp_keys: Optional[list[int]] = None,
        root_token_pgp_key: Optional[str] = None,
        stored_shares: Optional[int] = None,
        recovery_shares: Optional[int] = None,
        recovery_threshold: Optional[int] = None,
        recovery_pgp_keys: Optional[list[int]] = None,
    ) -> VaultxResponse:
        """
        Initialize a new Vault.
        The Vault must not have been previously initialized. The recovery options, as well as the stored shares option,
        are only available when using Vault HSM.

        Supported methods:
            PUT: /sys/init. Produces: 200 application/json

        :param secret_shares: The number of shares to split the master key into.
        :param secret_threshold: Specifies the number of shares required to reconstruct the master key. This must be
            less than or equal secret_shares. If using Vault HSM with auto-unsealing, this value must be the same as
            secret_shares, or omitted, depending on the version of Vault and the seal type.
        :param pgp_keys: List of PGP public keys used to encrypt the output unseal keys.
            Ordering is preserved. The keys must be base64-encoded from their original binary representation.
            The size of this array must be the same as secret_shares.
        :param root_token_pgp_key: Specifies a PGP public key used to encrypt the initial root token. The
            key must be base64-encoded from its original binary representation.
        :param stored_shares: <enterprise only> Specifies the number of shares that should be encrypted by the HSM and
            stored for auto-unsealing. Currently, must be the same as secret_shares.
        :param recovery_shares: <enterprise only> Specifies the number of shares to split the recovery key into.
        :param recovery_threshold: <enterprise only> Specifies the number of shares required to reconstruct the recovery
            key. This must be less than or equal to recovery_shares.
        :param recovery_pgp_keys: <enterprise only> Specifies an array of PGP public keys used to encrypt the output
            recovery keys. Ordering is preserved. The keys must be base64-encoded from their original binary
            representation. The size of this array must be the same as recovery_shares.
        :return: The VaultxResponse of the request.
        """

        params: dict = {
            "secret_shares": secret_shares,
            "secret_threshold": secret_threshold,
            "root_token_pgp_key": root_token_pgp_key,
        }

        if pgp_keys is not None and secret_shares is not None:
            if len(pgp_keys) != secret_shares:
                raise VaultxError("length of pgp_keys list argument must equal secret_shares value")
            params["pgp_keys"] = pgp_keys

        if stored_shares is not None and secret_shares is not None:
            if stored_shares != secret_shares:
                raise VaultxError("value for stored_shares argument must equal secret_shares argument")
            params["stored_shares"] = stored_shares

        if recovery_shares is not None:
            params["recovery_shares"] = recovery_shares

            if recovery_threshold is not None:
                if recovery_threshold > recovery_shares:
                    raise VaultxError(
                        "value for recovery_threshold argument must be less than or equal to recovery_shares argument"
                    )
                params["recovery_threshold"] = recovery_threshold

            if recovery_pgp_keys is not None:
                if len(recovery_pgp_keys) != recovery_shares:
                    raise VaultxError("length of recovery_pgp_keys list argument must equal recovery_shares value")
                params["recovery_pgp_keys"] = recovery_pgp_keys

        api_path = "/v1/sys/init"
        return self._adapter.put(
            url=api_path,
            json=params,
        )
