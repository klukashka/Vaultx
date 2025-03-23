from typing import Optional, Union

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase
from vaultx.utils import (
    comma_delimited_to_list,
    validate_list_of_strings_param,
    validate_pem_format,
)


DEFAULT_MOUNT_POINT = "kubernetes"


class Kubernetes(AsyncVaultApiBase):
    """
    Kubernetes Auth Method (API).

    Reference: https://www.vaultproject.io/api/auth/kubernetes/index.html
    """

    async def configure(
        self,
        kubernetes_host: str,
        kubernetes_ca_cert: Optional[str] = None,
        token_reviewer_jwt: Optional[str] = None,
        pem_keys: Optional[list[str]] = None,
        issuer: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        disable_local_ca_jwt: bool = False,
    ) -> VaultxResponse:
        """
        Configure the connection parameters for Kubernetes.

        This path honors the distinction between the create and update capabilities inside ACL policies.

        Supported methods:
            POST: /auth/{mount_point}/config. Produces: 204 (empty body)

        :param kubernetes_host: Host must be a host string, a host:port pair, or a URL to the base of the
            Kubernetes API server. Example: https://k8s.example.com:443
        :param kubernetes_ca_cert: PEM encoded CA cert for use by the TLS client used to talk with the Kubernetes API.
            NOTE: Every line must end with a newline: \n
        :param token_reviewer_jwt: A service account JWT used to access the TokenReview API to validate other
            JWTs during login. If not set the JWT used for login will be used to access the API.
        :param pem_keys: Optional list of PEM-formatted public keys or certificates used to verify the signatures of
            Kubernetes service account JWTs. If a certificate is given, its public key will be extracted. Not every
            installation of Kubernetes exposes these keys.
        :param issuer: Optional JWT issuer.
        :param mount_point: The "path" the method/backend was mounted on.
        :param disable_local_ca_jwt: Disable defaulting to the local CA cert and service account JWT
        :return: The response of the configure_method request.
        """
        list_of_pem_params = {
            "kubernetes_ca_cert": kubernetes_ca_cert,
            "pem_keys": pem_keys,
        }
        for param_name, param_argument in list_of_pem_params.items():
            if param_argument is not None:
                validate_pem_format(
                    param_name=param_name,
                    param_argument=param_argument,
                )

        params = {
            "kubernetes_host": kubernetes_host,
            "disable_local_ca_jwt": disable_local_ca_jwt,
        }
        params.update(
            utils.remove_nones(
                {
                    "kubernetes_ca_cert": kubernetes_ca_cert,
                    "token_reviewer_jwt": token_reviewer_jwt,
                    "pem_keys": pem_keys,
                    "issuer": issuer,
                }
            )
        )
        api_path = f"/v1/auth/{mount_point}/config"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> dict:
        """
        Return the previously configured config, including credentials.

        Supported methods:
            GET: /auth/{mount_point}/config. Produces: 200 application/json

        :param mount_point: The "path" the kubernetes auth method was mounted on.
        :return: The data key from the JSON response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config"
        response = await self._adapter.get(
            url=api_path,
        )
        return response.value["data"]

    async def create_role(
        self,
        name: str,
        bound_service_account_names: list[str],
        bound_service_account_namespaces: list[str],
        ttl: Optional[Union[str, int]] = None,
        max_ttl: Optional[Union[str, int]] = None,
        period: Optional[Union[str, int]] = None,
        policies: Optional[Union[list[str], str]] = None,
        token_type: str = "",
        mount_point: str = DEFAULT_MOUNT_POINT,
        alias_name_source: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Create a role in the method.

        Registers a role in the auth method. Role types have specific entities that can perform login operations
        against this endpoint. Constraints specific to the role type must be set on the role. These are applied to
        the authenticated entities attempting to login.

        Supported methods:
            POST: /auth/{mount_point}/role/{name}. Produces: 204 (empty body)

        :param name: Name of the role.
        :param bound_service_account_names: List of service account names able to access this role. If set to "*"
            all names are allowed.
        :param bound_service_account_namespaces: List of namespaces allowed to access this role. If set to "*" all
            namespaces are allowed.
        :param ttl: The TTL period of tokens issued using this role in seconds.
        :param max_ttl: The maximum allowed lifetime of tokens issued in seconds using this role.
        :param period: If set, indicates that the token generated using this role should never expire. The token should
            be renewed within the duration specified by this value. At each renewal, the token's TTL will be set to the
            value of this parameter.
        :param policies: Policies to be set on tokens issued using this role.
        :param token_type: The type of token that should be generated. Can be service, batch, or default to use the
            mount's tuned default (which unless changed will be service tokens). For token store roles, there are two
            additional possibilities: default-service and default-batch which specify the type to return unless the
            client requests a different type at generation time.
        :param mount_point: The "path" the kubernetes auth method was mounted on.
        :param alias_name_source: Configures how identity aliases are generated.
            Valid choices are: serviceaccount_uid, serviceaccount_name.
        :return: The response of the request.
        """
        list_of_strings_params = {
            "bound_service_account_names": bound_service_account_names,
            "bound_service_account_namespaces": bound_service_account_namespaces,
            "policies": policies,
        }
        for param_name, param_argument in list_of_strings_params.items():
            validate_list_of_strings_param(
                param_name=param_name,
                param_arg=param_argument,
            )

        params: dict = {
            "bound_service_account_names": comma_delimited_to_list(bound_service_account_names),
            "bound_service_account_namespaces": comma_delimited_to_list(bound_service_account_namespaces),
        }
        if alias_name_source is not None:
            params["alias_name_source"] = alias_name_source

        params.update(
            utils.remove_nones(
                {
                    "ttl": ttl,
                    "max_ttl": max_ttl,
                    "period": period,
                }
            )
        )
        if policies is not None:
            params["policies"] = comma_delimited_to_list(policies)

        if token_type:
            params["token_type"] = token_type

        api_path = f"/v1/auth/{mount_point}/role/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> dict:
        """
        Return the previously registered role configuration.

        Supported methods:
            POST: /auth/{mount_point}/role/{name}. Produces: 200 application/json

        :param name: Name of the role.
        :param mount_point: The "path" the kubernetes auth method was mounted on.
        :return: The "data" key from the VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/role/{name}"
        response = await self._adapter.get(
            url=api_path,
        )
        return response.value["data"]

    async def list_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> dict:
        """
        List all the roles that are registered with the plugin.

        Supported methods:
            LIST: /auth/{mount_point}/role. Produces: 200 application/json

        :param mount_point: The "path" the kubernetes auth method was mounted on.
        :return: The "data" key from the VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/role"
        response = await self._adapter.list(
            url=api_path,
        )
        return response.value["data"]

    async def delete_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete the previously registered role.

        Supported methods:
            DELETE: /auth/{mount_point}/role/{name}. Produces: 204 (empty body)

        :param name: Name of the role.
        :param mount_point: The "path" the kubernetes auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/role/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def login(
        self, role: str, jwt: str, use_token: bool = True, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Fetch a token.

        This endpoint takes a signed JSON Web Token (JWT) and a role name for some entity. It verifies the JWT signature
        to authenticate that entity and then authorizes the entity for the given role.

        Supported methods:
            POST: /auth/{mount_point}/login. Produces: 200 application/json

        :param role: Name of the role against which the login is being attempted.
        :param jwt: Signed JSON Web Token (JWT) from Kubernetes service account.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.Adapter` instance under the _adapter Client attribute.
        :param mount_point: The "path" the kubernetes auth method was mounted on.
        :return: The VaultxResponse of the request.
        """
        params = {
            "role": role,
            "jwt": jwt,
        }

        api_path = f"/v1/auth/{mount_point}/login"
        return await self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )
