from typing import Optional

from vaultx import exceptions
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase


SUPPORTED_MFA_TYPES = ["duo"]
SUPPORTED_AUTH_METHODS = ["ldap", "okta", "radius", "userpass"]


class LegacyMfa(VaultApiBase):
    """
    Multi-factor authentication Auth Method (API).

    .. warning::
        This class's methods correspond to a legacy / unsupported set of Vault API routes. Please see the reference link
        for additional context.

    Reference: https://developer.hashicorp.com/vault/docs/v1.10.x/auth/mfa
    """

    def configure(self, mount_point: str, mfa_type: str = "duo", force: bool = False) -> VaultxResponse:
        """
        Configure MFA for a supported method.

        This endpoint allows you to turn on multi-factor authentication with a given backend.
        Currently only Duo is supported.

        Supported methods:
            POST: /auth/{mount_point}/mfa_config. Produces: 204 (empty body)

        :param mount_point: The "path" the method/backend was mounted on.
        :param mfa_type: Enables MFA with given backend (available: duo)
        :param force: If `True`, make the `mfa_config` request regardless of circumstance. If `False` (the default),
            verify the provided `mount_point` is available and one of the types of methods supported by this feature.
        :return: The response of the configure MFA request.
        """
        if mfa_type != "duo" and not force:
            # The situation described via this exception is not likely to change in the future.
            # However, we provided that flexibility here just in case.
            mfa_types = ",".join(SUPPORTED_MFA_TYPES)
            raise exceptions.VaultxError(
                f'Unsupported mfa_type argument provided "{mfa_type}", supported types: "{mfa_types}"'
            )
        params = {
            "type": mfa_type,
        }

        api_path = f"/v1/auth/{mount_point}/mfa_config"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_configuration(self, mount_point: str) -> VaultxResponse:
        """
        Read the MFA configuration.

        Supported methods:
            GET: /auth/{mount_point}/mfa_config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_configuration request.
        """
        api_path = f"/v1/auth/{mount_point}/mfa_config"
        return self._adapter.get(url=api_path)

    def configure_duo_access(
        self, mount_point: str, host: str, integration_key: str, secret_key: str
    ) -> VaultxResponse:
        """
        Configure the access keys and host for Duo API connections.

        To authenticate users with Duo, the backend needs to know what host to connect to and must authenticate with an
        integration key and secret key. This endpoint is used to configure that information.

        Supported methods:
            POST: /auth/{mount_point}/duo/access. Produces: 204 (empty body)

        :param mount_point: The "path" the method/backend was mounted on.
        :param host: Duo API host
        :param integration_key: Duo integration key
        :param secret_key: Duo secret key
        :return: The response of the `configure_duo_access` request.
        """
        params = {
            "host": host,
            "ikey": integration_key,
            "skey": secret_key,
        }
        api_path = f"/v1/auth/{mount_point}/duo/access"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def configure_duo_behavior(
        self,
        mount_point: str,
        push_info: Optional[str] = None,
        user_agent: Optional[str] = None,
        username_format: str = "%s",
    ) -> VaultxResponse:
        """
        Configure Duo second factor behavior.

        This endpoint allows you to configure how the original auth method username maps to the Duo username by
        providing a template format string.

        Supported methods:
            POST: /auth/{mount_point}/duo/config. Produces: 204 (empty body)

        :param mount_point: The "path" the method/backend was mounted on.
        :param push_info: A string of URL-encoded key/value pairs that provides additional context about the
            authentication attempt in the Duo Mobile app
        :param user_agent: User agent to connect to Duo (default is empty string `""`)
        :param username_format: Format string given auth method username as argument to create Duo username
            (default `%s`)
        :return: The response of the `configure_duo_behavior` request.
        """
        params = {
            "username_format": username_format,
        }
        if push_info is not None:
            params["push_info"] = push_info
        if user_agent is not None:
            params["user_agent"] = user_agent
        api_path = f"/v1/auth/{mount_point}/duo/config"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_duo_behavior_configuration(self, mount_point: str) -> VaultxResponse:
        """
        Read the Duo second factor behavior configuration.

        Supported methods:
            GET: /auth/{mount_point}/duo/config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the `read_duo_behavior_configuration` request.
        """
        api_path = f"/v1/auth/{mount_point}/duo/config"
        return self._adapter.get(url=api_path)
