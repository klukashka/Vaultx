from typing import Optional

from vaultx import exceptions, utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase


DEFAULT_MOUNT_POINT = "radius"


class Radius(VaultApiBase):
    """
    RADIUS Auth Method (API).

    Reference: https://www.vaultproject.io/docs/auth/radius.html
    """

    def configure(
        self,
        host: str,
        secret: str,
        port: Optional[int] = None,
        unregistered_user_policies: Optional[list[str]] = None,
        dial_timeout: Optional[int] = None,
        nas_port: Optional[int] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure the RADIUS auth method.

        Supported methods:
            POST: /auth/{mount_point}/config. Produces: 204 (empty body)

        :param host: The RADIUS server to connect to. Examples: radius.myorg.com, 127.0.0.1
        :param secret: The RADIUS shared secret.
        :param port: The UDP port where the RADIUS server is listening on. Defaults is 1812.
        :param unregistered_user_policies: A comma-separated list of policies to be granted to unregistered users.
        :param dial_timeout: Number of second to wait for a backend connection before timing out. Default is 10.
        :param nas_port: The NAS-Port attribute of the RADIUS request. Defaults is 10.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the configure request.
        """
        params = {
            "host": host,
            "secret": secret,
        }
        params.update(
            utils.remove_nones(
                {
                    "port": port,
                    "dial_timeout": dial_timeout,
                    "nas_port": nas_port,
                }
            )
        )
        # Fill out params dictionary with any optional parameters provided
        if unregistered_user_policies is not None:
            if not isinstance(unregistered_user_policies, list):
                error_msg = (
                    f'"unregistered_user_policies" argument must be an instance of list or None, '
                    f'"{type(unregistered_user_policies)}" provided.'
                )
                raise exceptions.VaultxError(error_msg)

            params["unregistered_user_policies"] = ",".join(unregistered_user_policies)

        api_path = f"/v1/auth/{mount_point}/config"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_configuration(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Retrieve the RADIUS configuration for the auth method.

        Supported methods:
            GET: /auth/{mount_point}/config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultResponse of the read_configuration request.
        """
        api_path = f"/v1/auth/{mount_point}/config"
        return self._adapter.get(
            url=api_path,
        )

    def register_user(
        self, username: str, policies: Optional[list[str]] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Create or update RADIUS user with a set of policies.

        Supported methods:
            POST: /auth/{mount_point}/users/{username}. Produces: 204 (empty body)

        :param username: Username for this RADIUS user.
        :param policies: List of policies associated with the user. This parameter is transformed to a comma-delimited
            string before being passed to Vault.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the register_user request.
        """
        if policies is not None and not isinstance(policies, list):
            error_msg = f'"policies" argument must be an instance of list or None, "{type(policies)}" provided.'
            raise exceptions.VaultxError(error_msg)

        params = {}
        if policies is not None:
            params["policies"] = ",".join(policies)
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def list_users(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List existing users in the method.

        Supported methods:
            LIST: /auth/{mount_point}/users. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the list_users request.
        """
        api_path = f"/v1/auth/{mount_point}/users"
        return self._adapter.list(
            url=api_path,
        )

    def read_user(self, username: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read policies associated with a RADIUS user.

        Supported methods:
            GET: /auth/{mount_point}/users/{username}. Produces: 200 application/json

        :param username: The username of the RADIUS user
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_user request.
        """
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return self._adapter.get(
            url=api_path,
        )

    def delete_user(self, username: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete a RADIUS user and policy association.

        Supported methods:
            DELETE: /auth/{mount_point}/users/{username}. Produces: 204 (empty body)

        :param username: The username of the RADIUS user
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the delete_user request.
        """
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return self._adapter.delete(
            url=api_path,
        )

    def login(
        self, username: str, password: str, use_token: bool = True, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Log in with RADIUS credentials.

        Supported methods:
            POST: /auth/{mount_point}/login/{username}. Produces: 200 application/json

        :param username: The username of the RADIUS user
        :param password: The password for the RADIUS user
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.Adapter` instance under the _adapter Client attribute.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the login_with_user request.
        """
        params = {
            "password": password,
        }
        api_path = f"/v1/auth/{mount_point}/login/{username}"
        return self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )
