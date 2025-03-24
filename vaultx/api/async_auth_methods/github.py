from typing import Optional

from vaultx import exceptions, utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


DEFAULT_MOUNT_POINT = "github"


class Github(AsyncVaultApiBase):
    """
    GitHub Auth Method (API).

    Reference: https://www.vaultproject.io/api/auth/github/index.html
    """

    async def configure(
        self,
        organization: str,
        base_url: Optional[str] = None,
        ttl: Optional[str] = None,
        max_ttl: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure the connection parameters for GitHub.

        This path honors the distinction between the create and update capabilities inside ACL policies.

        Supported methods:
            POST: /auth/{mount_point}/config. Produces: 204 (empty body)

        :param organization: The organization users must be part of.
        :param base_url: The API endpoint to use. Useful if you are running GitHub Enterprise or an API-compatible
            authentication server.
        :param ttl: Duration after which authentication will be expired.
        :param max_ttl: Maximum duration after which authentication will
            be expired.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the configure_method request.
        """
        params = {
            "organization": organization,
        }
        params.update(
            utils.remove_nones(
                {
                    "base_url": base_url,
                    "ttl": ttl,
                    "max_ttl": max_ttl,
                }
            )
        )
        api_path = f"/v1/auth/{mount_point}/config"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_configuration(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the GitHub configuration.

        Supported methods:
            GET: /auth/{mount_point}/config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_configuration request.
        """
        api_path = f"/v1/auth/{mount_point}/config"
        return await self._adapter.get(url=api_path)

    async def map_team(
        self, team_name: str, policies: Optional[list[str]] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Map a list of policies to a team that exists in the configured GitHub organization.

        Supported methods:
            POST: /auth/{mount_point}/map/teams/{team_name}. Produces: 204 (empty body)

        :param team_name: GitHub team name in "slugified" format
        :param policies: Comma separated list of policies to assign
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the map_github_teams request.
        """
        # First, perform parameter validation.
        if policies is None:
            policies = []
        if not isinstance(policies, list) or not all(isinstance(p, str) for p in policies):
            raise exceptions.VaultxError(
                f'unsupported policies argument provided "{policies}" ({type(policies)}), required type: list[str]"'
            )
        # Then, perform request.
        params = {
            "value": ",".join(policies),
        }
        api_path = f"/v1/auth/{mount_point}/map/teams/{team_name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_team_mapping(self, team_name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the GitHub team policy mapping.

        Supported methods:
            GET: /auth/{mount_point}/map/teams/{team_name}. Produces: 200 application/json

        :param team_name: GitHub team name
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_team_mapping request.
        """
        api_path = f"/v1/auth/{mount_point}/map/teams/{team_name}"
        return await self._adapter.get(url=api_path)

    async def map_user(
        self, user_name: str, policies: Optional[list[str]] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Map a list of policies to a specific GitHub user exists in the configured organization.

        Supported methods:
            POST: /auth/{mount_point}/map/users/{user_name}. Produces: 204 (empty body)

        :param user_name: GitHub username
        :param policies: Comma separated list of policies to assign
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the map_github_users request.
        """
        # First, perform parameter validation.
        if policies is None:
            policies = []
        if not (isinstance(policies, list) and all(isinstance(p, str) for p in policies)):
            raise exceptions.VaultxError(
                f'unsupported policies argument provided "{policies}" ({type(policies)}), required type: list[str]"'
            )

        # Then, perform request.
        params = {
            "value": ",".join(policies),
        }
        api_path = f"/v1/auth/{mount_point}/map/users/{user_name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_user_mapping(self, user_name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the GitHub user policy mapping.

        Supported methods:
            GET: /auth/{mount_point}/map/users/{user_name}. Produces: 200 application/json

        :param user_name: GitHub username
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_user_mapping request.
        """
        api_path = f"/v1/auth/{mount_point}/map/users/{user_name}"
        return await self._adapter.get(url=api_path)

    async def login(self, token: str, use_token: bool = True, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Login using GitHub access token.

        Supported methods:
            POST: /auth/{mount_point}/login. Produces: 200 application/json

        :param token: GitHub personal API token.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.Adapter` instance under the _adapter Client attribute.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the login request.
        """
        params = {
            "token": token,
        }
        api_path = f"/v1/auth/{mount_point}/login"
        return await self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )
