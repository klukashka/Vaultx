"""Collection of classes for various Vault auth methods."""

import typing as tp

from vaultx import exceptions
from vaultx.adapters import Adapter
from vaultx.api.auth_methods.approle import AppRole
from vaultx.api.auth_methods.token import Token
from vaultx.api.auth_methods.userpass import Userpass
from vaultx.api.vault_api_base import VaultApiBase


__all__ = (
    "AuthMethods",
    "AppRole",
    "Userpass",
    "Token",
)


@exceptions.handle_unknown_exception
class AuthMethods(VaultApiBase):
    """Auth Methods."""

    _implemented_classes: tp.Final[dict] = {
        "_approle": AppRole,
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
