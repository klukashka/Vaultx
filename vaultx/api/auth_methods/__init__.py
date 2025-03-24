"""Collection of classes for various Vault auth methods."""

import typing as tp

from vaultx import exceptions
from vaultx.adapters import Adapter
from vaultx.api.auth_methods.approle import AppRole
from vaultx.api.auth_methods.aws import Aws
from vaultx.api.auth_methods.azure import Azure
from vaultx.api.auth_methods.cert import Cert
from vaultx.api.auth_methods.gcp import Gcp
from vaultx.api.auth_methods.github import Github
from vaultx.api.auth_methods.jwt import Jwt
from vaultx.api.auth_methods.kubernetes import Kubernetes
from vaultx.api.auth_methods.ldap import Ldap
from vaultx.api.auth_methods.legacy_mfa import LegacyMfa
from vaultx.api.auth_methods.oidc import Oidc
from vaultx.api.auth_methods.okta import Okta
from vaultx.api.auth_methods.radius import Radius
from vaultx.api.auth_methods.token import Token
from vaultx.api.auth_methods.userpass import Userpass
from vaultx.api.vault_api_base import VaultApiBase


__all__ = (
    "AuthMethods",
    "AppRole",
    "Aws",
    "Azure",
    "Cert",
    "Gcp",
    "Github",
    "Jwt",
    "Kubernetes",
    "Ldap",
    "LegacyMfa",
    "Oidc",
    "Okta",
    "Radius",
    "Userpass",
    "Token",
)


@exceptions.handle_unknown_exception
class AuthMethods(VaultApiBase):
    """Auth Methods."""

    _implemented_classes: tp.Final[dict] = {
        "_approle": AppRole,
        "_aws": Aws,
        "_azure": Azure,
        "_cert": Cert,
        "_gcp": Gcp,
        "_github": Github,
        "_jwt": Jwt,
        "_kubernetes": Kubernetes,
        "_ldap": Ldap,
        "_legacy_mfa": LegacyMfa,
        "_oidc": Oidc,
        "_okta": Okta,
        "_radius": Radius,
        "_userpass": Userpass,
        "_token": Token,
    }

    def __init__(self, adapter: Adapter) -> None:
        for attr_name, _class in self._implemented_classes.items():
            setattr(self, attr_name, _class(adapter=adapter))
        super().__init__(adapter)

    def __getattr__(self, item: str):
        """
        Get an instance of a class instance in this category where available.

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
