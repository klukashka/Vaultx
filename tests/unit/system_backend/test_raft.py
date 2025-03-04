import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_system_backend.raft import Raft as AsyncRaft
from vaultx.api.system_backend.raft import Raft


class TestRaft(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.raft = Raft(self.mock_adapter)

    def test_join_raft_cluster(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.raft.join_raft_cluster(
            leader_api_addr="http://leader:8200",
            retry=True,
            leader_ca_cert="ca_cert",
            leader_client_cert="client_cert",
            leader_client_key="client_key",
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/storage/raft/join",
            json={
                "leader_api_addr": "http://leader:8200",
                "retry": True,
                "leader_ca_cert": "ca_cert",
                "leader_client_cert": "client_cert",
                "leader_client_key": "client_key",
            },
        )

    def test_read_raft_config(self):
        self.mock_adapter.get.return_value = {"data": {"nodes": []}}
        result = self.raft.read_raft_config()
        if isinstance(result, Response):
            self.assertEqual(result, {"data": {"nodes": []}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/storage/raft/configuration")

    def test_remove_raft_node(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.raft.remove_raft_node(server_id="node1")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/storage/raft/remove-peer",
            json={"server_id": "node1"},
        )

    def test_restore_raft_snapshot(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.raft.restore_raft_snapshot(snapshot=b"snapshot_data")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/storage/raft/snapshot",
            data=b"snapshot_data",
        )

    def test_force_restore_raft_snapshot(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.raft.force_restore_raft_snapshot(snapshot=b"snapshot_data")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/storage/raft/snapshot-force",
            data=b"snapshot_data",
        )

    def test_read_raft_auto_snapshot_status(self):
        self.mock_adapter.get.return_value = {"data": {"status": "active"}}
        result = self.raft.read_raft_auto_snapshot_status(name="config1")
        self.assertEqual(result, {"data": {"status": "active"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/storage/raft/snapshot-auto/status/config1")

    def test_read_raft_auto_snapshot_config(self):
        self.mock_adapter.get.return_value = {"data": {"interval": "24h"}}
        result = self.raft.read_raft_auto_snapshot_config(name="config1")
        self.assertEqual(result, {"data": {"interval": "24h"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/storage/raft/snapshot-auto/config/config1")

    def test_list_raft_auto_snapshot_configs(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["config1", "config2"]}}
        result = self.raft.list_raft_auto_snapshot_configs()
        self.assertEqual(result, {"data": {"keys": ["config1", "config2"]}})
        self.mock_adapter.list.assert_called_once_with(url="/v1/sys/storage/raft/snapshot-auto/config")

    def test_create_or_update_raft_auto_snapshot_config(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.raft.create_or_update_raft_auto_snapshot_config(
            name="config1",
            interval="24h",
            storage_type="local",
            retain=2,
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/storage/raft/snapshot-auto/config/config1",
            json={
                "interval": "24h",
                "storage_type": "local",
                "retain": 2,
            },
        )

    def test_delete_raft_auto_snapshot_config(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.raft.delete_raft_auto_snapshot_config(name="config1")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/storage/raft/snapshot-auto/config/config1")


class TestAsyncRaft(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.raft = AsyncRaft(self.mock_adapter)

    async def test_join_raft_cluster(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.raft.join_raft_cluster(
            leader_api_addr="http://leader:8200",
            retry=True,
            leader_ca_cert="ca_cert",
            leader_client_cert="client_cert",
            leader_client_key="client_key",
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/storage/raft/join",
            json={
                "leader_api_addr": "http://leader:8200",
                "retry": True,
                "leader_ca_cert": "ca_cert",
                "leader_client_cert": "client_cert",
                "leader_client_key": "client_key",
            },
        )

    async def test_read_raft_config(self):
        self.mock_adapter.get.return_value = {"data": {"nodes": []}}
        result = await self.raft.read_raft_config()
        if isinstance(result, Response):
            self.assertEqual(result, {"data": {"nodes": []}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/storage/raft/configuration")

    async def test_remove_raft_node(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.raft.remove_raft_node(server_id="node1")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/storage/raft/remove-peer",
            json={"server_id": "node1"},
        )

    async def test_restore_raft_snapshot(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.raft.restore_raft_snapshot(snapshot=b"snapshot_data")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/storage/raft/snapshot",
            data=b"snapshot_data",
        )

    async def test_force_restore_raft_snapshot(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.raft.force_restore_raft_snapshot(snapshot=b"snapshot_data")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/storage/raft/snapshot-force",
            data=b"snapshot_data",
        )

    async def test_read_raft_auto_snapshot_status(self):
        self.mock_adapter.get.return_value = {"data": {"status": "active"}}
        result = await self.raft.read_raft_auto_snapshot_status(name="config1")
        self.assertEqual(result, {"data": {"status": "active"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/storage/raft/snapshot-auto/status/config1")

    async def test_read_raft_auto_snapshot_config(self):
        self.mock_adapter.get.return_value = {"data": {"interval": "24h"}}
        result = await self.raft.read_raft_auto_snapshot_config(name="config1")
        self.assertEqual(result, {"data": {"interval": "24h"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/storage/raft/snapshot-auto/config/config1")

    async def test_list_raft_auto_snapshot_configs(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["config1", "config2"]}}
        result = await self.raft.list_raft_auto_snapshot_configs()
        self.assertEqual(result, {"data": {"keys": ["config1", "config2"]}})
        self.mock_adapter.list.assert_called_once_with(url="/v1/sys/storage/raft/snapshot-auto/config")

    async def test_create_or_update_raft_auto_snapshot_config(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.raft.create_or_update_raft_auto_snapshot_config(
            name="config1",
            interval="24h",
            storage_type="local",
            retain=2,
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/storage/raft/snapshot-auto/config/config1",
            json={
                "interval": "24h",
                "storage_type": "local",
                "retain": 2,
            },
        )

    async def test_delete_raft_auto_snapshot_config(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.raft.delete_raft_auto_snapshot_config(name="config1")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/storage/raft/snapshot-auto/config/config1")
