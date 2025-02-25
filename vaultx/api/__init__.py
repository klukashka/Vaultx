"""Collection of Vault API endpoint classes."""

from vaultx.api.auth_methods import AuthMethods
from vaultx.api.secrets_engines import SecretsEngines
from vaultx.api.system_backend import SystemBackend
from vaultx.api.vault_api_base import VaultApiBase


__all__ = (
    "AuthMethods",
    "SecretsEngines",
    "SystemBackend",
    "VaultApiBase",
)
