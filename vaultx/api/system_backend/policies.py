import json
from typing import Union

from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase


class Policies(VaultApiBase):
    def list_acl_policies(self) -> VaultxResponse:
        """
        List all configured acl policies.

        Supported methods:
            GET: /sys/policies/acl. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        api_path = "/v1/sys/policies/acl"
        return self._adapter.list(
            url=api_path,
        )

    def read_acl_policy(self, name: str) -> VaultxResponse:
        """
        Retrieve the policy body for the named acl policy.

        Supported methods:
            GET: /sys/policies/acl/{name}. Produces: 200 application/json

        :param name: The name of the acl policy to retrieve.
        :return: The response of the request
        """
        api_path = f"/v1/sys/policies/acl/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def create_or_update_acl_policy(
        self, name: str, policy: Union[str, dict], pretty_print: bool = True
    ) -> VaultxResponse:
        """
        Add a new or update an existing acl policy.

        Once a policy is updated, it takes effect immediately to all associated users.

        Supported methods:
            PUT: /sys/policies/acl/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to create.
        :param policy: Specifies the policy to create or update.
        :param pretty_print: If True, and provided a dict for the policy argument, send the policy JSON to Vault with
            "pretty" formatting.
        :return: The response of the request.
        """
        if isinstance(policy, dict):
            policy = json.dumps(policy, indent=4, sort_keys=True) if pretty_print else json.dumps(policy)
        params = {
            "policy": policy,
        }
        api_path = f"/v1/sys/policies/acl/{name}"
        return self._adapter.put(
            url=api_path,
            json=params,
        )

    def delete_acl_policy(self, name: str) -> VaultxResponse:
        """
        Delete the acl policy with the given name.

        This will immediately affect all users associated with this policy.

        Supported methods:
            DELETE: /sys/policies/acl/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to delete.
        :return: The response of the request.
        """
        api_path = f"/v1/sys/policies/acl/{name}"
        return self._adapter.delete(
            url=api_path,
        )

    def list_rgp_policies(self) -> VaultxResponse:
        """
        List all configured rgp policies.

        Supported methods:
            GET: /sys/policies/rgp. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        api_path = "/v1/sys/policies/rgp"
        return self._adapter.list(
            url=api_path,
        )

    def read_rgp_policy(self, name: str) -> VaultxResponse:
        """
        Retrieve the policy body for the named rgp policy.

        Supported methods:
            GET: /sys/policies/rgp/{name}. Produces: 200 application/json

        :param name: The name of the rgp policy to retrieve.
        :return: The response of the request
        """
        api_path = f"/v1/sys/policies/rgp/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def create_or_update_rgp_policy(self, name: str, policy: str, enforcement_level: str) -> VaultxResponse:
        """
        Add a new or update an existing rgp policy.
        Once a policy is updated, it takes effect immediately to all associated users.

        Supported methods:
            PUT: /sys/policies/rgp/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to create.
        :param policy: Specifies the policy to create or update.
        :param enforcement_level: Specifies the enforcement level to use.
            This must be one of advisory, soft-mandatory, or hard-mandatory
        :return: The response of the request.
        """
        params = {"policy": policy, "enforcement_level": enforcement_level}
        api_path = f"/v1/sys/policies/rgp/{name}"
        return self._adapter.put(
            url=api_path,
            json=params,
        )

    def delete_rgp_policy(self, name: str) -> VaultxResponse:
        """
        Delete the rgp policy with the given name.
        This will immediately affect all users associated with this policy.

        Supported methods:
            DELETE: /sys/policies/rgp/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to delete.
        :return: The response of the request.
        """
        api_path = f"/v1/sys/policies/rgp/{name}"
        return self._adapter.delete(
            url=api_path,
        )

    def list_egp_policies(self) -> VaultxResponse:
        """
        List all configured egp policies.

        Supported methods:
            GET: /sys/policies/egp. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        api_path = "/v1/sys/policies/egp"
        return self._adapter.list(
            url=api_path,
        )

    def read_egp_policy(self, name: str) -> VaultxResponse:
        """
        Retrieve the policy body for the named egp policy.

        Supported methods:
            GET: /sys/policies/egp/{name}. Produces: 200 application/json

        :param name: The name of the egp policy to retrieve.
        :return: The response of the request
        """
        api_path = f"/v1/sys/policies/egp/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def create_or_update_egp_policy(
        self, name: str, policy: str, enforcement_level: str, paths: list[str]
    ) -> VaultxResponse:
        """
        Add a new or update an existing egp policy.
        Once a policy is updated, it takes effect immediately to all associated users.

        Supported methods:
            PUT: /sys/policies/egp/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to create.
        :param policy: Specifies the policy to create or update.
        :param enforcement_level: Specifies the enforcement level to use. This must be one of advisory,
            soft-mandatory, or hard-mandatory
        :param paths: Specifies the paths on which this EGP should be applied.
        :return: The response of the request.
        """
        params = {
            "policy": policy,
            "enforcement_level": enforcement_level,
            "paths": paths,
        }
        api_path = f"/v1/sys/policies/egp/{name}"
        return self._adapter.put(
            url=api_path,
            json=params,
        )

    def delete_egp_policy(self, name: str) -> VaultxResponse:
        """
        Delete the egp policy with the given name.
        This will immediately affect all users associated with this policy.

        Supported methods:
            DELETE: /sys/policies/egp/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to delete.
        :return: The response of the request.
        """
        api_path = f"/v1/sys/policies/egp/{name}"
        return self._adapter.delete(
            url=api_path,
        )
