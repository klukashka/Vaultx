from vaultx.api.secrets_engines import kv_v1, kv_v2
from vaultx.api.vault_api_base import VaultApiBase


class Kv(VaultApiBase):
    """
    Class containing methods for the key/value secrets_engines backend API routes.
    Reference: https://www.vaultproject.io/docs/secrets/kv/index.html
    """

    allowed_kv_versions = ["1", "2"]

    def __init__(self, adapter, default_kv_version: str = "2"):
        """
        Create a new Kv instance.

        :param adapter: Instance of :py:class:`vaultx.adapters.Adapter`; used for performing HTTP requests.
        :param default_kv_version: KV version number (e.g., '1') to use as the default
            when accessing attributes/methods under this class.
        """
        super().__init__(adapter=adapter)
        self._default_kv_version = default_kv_version

        self._kv_v1 = kv_v1.KvV1(adapter=self._adapter)
        self._kv_v2 = kv_v2.KvV2(adapter=self._adapter)

    @property
    def v1(self) -> kv_v1.KvV1:
        """
        Accessor for kv version 1 class / method.
            Provided via the :py:class:`vaultx.api.secrets_engines.kv_v1.KvV1` class.

        :return: This Kv instance's associated KvV1 instance.
        """
        return self._kv_v1

    @property
    def v2(self) -> kv_v2.KvV2:
        """
        Accessor for kv version 2 class / method.
            Provided via the :py:class:`vaultx.api.secrets_engines.kv_v2.KvV2` class.

        :return: This Kv instance's associated KvV2 instance.
        """
        return self._kv_v2

    @property
    def default_kv_version(self) -> str:
        return self._default_kv_version

    @default_kv_version.setter
    def default_kv_version(self, default_kv_version):
        if str(default_kv_version) not in self.allowed_kv_versions:
            error_message = 'Invalid "default_kv_version"; "{allowed}" allowed, "{provided}" provided'.format(
                allowed=",".join(self.allowed_kv_versions), provided=default_kv_version
            )
            raise ValueError(error_message)
        self._default_kv_version = str(default_kv_version)

    def __getattr__(self, item: str) -> VaultApiBase:
        """
        Overridden magic method used to direct method calls to the appropriate KV version's vaultx class.

        :param item: Name of the attribute/method being accessed
        :return: The selected secrets_engines class corresponding to this instance's default_kv_version setting
        """
        if item in ["_default_kv_version", "default_kv_version"]:
            raise AttributeError
        if self.default_kv_version == "1":
            return getattr(self._kv_v1, item)
        if self.default_kv_version == "2":
            return getattr(self._kv_v2, item)

        raise AttributeError
