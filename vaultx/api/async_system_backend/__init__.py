"""Collection of Vault system backend API endpoint classes."""

import typing as tp

from vaultx import exceptions
from vaultx.adapters import AsyncAdapter
from vaultx.api.async_system_backend.audit import Audit
from vaultx.api.async_system_backend.auth import Auth
from vaultx.api.async_system_backend.capabilities import Capabilities
from vaultx.api.async_system_backend.health import Health
from vaultx.api.async_system_backend.init import Init
from vaultx.api.async_system_backend.key import Key
from vaultx.api.async_system_backend.leader import Leader
from vaultx.api.async_system_backend.lease import Lease
from vaultx.api.async_system_backend.mount import Mount
from vaultx.api.async_system_backend.namespace import Namespace
from vaultx.api.async_system_backend.policies import Policies
from vaultx.api.async_system_backend.policy import Policy
from vaultx.api.async_system_backend.quota import Quota
from vaultx.api.async_system_backend.raft import Raft
from vaultx.api.async_system_backend.seal import Seal
from vaultx.api.async_system_backend.wrapping import Wrapping
from vaultx.api.vault_api_base import AsyncVaultApiBase


__all__ = (
    "Audit",
    "Auth",
    "Capabilities",
    "Health",
    "Init",
    "Key",
    "Leader",
    "Lease",
    "Mount",
    "Namespace",
    "Policies",
    "Policy",
    "Quota",
    "Raft",
    "Seal",
    "AsyncSystemBackend",
    "Wrapping",
    "AsyncVaultApiBase",
)


@exceptions.handle_unknown_exception
class AsyncSystemBackend(
    Audit,
    Auth,
    Capabilities,
    Health,
    Init,
    Key,
    Leader,
    Lease,
    Mount,
    Namespace,
    Policies,
    Policy,
    Quota,
    Raft,
    Seal,
    Wrapping,
):
    _implemented_classes: tp.Final[dict] = {
        "_audit": Audit,
        "_auth": Auth,
        "_capabilities": Capabilities,
        "_health": Health,
        "_init": Init,
        "_key": Key,
        "_leader": Leader,
        "_lease": Lease,
        "_mount": Mount,
        "_namespace": Namespace,
        "_policies": Policies,
        "_policy": Policy,
        "_quota": Quota,
        "_raft": Raft,
        "_seal": Seal,
        "_wrapping": Wrapping,
    }

    def __init__(self, adapter: AsyncAdapter) -> None:
        for attr_name, _class in self._implemented_classes.items():
            setattr(self, attr_name, _class(adapter=adapter))
        super().__init__(adapter=adapter)

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
    def adapter(self) -> AsyncAdapter:
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
