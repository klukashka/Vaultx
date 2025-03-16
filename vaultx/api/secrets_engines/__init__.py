"""Vault secrets engines endpoints"""

import typing as tp

from vaultx import exceptions
from vaultx.adapters import Adapter
from vaultx.api.secrets_engines.active_directory import ActiveDirectory
from vaultx.api.secrets_engines.aws import Aws
from vaultx.api.secrets_engines.azure import Azure
from vaultx.api.secrets_engines.consul import Consul
from vaultx.api.secrets_engines.database import Database
from vaultx.api.secrets_engines.gcp import Gcp
from vaultx.api.secrets_engines.identity import Identity
from vaultx.api.secrets_engines.kv import Kv
from vaultx.api.secrets_engines.kv_v1 import KvV1
from vaultx.api.secrets_engines.kv_v2 import KvV2
from vaultx.api.secrets_engines.ldap import Ldap
from vaultx.api.secrets_engines.pki import Pki
from vaultx.api.secrets_engines.rabbitmq import RabbitMQ
from vaultx.api.secrets_engines.ssh import Ssh
from vaultx.api.secrets_engines.transform import Transform
from vaultx.api.secrets_engines.transit import Transit
from vaultx.api.vault_api_base import VaultApiBase


__all__ = (
    "ActiveDirectory",
    "Aws",
    "Azure",
    "Consul",
    "Database",
    "Gcp",
    "Identity",
    "Kv",
    "KvV1",
    "KvV2",
    "Ldap",
    "Pki",
    "RabbitMQ",
    "Ssh",
    "Transform",
    "Transit",
    "SecretsEngines",
)


@exceptions.handle_unknown_exception
class SecretsEngines(VaultApiBase):
    """Secrets Engines."""

    _implemented_classes: tp.Final[dict] = {
        "_kv": Kv,
    }

    def __init__(self, adapter: Adapter) -> None:
        for attr_name, _class in self._implemented_classes.items():
            setattr(self, attr_name, _class(adapter=adapter))
        super().__init__(adapter)

    def __getattr__(self, item: str):
        """
        Get an instance of a class instance.

        :param item: Name of the class being requested.
        :return: The requested class instance where available.
        """
        item = f"_{item}"
        if item in self._implemented_classes:
            return getattr(self, item)
        raise AttributeError

    @property
    def adapter(self) -> Adapter:
        """
        Retrieve the adapter instance under the "_adapter" property in use by this class.

        :return: The adapter instance in use by this class.
        """
        return self._adapter

    @adapter.setter
    def adapter(self, adapter) -> None:
        """
        Set the adapter instance under the "_adapter" property in use by this class.
        Also set the adapter property for all implemented classes.

        :param adapter: New adapter instance to set for this class and all implemented classes.
        """
        self._adapter = adapter
        for implemented_class in self._implemented_classes:
            getattr(self, f"{implemented_class}").adapter = adapter
