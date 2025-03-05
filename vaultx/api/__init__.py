"""Collection of Vault API endpoint classes."""

from vaultx.api.async_auth_methods import AsyncAuthMethods
from vaultx.api.async_secrets_engines import AsyncSecretsEngines
from vaultx.api.async_system_backend import AsyncSystemBackend
from vaultx.api.auth_methods import AuthMethods
from vaultx.api.secrets_engines import SecretsEngines
from vaultx.api.system_backend import SystemBackend
from vaultx.api.vault_api_base import AsyncVaultApiBase, VaultApiBase


__all__ = (
    "AuthMethods",
    "SecretsEngines",
    "SystemBackend",
    "AsyncAuthMethods",
    "AsyncSecretsEngines",
    "AsyncSystemBackend",
    "VaultApiBase",
    "AsyncVaultApiBase",
)
