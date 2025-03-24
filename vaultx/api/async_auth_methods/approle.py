import json
from typing import Optional

from vaultx import exceptions, utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase
from vaultx.constants.approle import ALLOWED_TOKEN_TYPES, DEFAULT_MOUNT_POINT
from vaultx.utils import list_to_comma_delimited, validate_list_of_strings_param


class AppRole(AsyncVaultApiBase):
    """
    AppRole Async Auth Method (API).
    Reference: https://www.vaultproject.io/api-docs/auth/approle/index.html
    """

    async def create_or_update_approle(
        self,
        role_name: str,
        bind_secret_id: Optional[bool] = None,
        secret_id_bound_cidrs: Optional[list[str]] = None,
        secret_id_num_uses: Optional[int] = None,
        secret_id_ttl: Optional[str] = None,
        enable_local_secret_ids: Optional[bool] = None,
        token_ttl: Optional[str] = None,
        token_max_ttl: Optional[str] = None,
        token_policies: Optional[list[str]] = None,
        token_bound_cidrs: Optional[list[str]] = None,
        token_explicit_max_ttl: Optional[str] = None,
        token_no_default_policy: Optional[bool] = None,
        token_num_uses: Optional[int] = None,
        token_period: Optional[str] = None,
        token_type: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ):
        """
        Create/update approle.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}. Produces: 204 (empty body)

        :param role_name: The name for the approle.
        :param bind_secret_id: Require secret_id to be presented when logging in using this approle.
        :param secret_id_bound_cidrs: Blocks of IP addresses which can perform login operations.
        :param secret_id_num_uses: Number of times any secret_id can be used to fetch a token.
            A value of zero allows unlimited uses.
        :param secret_id_ttl: Duration after which a secret_id expires. This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :param enable_local_secret_ids: Secret IDs generated using role will be cluster local.
        :param token_ttl: Incremental lifetime for generated tokens. This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :param token_max_ttl: Maximum lifetime for generated tokens: This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :param token_policies: List of policies to encode onto generated tokens.
        :param token_bound_cidrs: Blocks of IP addresses which can authenticate successfully.
        :param token_explicit_max_ttl: If set, will encode an explicit max TTL onto the token. This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :param token_no_default_policy: Do not add the default policy to generated tokens, use only tokens
            specified in token_policies.
        :param token_num_uses: Maximum number of times a generated token may be used. A value of zero
            allows unlimited uses.
        :param token_period: The period, if any, to set on the token. This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :param token_type: The type of token that should be generated, can be "service", "batch", or "default".
        :param mount_point: The "path" the method/backend was mounted on.
        """
        list_of_strings_params = {
            "secret_id_bound_cidrs": secret_id_bound_cidrs,
            "token_policies": token_policies,
            "token_bound_cidrs": token_bound_cidrs,
        }

        if token_type is not None and token_type not in ALLOWED_TOKEN_TYPES:
            raise exceptions.VaultxError(
                f'unsupported token_type argument provided "{token_type}", '
                f'supported types: "{",".join(ALLOWED_TOKEN_TYPES)}"'
            )

        params = {}

        for param_name, param_argument in list_of_strings_params.items():
            validate_list_of_strings_param(
                param_name=param_name,
                param_arg=param_argument,
            )
            if param_argument is not None:
                params[param_name] = list_to_comma_delimited(param_argument)

        params.update(
            utils.remove_nones(
                {
                    "bind_secret_id": bind_secret_id,
                    "secret_id_num_uses": secret_id_num_uses,
                    "secret_id_ttl": secret_id_ttl,
                    "enable_local_secret_ids": enable_local_secret_ids,
                    "token_ttl": token_ttl,
                    "token_max_ttl": token_max_ttl,
                    "token_explicit_max_ttl": token_explicit_max_ttl,
                    "token_no_default_policy": token_no_default_policy,
                    "token_num_uses": token_num_uses,
                    "token_period": token_period,
                    "token_type": token_type,
                }
            )
        )

        api_path = f"/v1/auth/{mount_point}/role/{role_name}"
        return await self._adapter.post(url=api_path, json=params)

    async def list_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List existing roles created in the auth method.

        Supported methods:
            LIST: /auth/{mount_point}/role. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the list_roles request.
        """
        api_path = f"/v1/auth/{mount_point}/role"
        return await self._adapter.list(url=api_path)

    async def read_role(self, role_name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read role in the auth method.

        Supported methods:
            GET: /auth/{mount_point}/role/{role_name}. Produces: 200 application/json

        :param role_name: The name for the role.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_role request.
        """
        api_path = f"/v1/auth/{mount_point}/role/{role_name}"
        return await self._adapter.get(url=api_path)

    async def delete_role(self, role_name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete role in the auth method.

        Supported methods:
            DELETE: /auth/{mount_point}/role/{role_name}. Produces: 204 (empty body)

        :param role_name: The name for the role.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: response of the request
        """
        api_path = f"/v1/auth/{mount_point}/role/{role_name}"
        return await self._adapter.delete(url=api_path)

    async def read_role_id(self, role_name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the Role ID of a role in the auth method.

        Supported methods:
            GET: /auth/{mount_point}/role/{role_name}/role-id. Produces: 200 application/json

        :param role_name: The name for the role.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_role_id request.
        """
        api_path = f"/v1/auth/{mount_point}/role/{role_name}/role-id"
        return await self._adapter.get(url=api_path)

    async def update_role_id(
        self, role_name: str, role_id: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Update the Role ID of a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/role-id. Produces: 200 application/json

        :param role_name: The name for the role.
        :param role_id: New value for the Role ID.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_role_id request.
        """
        params = {"role_id": role_id}

        api_path = f"/v1/auth/{mount_point}/role/{role_name}/role-id"
        return await self._adapter.post(url=api_path, json=params)

    async def generate_secret_id(
        self,
        role_name: str,
        metadata: Optional[dict] = None,
        cidr_list: Optional[list] = None,
        token_bound_cidrs: Optional[list[str]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        wrap_ttl: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Generate and issue a new Secret ID on a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/secret-id. Produces: 200 application/json

        :param role_name: The name for the role.
        :param metadata: Metadata to be tied to the Secret ID.
        :param cidr_list: Blocks of IP addresses which can perform login operations.
        :param token_bound_cidrs: Blocks of IP addresses which can authenticate successfully.
        :param mount_point: The "path" the method/backend was mounted on.
        :param wrap_ttl: Returns the request as a response-wrapping token.
            Can be either an integer number of seconds or a string duration of
            seconds (`15s`), minutes (`20m`), or hours (`25h`).
        :return: The VaultxResponse of the read_role_id request.
        """
        if metadata is not None and not isinstance(metadata, dict):
            raise exceptions.VaultxError(
                f'unsupported metadata argument provided "{metadata}" ({type(metadata)}), required type: dict"'
            )

        params = {}
        if metadata:
            params = {"metadata": json.dumps(metadata)}

        list_of_strings_params = {
            "cidr_list": cidr_list,
            "token_bound_cidrs": token_bound_cidrs,
        }
        for param_name, param_argument in list_of_strings_params.items():
            validate_list_of_strings_param(
                param_name=param_name,
                param_arg=param_argument,
            )
            if param_argument is not None:
                params[param_name] = list_to_comma_delimited(param_argument)

        api_path = f"/v1/auth/{mount_point}/role/{role_name}/secret-id"
        return await self._adapter.post(url=api_path, json=params, wrap_ttl=wrap_ttl)

    async def create_custom_secret_id(
        self,
        role_name: str,
        secret_id: str,
        metadata: Optional[dict] = None,
        cidr_list: Optional[list[str]] = None,
        token_bound_cidrs: Optional[list[str]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        wrap_ttl: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Generate and issue a new Secret ID on a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/custom-secret-id. Produces: 200 application/json

        :param role_name: The name for the role.
        :param secret_id: The Secret ID to read.
        :param metadata: Metadata to be tied to the Secret ID.
        :param cidr_list: Blocks of IP addresses which can perform login operations.
        :param token_bound_cidrs: Blocks of IP addresses which can authenticate successfully.
        :param mount_point: The "path" the method/backend was mounted on.
        :param wrap_ttl: Returns the request as a response-wrapping token.
            Can be either an integer number of seconds or a string duration of
            seconds (`15s`), minutes (`20m`), or hours (`25h`).
        :return: The VaultxResponse of the read_role_id request.
        """
        if metadata is not None and not isinstance(metadata, dict):
            raise exceptions.VaultxError(
                'unsupported metadata argument provided "{metadata}" ({type(metadata)}), required type: dict"'
            )

        params = {"secret_id": secret_id}

        if metadata:
            params["metadata"] = json.dumps(metadata)

        list_of_strings_params = {
            "cidr_list": cidr_list,
            "token_bound_cidrs": token_bound_cidrs,
        }
        for param_name, param_argument in list_of_strings_params.items():
            validate_list_of_strings_param(
                param_name=param_name,
                param_arg=param_argument,
            )
            if param_argument is not None:
                params[param_name] = list_to_comma_delimited(param_argument)

        api_path = f"/v1/auth/{mount_point}/role/{role_name}/custom-secret-id"
        return await self._adapter.post(url=api_path, json=params, wrap_ttl=wrap_ttl)

    async def read_secret_id(
        self, role_name: str, secret_id: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Read the properties of a Secret ID for a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/secret-id/lookup. Produces: 200 application/json

        :param role_name: The name for the role
        :param secret_id: The Secret ID to read.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_role_id request.
        """
        params = {"secret_id": secret_id}
        api_path = f"/v1/auth/{mount_point}/role/{role_name}/secret-id/lookup"
        return await self._adapter.post(url=api_path, json=params)

    async def destroy_secret_id(
        self, role_name: str, secret_id: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Destroy a Secret ID for a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/secret-id/destroy. Produces 204 (empty body)

        :param role_name: The name for the role
        :param secret_id: The Secret ID to read.
        :param mount_point: The "path" the method/backend was mounted on.
        """
        params = {"secret_id": secret_id}
        api_path = f"/v1/auth/{mount_point}/role/{role_name}/secret-id/destroy"
        return await self._adapter.post(url=api_path, json=params)

    async def list_secret_id_accessors(self, role_name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List accessors of all issued Secret IDs for a role in the auth method.

        Supported methods:
            LIST: /auth/{mount_point}/role/{role_name}/secret-id. Produces: 200 application/json

        :param role_name: The name for the role
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_role_id request.
        """
        api_path = f"/v1/auth/{mount_point}/role/{role_name}/secret-id"
        return await self._adapter.list(url=api_path)

    async def read_secret_id_accessor(
        self, role_name: str, secret_id_accessor: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Read the properties of a Secret ID for a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/secret-id-accessor/lookup. Produces: 200 application/json

        :param role_name: The name for the role
        :param secret_id_accessor: The accessor for the Secret ID to read.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_role_id request.
        """
        params = {"secret_id_accessor": secret_id_accessor}
        api_path = f"/v1/auth/{mount_point}/role/{role_name}/secret-id-accessor/lookup"
        return await self._adapter.post(url=api_path, json=params)

    async def destroy_secret_id_accessor(
        self, role_name: str, secret_id_accessor: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Destroy a Secret ID for a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/secret-id-accessor/destroy. Produces: 204 (empty body)

        :param role_name: The name for the role
        :param secret_id_accessor: The accessor for the Secret ID to read.
        :param mount_point: The "path" the method/backend was mounted on.
        """
        params = {"secret_id_accessor": secret_id_accessor}
        api_path = f"/v1/auth/{mount_point}/role/{role_name}/secret-id-accessor/destroy"
        return await self._adapter.post(url=api_path, json=params)

    async def login(
        self, role_id: str, secret_id: Optional[str] = None, use_token: bool = True, mount_point=DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Login with APPROLE credentials.

        Supported methods:
            POST: /auth/{mount_point}/login. Produces: 200 application/json

        :param role_id: Role ID of the role.
        :param secret_id: Secret ID of the role.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the AsyncAdapter instance under the _adapter AsyncClient attribute.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the login request.
        """
        params = {"role_id": role_id, "secret_id": secret_id}
        api_path = f"/v1/auth/{mount_point}/login"
        return await self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )
