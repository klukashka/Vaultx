from typing import Optional

from vaultx import exceptions, utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase
from vaultx.utils import list_to_comma_delimited, validate_list_of_strings_param


class Auth(VaultApiBase):
    def list_auth_methods(self) -> VaultxResponse:
        """
        List all enabled auth methods.

        Supported methods:
            GET: /sys/auth. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        api_path = "/v1/sys/auth"
        return self._adapter.get(
            url=api_path,
        )

    def enable_auth_method(
        self,
        method_type: str,
        description: Optional[str] = None,
        config: Optional[dict] = None,
        plugin_name: Optional[str] = None,
        local: bool = False,
        path: Optional[str] = None,
        **kwargs,
    ) -> VaultxResponse:
        """
        Enable a new auth method.

        After enabling, the auth method can be accessed and configured via the auth path specified as part of the URL.
        This auth path will be nested under the auth prefix.

        Supported methods:
            POST: /sys/auth/{path}. Produces: 204 (empty body)

        :param method_type: The name of the authentication method type, such as "github" or "token".
        :param description: A human-friendly description of the auth method.
        :param config: Configuration options for this auth method. These are the possible values:

            * **default_lease_ttl**: The default lease duration, specified as a string duration like "5s" or "30m".
            * **max_lease_ttl**: The maximum lease duration, specified as a string duration like "5s" or "30m".
            * **audit_non_hmac_request_keys**: Comma-separated list of keys that will not be HMAC'd by audit devices in
              the request data object.
            * **audit_non_hmac_response_keys**: Comma-separated list of keys that will not be HMAC'd by audit devices in
              the response data object.
            * **listing_visibility**: Specifies whether to show this mount in the UI-specific listing endpoint.
            * **passthrough_request_headers**: Comma-separated list of headers to whitelist and pass from the request to
              the backend.
        :param plugin_name: The name of the auth plugin to use based from the name in the plugin catalog. Applies only
            to plugin methods.
        :param local: <Vault enterprise only> Specifies if the auth method is a local only. Local auth methods are not
            replicated nor (if a secondary) removed by replication.
        :param path: The path to mount the method on. If not provided, defaults to the value of the "method_type"
            argument.
        :param kwargs: All dicts are accepted and passed to vault. See your specific secret engine for details on which
            extra key-word arguments you might want to pass.
        :return: The response of the request.
        """
        if path is None:
            path = method_type

        params = {
            "type": method_type,
        }
        params.update(
            utils.remove_nones(
                {
                    "description": description,
                    "config": config,
                    "plugin_name": plugin_name,
                    "local": local,
                }
            )
        )
        params.update(kwargs)
        api_path = f"/v1/sys/auth/{path}"
        return self._adapter.post(url=api_path, json=params)

    def disable_auth_method(self, path: str) -> VaultxResponse:
        """
        Disable the auth method at the given auth path.

        Supported methods:
            DELETE: /sys/auth/{path}. Produces: 204 (empty body)

        :param path: The path the method was mounted on. If not provided, defaults to the value of the "method_type"
            argument.
        :return: The response of the request.
        """
        api_path = f"/v1/sys/auth/{path}"
        return self._adapter.delete(
            url=api_path,
        )

    def read_auth_method_tuning(self, path: str) -> VaultxResponse:
        """
        Read the given auth path's configuration.

        This endpoint requires sudo capability on the final path, but the same functionality can be achieved without
        sudo via sys/mounts/auth/[auth-path]/tune.

        Supported methods:
            GET: /sys/auth/{path}/tune. Produces: 200 application/json

        :param path: The path the method was mounted on. If not provided, defaults to the value of the "method_type"
            argument.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/sys/auth/{path}/tune"
        return self._adapter.get(
            url=api_path,
        )

    def tune_auth_method(
        self,
        path: str,
        default_lease_ttl: Optional[int] = None,
        max_lease_ttl: Optional[int] = None,
        description: Optional[str] = None,
        audit_non_hmac_request_keys: Optional[list[str]] = None,
        audit_non_hmac_response_keys: Optional[list[str]] = None,
        listing_visibility: Optional[str] = None,
        passthrough_request_headers: Optional[list[str]] = None,
        **kwargs,
    ) -> VaultxResponse:
        """
        Tune configuration parameters for a given auth path.

        This endpoint requires sudo capability on the final path, but the same functionality can be achieved without
        sudo via sys/mounts/auth/[auth-path]/tune.

        Supported methods:
            POST: /sys/auth/{path}/tune. Produces: 204 (empty body)

        :param path: The path the method was mounted on. If not provided, defaults to the value of the "method_type"
            argument.
        :param default_lease_ttl: Specifies the default time-to-live. If set on a specific auth path, this overrides the
            global default.
        :param max_lease_ttl: The maximum time-to-live. If set on a specific auth path, this overrides the global
            default.
        :param description: Specifies the description of the mount. This overrides the current stored value, if any.
        :param audit_non_hmac_request_keys: Specifies the list of keys that will not be HMAC'd by audit devices in the
            request data object.
        :param audit_non_hmac_response_keys: Specifies the list of keys that will not be HMAC'd by audit devices in the
            response data object.
        :param listing_visibility: Specifies whether to show this mount in the UI-specific listing endpoint. Valid
            values are "unauth" or "".
        :param passthrough_request_headers: List of headers to whitelist and pass from the request to the backend.
        :param kwargs: All dicts are accepted and passed to vault. See your specific secret engine for details on which
            extra key-word arguments you might want to pass.
        :return: The response of the request.
        """

        if listing_visibility is not None and listing_visibility not in ["unauth", ""]:
            raise exceptions.VaultxError(
                f'invalid listing_visibility argument provided: "{listing_visibility}"; valid values: "unauth" or ""'
            )

        # All parameters are optional for this method. Until/unless we include input validation, we simply loop over the
        # parameters and add which parameters are set.
        optional_parameters = {
            "default_lease_ttl": {},
            "max_lease_ttl": {},
            "description": {},
            "audit_non_hmac_request_keys": {"comma_delimited_list": True},
            "audit_non_hmac_response_keys": {"comma_delimited_list": True},
            "listing_visibility": {},
            "passthrough_request_headers": {"comma_delimited_list": True},
        }
        params = {}
        for optional_parameter, parameter_specification in optional_parameters.items():
            argument = locals().get(optional_parameter)
            if argument is not None:
                if parameter_specification.get("comma_delimited_list"):
                    validate_list_of_strings_param(optional_parameter, argument)
                    params[optional_parameter] = list_to_comma_delimited(argument)
                else:
                    params[optional_parameter] = argument
        params.update(kwargs)
        api_path = f"/v1/sys/auth/{path}/tune"
        return self._adapter.post(
            url=api_path,
            json=params,
        )
