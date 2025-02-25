from vaultx.adapters import Adapter


class VaultApiBase:
    """Base class for API endpoints."""

    def __init__(self, adapter: Adapter) -> None:
        """
        Default api class constructor.
        :param adapter: Instance of Adapter; used for performing HTTP requests.
        """
        self._adapter = adapter
