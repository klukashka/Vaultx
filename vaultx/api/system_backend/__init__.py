"""Collection of Vault system backend API endpoint classes."""

from vaultx.api.system_backend.audit import Audit
from vaultx.api.system_backend.auth import Auth
from vaultx.api.system_backend.capabilities import Capabilities
from vaultx.api.system_backend.health import Health
from vaultx.api.system_backend.init import Init
from vaultx.api.system_backend.key import Key
from vaultx.api.system_backend.leader import Leader
from vaultx.api.system_backend.lease import Lease
from vaultx.api.system_backend.mount import Mount
from vaultx.api.system_backend.namespace import Namespace
from vaultx.api.system_backend.policies import Policies
from vaultx.api.system_backend.policy import Policy
from vaultx.api.system_backend.quota import Quota
from vaultx.api.system_backend.raft import Raft
from vaultx.api.system_backend.seal import Seal
from vaultx.api.system_backend.system_backend_mixin import SystemBackendMixin
from vaultx.api.system_backend.wrapping import Wrapping
from vaultx.api.vault_api_category import VaultApiCategory


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
    "SystemBackend",
    "SystemBackendMixin",
    "Wrapping",
)


class SystemBackend(
    VaultApiCategory,
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
    implemented_classes = [
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
    ]
    unimplemented_classes = []
