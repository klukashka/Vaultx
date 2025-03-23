from typing import Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


DEFAULT_MOUNT_POINT = "okta"


class Okta(AsyncVaultApiBase):
    """
    Okta Auth Method (API).

    Reference: https://www.vaultproject.io/api/auth/okta/index.html
    """

    async def configure(
        self,
        org_name: str,
        api_token: Optional[str] = None,
        base_url: Optional[str] = None,
        ttl: Optional[str] = None,
        max_ttl: Optional[str] = None,
        bypass_okta_mfa: Optional[bool] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure the connection parameters for Okta.

        This path honors the distinction between the create and update capabilities inside ACL policies.

        Supported methods:
            POST: /auth/{mount_point}/config. Produces: 204 (empty body)

        :param org_name: Name of the organization to be used in the Okta API.
        :param api_token: Okta API token. This is required to query Okta for user group membership. If this is not
            supplied only locally configured groups will be enabled.
        :param base_url:  If set, will be used as the base domain for API requests.  Examples are okta.com,
            oktapreview.com, and okta-emea.com.
        :param ttl: Duration after which authentication will be expired.
        :param max_ttl: Maximum duration after which authentication will be expired.
        :param bypass_okta_mfa: Whether to bypass an Okta MFA request. Useful if using one of Vault's built-in MFA
            mechanisms, but this will also cause certain other statuses to be ignored, such as PASSWORD_EXPIRED.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = {
            "org_name": org_name,
        }
        params.update(
            utils.remove_nones(
                {
                    "api_token": api_token,
                    "base_url": base_url,
                    "ttl": ttl,
                    "max_ttl": max_ttl,
                    "bypass_okta_mfa": bypass_okta_mfa,
                }
            )
        )
        api_path = f"/v1/auth/{mount_point}/config"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the Okta configuration.

        Supported methods:
            GET: /auth/{mount_point}/config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_users(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List the users configured in the Okta method.

        Supported methods:
            LIST: /auth/{mount_point}/users. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/users"
        return await self._adapter.list(
            url=api_path,
        )

    async def register_user(
        self,
        username: str,
        groups: Optional[list[str]] = None,
        policies: Optional[list[str]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Register a new user and maps a set of policies to it.

        Supported methods:
            POST: /auth/{mount_point}/users/{username}. Produces: 204 (empty body)

        :param username: Name of the user.
        :param groups: List or comma-separated string of groups associated with the user.
        :param policies: List or comma-separated string of policies associated with the user.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = {
            "username": username,
        }
        params.update(
            utils.remove_nones(
                {
                    "groups": groups,
                    "policies": policies,
                }
            )
        )
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_user(self, username: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the properties of an existing username.

        Supported methods:
            GET: /auth/{mount_point}/users/{username}. Produces: 200 application/json

        :param username: Username for this user.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        params = {
            "username": username,
        }
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return await self._adapter.get(
            url=api_path,
            json=params,
        )

    async def delete_user(self, username: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an existing username from the method.

        Supported methods:
            DELETE: /auth/{mount_point}/users/{username}. Produces: 204 (empty body)

        :param username: Username for this user.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = {
            "username": username,
        }
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return await self._adapter.delete(
            url=api_path,
            json=params,
        )

    async def list_groups(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List the groups configured in the Okta method.

        Supported methods:
            LIST: /auth/{mount_point}/groups. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/groups"
        return await self._adapter.list(
            url=api_path,
        )

    async def register_group(
        self, name: str, policies: Optional[list[str]] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Register a new group and maps a set of policies to it.

        Supported methods:
            POST: /auth/{mount_point}/groups/{name}. Produces: 204 (empty body)

        :param name: The name of the group.
        :param policies: The list or comma-separated string of policies associated with the group.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = utils.remove_nones(
            {
                "policies": policies,
            }
        )
        api_path = f"/v1/auth/{mount_point}/groups/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_group(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the properties of an existing group.

        Supported methods:
            GET: /auth/{mount_point}/groups/{name}. Produces: 200 application/json

        :param name: The name for the group.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/groups/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def delete_group(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an existing group from the method.

        Supported methods:
            DELETE: /auth/{mount_point}/groups/{name}. Produces: 204 (empty body)

        :param name: The name for the group.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = {
            "name": name,
        }
        api_path = f"/v1/auth/{mount_point}/groups/{name}"
        return await self._adapter.delete(
            url=api_path,
            json=params,
        )

    async def login(
        self, username: str, password: str, use_token: bool = True, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Login with the username and password.

        Supported methods:
            POST: /auth/{mount_point}/login/{username}. Produces: 200 application/json

        :param username: Username for this user.
        :param password: Password for the authenticating user.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.Adapter` instance under the _adapter Client attribute.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the login request.
        """
        params = {
            "username": username,
            "password": password,
        }
        api_path = f"/v1/auth/{mount_point}/login/{username}"
        return await self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )
