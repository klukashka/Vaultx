from typing import Any, Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


DEFAULT_MOUNT_POINT = "userpass"


class Userpass(AsyncVaultApiBase):
    """
    Userpass Async Auth Method (API).
    Reference: https://www.vaultproject.io/api/auth/userpass/index.html
    """

    async def create_or_update_user(
        self,
        username: str,
        password: Optional[str] = None,
        policies: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        **kwargs: dict[Any, Any],
    ) -> VaultxResponse:
        """
        Create/update user in userpass.

        Supported methods:
            POST: /auth/{mount_point}/users/{username}. Produces: 204 (empty body)

        :param username: The username for the user.
        :param password: The password for the user. Only required when creating the user.
        :param policies: The list of policies to be set on username created.
        :param mount_point: The "path" the method/backend was mounted on.
        :param kwargs: Additional arguments to pass along with the corresponding request to Vault.
        """
        params = utils.remove_nones({"password": password, "policies": policies})
        params.update(kwargs)

        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def list_user(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List existing users that have been created in the auth method

        Supported methods:
            LIST: /auth/{mount_point}/users. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        """
        api_path = f"/v1/auth/{mount_point}/users"
        return await self._adapter.list(
            url=api_path,
        )

    async def read_user(self, username: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read user in the auth method.

        Supported methods:
            GET: /auth/{mount_point}/users/{username}. Produces: 200 application/json

        :param username: The username for the user.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_group request.
        """
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return await self._adapter.get(
            url=api_path,
        )

    async def delete_user(self, username: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete user in the auth method.

        Supported methods:
            GET: /auth/{mount_point}/users/{username}. Produces: 200 application/json

        :param username: The username for the user.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_group request.
        """
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def update_password_on_user(
        self, username: str, password: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        update password for the user in userpass.

        Supported methods:
            POST: /auth/{mount_point}/users/{username}/password. Produces: 204 (empty body)

        :param username: The username for the user.
        :param password: The password for the user. Only required when creating the user.
        :param mount_point: The "path" the method/backend was mounted on.
        """
        params = {"password": password}
        api_path = f"/v1/auth/{mount_point}/users/{username}/password"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def login(
        self, username: str, password: str, use_token: bool = True, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Log in with USERPASS credentials.

        Supported methods:
            POST: /auth/{mount_point}/login/{username}. Produces: 200 application/json

        :param username: The username for the user.
        :param password: The password for the user. Only required when creating the user.
        :param use_token: Whether to use a token or not
        :param mount_point: The "path" the method/backend was mounted on.
        """
        params = {"password": password}
        api_path = f"/v1/auth/{mount_point}/login/{username}"
        return await self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )
