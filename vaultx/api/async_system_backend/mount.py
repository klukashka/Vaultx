from typing import Any, Optional

from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase
from vaultx.exceptions import VaultxError


class Mount(AsyncVaultApiBase):
    async def list_mounted_secrets_engines(self) -> VaultxResponse:
        """
        List all the mounted secrets engines.

        Supported methods:
            POST: /sys/mounts. Produces: 200 application/json

        :return: VaultxResponse of the request.
        """
        return await self._adapter.get("/v1/sys/mounts")

    async def retrieve_mount_option(
        self, mount_point: str, option_name: str, default_value: Optional[str] = None
    ) -> Any:
        """
        Retrieve a specific option for the secrets engine mounted under the path specified.
        If no matching option (or no options at all) are discovered, a default value is returned.

        :param mount_point: The path the relevant secrets engine is mounted under.
        :param option_name: Specifies the name of the option to be retrieved.
        :param default_value: The value returned if no matching option (or no options at all) are discovered.
        :return: The value for the specified secrets engine's named option.
        """
        secrets_engine_path = f"{mount_point}/"
        listed_engines = await self.list_mounted_secrets_engines()
        if isinstance(listed_engines, dict):
            secrets_engines_list = listed_engines["data"]
        else:
            raise VaultxError("Unexpected return of non-json response")
        mount_options = secrets_engines_list[secrets_engine_path].get("options")
        if mount_options is None:
            return default_value

        return mount_options.get(option_name, default_value)

    async def enable_secrets_engine(
        self,
        backend_type: str,
        path: Optional[str] = None,
        description: Optional[str] = None,
        config: Optional[dict[str, Any]] = None,
        plugin_name: Optional[str] = None,
        options: Optional[dict[str, None]] = None,
        local: bool = False,
        seal_wrap: bool = False,
        **kwargs,
    ) -> VaultxResponse:
        """
        Enable a new secrets engine at the given path.

        Supported methods:
            POST: /sys/mounts/{path}. Produces: 204 (empty body)

        :param backend_type: The name of the backend type, such as "github" or "token".
        :param path: The path to mount the method on. If not provided, defaults to the value of the "backend_type"
            argument.
        :param description: A human-friendly description of the mount.
        :param config: Configuration options for this mount. These are the possible values:

            * **default_lease_ttl**: The default lease duration, specified as a string duration like "5s" or "30m".
            * **max_lease_ttl**: The maximum lease duration, specified as a string duration like "5s" or "30m".
            * **force_no_cache**: Disable caching.
            * **plugin_name**: The name of the plugin in the plugin catalog to use.
            * **audit_non_hmac_request_keys**: Comma-separated list of keys that will not be HMAC'd by audit devices in
              the request data object.
            * **audit_non_hmac_response_keys**: Comma-separated list of keys that will not be HMAC'd by audit devices in
              the response data object.
            * **listing_visibility**: Specifies whether to show this mount in the UI-specific listing endpoint.
                ("unauth" or "hidden")
            * **passthrough_request_headers**: Comma-separated list of headers to whitelist and pass from the request to
              the backend.
        :param options: Specifies mount type specific options that are passed to the backend.

            * **version**: <KV> The version of the KV to mount. Set to "2" for mount KV v2.
        :param plugin_name: Specifies the name of the plugin to use based from the name in the plugin catalog.
            Applies only to plugin backends.
        :param local: <Vault enterprise only> Specifies if the auth method is a local only. Local auth methods are not
            replicated nor (if a secondary) removed by replication.
        :param seal_wrap: <Vault enterprise only> Enable seal wrapping for the mount.
        :param kwargs: All dicts are accepted and passed to vault. See your specific secret engine for details on which
            extra key-word arguments you might want to pass.
        :return: The response of the request.
        """
        if path is None:
            path = backend_type

        params = {
            "type": backend_type,
            "description": description,
            "config": config,
            "options": options,
            "plugin_name": plugin_name,
            "local": local,
            "seal_wrap": seal_wrap,
        }

        params.update(kwargs)

        api_path = f"/v1/sys/mounts/{path}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def disable_secrets_engine(self, path: str) -> VaultxResponse:
        """
        Disable the mount point specified by the provided path.

        Supported methods:
            DELETE: /sys/mounts/{path}. Produces: 204 (empty body)

        :param path: Specifies the path where the secrets engine will be mounted. This is specified as part of the URL.
        :return: The response of the request.
        """
        api_path = f"/v1/sys/mounts/{path}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def read_mount_configuration(self, path: str) -> VaultxResponse:
        """
        Read the given mount's configuration.
        Unlike the mounts endpoint, this will return the current time in seconds for each TTL, which may be the system
        default or a mount-specific value.

        Supported methods:
            GET: /sys/mounts/{path}/tune. Produces: 200 application/json

        :param path: Specifies the path where the secrets engine will be mounted. This is specified as part of the URL.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/sys/mounts/{path}/tune"
        return await self._adapter.get(
            url=api_path,
        )

    async def tune_mount_configuration(
        self,
        path: str,
        default_lease_ttl: Optional[int] = None,
        max_lease_ttl: Optional[int] = None,
        description: Optional[str] = None,
        audit_non_hmac_request_keys: Optional[list[str]] = None,
        audit_non_hmac_response_keys: Optional[str] = None,
        listing_visibility: Optional[str] = None,
        passthrough_request_headers: Optional[str] = None,
        options=None,
        force_no_cache: Optional[bool] = None,
        **kwargs,
    ):
        """
        Tune configuration parameters for a given mount point.

        Supported methods:
            POST: /sys/mounts/{path}/tune. Produces: 204 (empty body)

        :param path: Specifies the path where the secrets engine will be mounted. This is specified as part of the URL.
        :param description: Specifies the description of the mount. This overrides the current stored value, if any.
        :param default_lease_ttl: Default time-to-live. This overrides the global default. A value of 0 is equivalent to
            the system default TTL
        :param max_lease_ttl: Maximum time-to-live. This overrides the global default. A value of 0 are equivalent and
            set to the system max TTL.
        :param audit_non_hmac_request_keys: Specifies the comma-separated list of keys that will not be HMAC'd by audit
            devices in the request data object.
        :param audit_non_hmac_response_keys: Specifies the comma-separated list of keys that will not be HMAC'd by audit
            devices in the response data object.
        :param listing_visibility: Specifies whether to show this mount in the UI-specific listing endpoint. Valid
            values are "unauth" or "".
        :param passthrough_request_headers: Comma-separated list of headers to whitelist and pass from the request
            to the backend.
        :param options: Specifies mount type specific options that are passed to the backend.

            * **version**: <KV> The version of the KV to mount. Set to "2" for mount KV v2.
        :type options: dict
        :param force_no_cache: Disable caching.
        :param kwargs: All dicts are accepted and passed to vault. See your specific secret engine for details on which
            extra key-word arguments you might want to pass.
        :type kwargs: dict
        :return: The response from the request.
        :rtype: request.Response
        """
        # All parameters are optional for this method. Until/unless we include input validation, we simply loop over the
        # parameters and add which parameters are set.
        optional_parameters = [
            "default_lease_ttl",
            "max_lease_ttl",
            "description",
            "audit_non_hmac_request_keys",
            "audit_non_hmac_response_keys",
            "listing_visibility",
            "passthrough_request_headers",
            "force_no_cache",
            "options",
        ]
        params = {}
        for optional_parameter in optional_parameters:
            local_parameter = locals().get(optional_parameter)
            if local_parameter is not None:
                params[optional_parameter] = local_parameter

        params.update(kwargs)

        api_path = f"/v1/sys/mounts/{path}/tune"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def move_backend(self, from_path: str, to_path: str) -> VaultxResponse:
        """
        Move an already-mounted backend to a new mount point.

        Supported methods:
            POST: /sys/remount. Produces: 204 (empty body)

        :param from_path: Specifies the previous mount point.
        :param to_path: Specifies the new destination mount point.
        :return: The response of the request.
        """
        params = {
            "from": from_path,
            "to": to_path,
        }
        api_path = "/v1/sys/remount"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )
