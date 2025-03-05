"""Raft methods module."""

from typing import Any, Optional, Union

from httpx import Response

from vaultx import adapters, utils
from vaultx.api.vault_api_base import AsyncVaultApiBase


class Raft(AsyncVaultApiBase):
    """
    Raft cluster-related system backend methods.

    When using Shamir seal, as soon as the Vault server is brought up, this API should be invoked
    instead of sys/init. This API completes in 2 phases. Once this is invoked, the joining node
    will receive a challenge from the Raft's leader node. This challenge can be answered by the
    joining node only after a successful unseal. Hence, the joining node should be unsealed using
    the unseal keys of the Raft's leader node.

    Reference: https://www.vaultproject.io/api-docs/system/storage/raft
    """

    async def join_raft_cluster(
        self,
        leader_api_addr: str,
        retry: bool = False,
        leader_ca_cert: Optional[str] = None,
        leader_client_cert: Optional[str] = None,
        leader_client_key: Optional[str] = None,
    ) -> Union[dict[str, Any], Response]:
        """
        Join a new server node to the Raft cluster.

        When using Shamir seal, as soon as the Vault server is brought up, this API should be invoked
        instead of sys/init. This API completes in 2 phases. Once this is invoked, the joining node will
        receive a challenge from the Raft's leader node. This challenge can be answered by the joining
        node only after a successful unseal. Hence, the joining node should be unsealed using the unseal
        keys of the Raft's leader node.

        Supported methods:
            POST: /sys/storage/raft/join.

        :param leader_api_addr: Address of the leader node in the Raft cluster to which this node is trying to join.
        :param retry: Retry joining the Raft cluster in case of failures.
        :param leader_ca_cert: CA certificate used to communicate with Raft's leader node.
        :param leader_client_cert: AsyncClient certificate used to communicate with Raft's leader node.
        :param leader_client_key: AsyncClient key used to communicate with Raft's leader node.
        :return: The response of the join_raft_cluster request.
        """
        params = utils.remove_nones(
            {
                "leader_api_addr": leader_api_addr,
                "retry": retry,
                "leader_ca_cert": leader_ca_cert,
                "leader_client_cert": leader_client_cert,
                "leader_client_key": leader_client_key,
            }
        )
        api_path = "/v1/sys/storage/raft/join"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_raft_config(self) -> Union[dict[str, Any], Response]:
        """
        Read the details of all the nodes in the raft cluster.

        Supported methods:
            GET: /sys/storage/raft/configuration.

        :return: The response of the read_raft_config request.
        """
        api_path = "/v1/sys/storage/raft/configuration"
        return await self._adapter.get(
            url=api_path,
        )

    async def remove_raft_node(self, server_id: str) -> Union[dict[str, Any], Response]:
        """
        Remove a node from the raft cluster.

        Supported methods:
            POST: /sys/storage/raft/remove-peer.

        :param server_id: The ID of the node to remove.
        :return: The response of the remove_raft_node request.
        """
        params = {
            "server_id": server_id,
        }
        api_path = "/v1/sys/storage/raft/remove-peer"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def take_raft_snapshot(self) -> Union[dict[str, Any], Response]:
        """
        Return a snapshot of the current state of the raft cluster.
        The snapshot is returned as binary data and should be redirected to a file.
        This endpoint will ignore your chosen adapter and always uses a AsyncRawAdapter.

        Supported methods:
            GET: /sys/storage/raft/snapshot.

        :return: The response of the snapshot request.
        """
        api_path = "/v1/sys/storage/raft/snapshot"
        raw_adapter = adapters.AsyncRawAdapter.from_adapter(self._adapter)
        return await raw_adapter.get(
            url=api_path,
            stream=True,
        )

    async def restore_raft_snapshot(self, snapshot: bytes) -> Union[dict[str, Any], Response]:
        """
        Install the provided snapshot, returning the cluster to the state defined in it.

        Supported methods:
            POST: /sys/storage/raft/snapshot.

        :param snapshot: Previously created raft snapshot / binary data.
        :return: The response of the restore_raft_snapshot request.
        """
        api_path = "/v1/sys/storage/raft/snapshot"
        return await self._adapter.post(
            url=api_path,
            data=snapshot,
        )

    async def force_restore_raft_snapshot(self, snapshot: bytes) -> Union[dict[str, Any], Response]:
        """
        Install the provided snapshot, returning the cluster to the state defined in it.
        This is same as writing to /sys/storage/raft/snapshot except that this bypasses checks
        ensuring the Autounseal or shamir keys are consistent with the snapshot data.

        Supported methods:
            POST: /sys/storage/raft/snapshot-force.

        :param snapshot: Previously created raft snapshot / binary data.
        :return: The response of the force_restore_raft_snapshot request.
        """
        api_path = "/v1/sys/storage/raft/snapshot-force"
        return await self._adapter.post(
            url=api_path,
            data=snapshot,
        )

    async def read_raft_auto_snapshot_status(self, name: str) -> Union[dict[str, Any], Response]:
        """
        Read the status of the raft auto snapshot.

        Supported methods:
            GET: /sys/storage/raft/snapshot-auto/status/:name. Produces: 200 application/json

        :param name: The name of the snapshot configuration.
        :return: The response of the read_raft_auto_snapshot_status request.
        """
        api_path = f"/v1/sys/storage/raft/snapshot-auto/status/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def read_raft_auto_snapshot_config(self, name: str) -> Union[dict[str, Any], Response]:
        """
        Read the configuration of the raft auto snapshot.

        Supported methods:
            GET: /sys/storage/raft/snapshot-auto/config/:name. Produces: 200 application/json

        :param name: The name of the snapshot configuration.
        :return: The response of the read_raft_auto_snapshot_config request.
        """
        api_path = f"/v1/sys/storage/raft/snapshot-auto/config/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_raft_auto_snapshot_configs(self) -> Union[dict[str, Any], Response]:
        """
        List the configurations of the raft auto snapshot.

        Supported methods:
            LIST: /sys/storage/raft/snapshot-auto/config. Produces: 200 application/json

        :return: The response of the list_raft_auto_snapshot_configs request.
        """
        api_path = "/v1/sys/storage/raft/snapshot-auto/config"
        return await self._adapter.list(
            url=api_path,
        )

    async def create_or_update_raft_auto_snapshot_config(
        self, name: str, interval: str, storage_type: str, retain: int = 1, **kwargs
    ) -> Union[dict[str, Any], Response]:
        """
        Create or update the configuration of the raft auto snapshot.

        Supported methods:
            POST: /sys/storage/raft/snapshot-auto/config/:name. Produces: 204 application/json

        :param name: The name of the snapshot configuration.
        :param interval: The interval at which snapshots should be taken.
        :param storage_type: The type of storage to use for the snapshot.
        :param retain: The number of snapshots to retain. Default is 1
        :param kwargs: Additional parameters to send in the request. Should be params specific to the storage type.
        :return: The response of the create_or_update_raft_auto_snapshot_config request.
        """
        params = utils.remove_nones(
            {
                "interval": interval,
                "storage_type": storage_type,
                "retain": retain,
                **kwargs,
            }
        )

        api_path = f"/v1/sys/storage/raft/snapshot-auto/config/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def delete_raft_auto_snapshot_config(self, name: str) -> Union[dict[str, Any], Response]:
        """
        Delete the configuration of the raft auto snapshot.

        Supported methods:
            DELETE: /sys/storage/raft/snapshot-auto/config/:name. Produces: 204 application/json

        :param name: The name of the snapshot configuration.
        :return: The response of the delete_raft_auto_snapshot_config request.
        """
        api_path = f"/v1/sys/storage/raft/snapshot-auto/config/{name}"
        return await self._adapter.delete(
            url=api_path,
        )
