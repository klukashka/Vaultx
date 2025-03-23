from typing import Optional, Union

from vaultx import exceptions, utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase
from vaultx.constants.azure import VALID_ENVIRONMENTS


DEFAULT_MOUNT_POINT = "azure"


class Azure(AsyncVaultApiBase):
    """
    Azure Auth Method (API).

    Reference: https://www.vaultproject.io/api/auth/azure/index.html
    """

    async def configure(
        self,
        tenant_id: str,
        resource: str,
        environment: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure the credentials required for the plugin to perform API calls to Azure.

        These credentials will be used to query the metadata about the virtual machine.

        Supported methods:
            POST: /auth/{mount_point}/config. Produces: 204 (empty body)

        :param tenant_id: The tenant id for the Azure Active Directory organization.
        :param resource: The configured URL for the application registered in Azure Active Directory.
        :param environment: The Azure cloud environment. Valid values: AzurePublicCloud, AzureUSGovernmentCloud,
            AzureChinaCloud, AzureGermanCloud.
        :param client_id: The client id for credentials to query the Azure APIs.  Currently read permissions to query
            compute resources are required.
        :param client_secret: The client secret for credentials to query the Azure APIs.
        :param mount_point: The "path" the azure auth method was mounted on.
        :return: The response of the request.
        """
        if environment is not None and environment not in VALID_ENVIRONMENTS:
            environments = ",".join(VALID_ENVIRONMENTS)
            raise exceptions.VaultxError(
                f'invalid environment argument provided: "{environment}"; supported environments: "{environments}"'
            )
        params = {
            "tenant_id": tenant_id,
            "resource": resource,
        }
        params.update(
            utils.remove_nones(
                {
                    "environment": environment,
                    "client_id": client_id,
                    "client_secret": client_secret,
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

        :param mount_point: The "path" the azure auth method was mounted on.
        :return: The data key from the VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config"
        response = await self._adapter.get(
            url=api_path,
        )
        return response.value["data"]

    async def delete_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete the previously configured Azure config and credentials.

        Supported methods:
            DELETE: /auth/{mount_point}/config. Produces: 204 (empty body)

        :param mount_point: The "path" the azure auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config"
        return await self._adapter.delete(
            url=api_path,
        )

    async def create_role(
        self,
        name: str,
        policies: Optional[Union[str, list]] = None,
        ttl: Optional[str] = None,
        max_ttl: Optional[str] = None,
        period: Optional[str] = None,
        bound_service_principal_ids: Optional[list] = None,
        bound_group_ids: Optional[list] = None,
        bound_locations: Optional[list] = None,
        bound_subscription_ids: Optional[list] = None,
        bound_resource_groups: Optional[list] = None,
        bound_scale_sets: Optional[list] = None,
        num_uses: Optional[int] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create a role in the method.

        Role types have specific entities that can perform login operations against this endpoint. Constraints specific
        to the role type must be set on the role. These are applied to the authenticated entities attempting to login.

        Supported methods:
            POST: /auth/{mount_point}/role/{name}. Produces: 204 (empty body)

        :param name: Name of the role.
        :param policies: Policies to be set on tokens issued using this role.
        :param num_uses: Number of uses to set on a token produced by this role.
        :param ttl: The TTL period of tokens issued using this role in seconds.
        :param max_ttl: The maximum allowed lifetime of tokens issued in seconds using this role.
        :param period: If set, indicates that the token generated using this role should never expire. The token should
            be renewed within the duration specified by this value. At each renewal, the token's TTL will be set to the
            value of this parameter.
        :param bound_service_principal_ids: The list of Service Principal IDs that login is restricted to.
        :param bound_group_ids: The list of group ids that login is restricted to.
        :param bound_locations: The list of locations that login is restricted to.
        :param bound_subscription_ids: The list of subscription IDs that login is restricted to.
        :param bound_resource_groups: The list of resource groups that the login restricted to.
        :param bound_scale_sets: The list of 'scale set' names that the login restricted to.
        :param mount_point: The "path" where the azure auth method mounted on.
        :return: The response of the request.
        """
        if policies is not None and not (
            isinstance(policies, str) or (isinstance(policies, list) and all(isinstance(p, str) for p in policies))
        ):
            arg = policies
            arg_type = type(policies)
            raise exceptions.VaultxError(
                f'unsupported policies argument provided "{arg}" ({arg_type}), required type: str or List[str]"'
            )
        params = utils.remove_nones(
            {
                "policies": policies,
                "ttl": ttl,
                "max_ttl": max_ttl,
                "period": period,
                "bound_service_principal_ids": bound_service_principal_ids,
                "bound_group_ids": bound_group_ids,
                "bound_locations": bound_locations,
                "bound_subscription_ids": bound_subscription_ids,
                "bound_resource_groups": bound_resource_groups,
                "bound_scale_sets": bound_scale_sets,
                "num_uses": num_uses,
            }
        )

        api_path = f"/v1/auth/{mount_point}/role/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> dict:
        """
        Read the previously registered role configuration.

        Supported methods:
            GET: /auth/{mount_point}/role/{name}. Produces: 200 application/json

        :param name: Name of the role.
        :param mount_point: The "path" the azure auth method was mounted on.
        :return: The "data" key from the VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/role/{name}"
        response = await self._adapter.get(
            url=api_path,
        )
        return response.value["data"]

    async def list_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List all the roles that are registered with the plugin.

        Supported methods:
            LIST: /auth/{mount_point}/role. Produces: 200 application/json

        :param mount_point: The "path" the azure auth method was mounted on.
        :return: The "data" key from the VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/role"
        response = await self._adapter.list(url=api_path)
        return response.value["data"]

    async def delete_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete the previously registered role.

        Supported methods:
            DELETE: /auth/{mount_point}/role/{name}. Produces: 204 (empty body)

        :param name: Name of the role.
        :param mount_point: The "path" the azure auth method was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/role/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def login(
        self,
        role: str,
        jwt: str,
        subscription_id: Optional[str] = None,
        resource_group_name: Optional[str] = None,
        vm_name: Optional[str] = None,
        vmss_name: Optional[str] = None,
        use_token: bool = True,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Fetch a token.

        This endpoint takes a signed JSON Web Token (JWT) and a role name for some entity. It verifies the JWT signature
        to authenticate that entity and then authorizes the entity for the given role.

        Supported methods:
            POST: /auth/{mount_point}/login. Produces: 200 application/json

        :param role: Name of the role against which the login is being attempted.
        :param jwt: Signed JSON Web Token (JWT) from Azure MSI.
        :param subscription_id: The subscription ID for the machine that generated the MSI token. This information can
            be obtained through instance metadata.
        :param resource_group_name: The resource group for the machine that generated the MSI token. This information
            can be obtained through instance metadata.
        :param vm_name: The virtual machine name for the machine that generated the MSI token. This information can be
            obtained through instance metadata.  If vmss_name is provided, this value is ignored.
        :param vmss_name: The virtual machine scale set name for the machine that generated the MSI token. This
            information can be obtained through instance metadata.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.Adapter` instance under the _adapter Client attribute.
        :param mount_point: The "path" the azure auth method was mounted on.
        :return: The VaultxResponse of the request.
        """
        params = {
            "role": role,
            "jwt": jwt,
        }
        params.update(
            utils.remove_nones(
                {
                    "subscription_id": subscription_id,
                    "resource_group_name": resource_group_name,
                    "vm_name": vm_name,
                    "vmss_name": vmss_name,
                }
            )
        )
        api_path = f"/v1/auth/{mount_point}/login"
        return await self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )
