import json
from typing import Union

from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


class Policy(AsyncVaultApiBase):
    async def list_policies(self) -> VaultxResponse:
        """
        List all configured policies.

        Supported methods:
            GET: /sys/policy. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        api_path = "/v1/sys/policy"
        return await self._adapter.get(
            url=api_path,
        )

    async def read_policy(self, name: str) -> VaultxResponse:
        """
        Retrieve the policy body for the named policy.

        Supported methods:
            GET: /sys/policy/{name}. Produces: 200 application/json

        :param name: The name of the policy to retrieve.
        :return: The response of the request
        """
        api_path = f"/v1/sys/policy/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def create_or_update_policy(
        self, name: str, policy: Union[str, dict], pretty_print: bool = True
    ) -> VaultxResponse:
        """
        Add a new or update an existing policy.
        Once a policy is updated, it takes effect immediately to all associated users.

        Supported methods:
            PUT: /sys/policy/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to create.
        :param policy: Specifies the policy document.
        :param pretty_print: If True, and provided a dict for the policy argument, send the policy JSON to Vault with
            "pretty" formatting.
        :return: The response of the request.
        """
        if isinstance(policy, dict):
            policy = json.dumps(policy, indent=4, sort_keys=True) if pretty_print else json.dumps(policy)
        params = {
            "policy": policy,
        }
        api_path = f"/v1/sys/policy/{name}"
        return await self._adapter.put(
            url=api_path,
            json=params,
        )

    async def delete_policy(self, name: str) -> VaultxResponse:
        """
        Delete the policy with the given name.
        This will immediately affect all users associated with this policy.

        Supported methods:
            DELETE: /sys/policy/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to delete.
        :return: The response of the request.
        """
        api_path = f"/v1/sys/policy/{name}"
        return await self._adapter.delete(
            url=api_path,
        )
