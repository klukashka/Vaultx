import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_system_backend.mount import Mount as AsyncMount
from vaultx.api.system_backend.mount import Mount
from vaultx.exceptions import VaultxError


class TestMount(unittest.TestCase):
    def setUp(self):
        # Mock the _adapter attribute of the Mount class
        self.mock_adapter = mock.Mock()
        self.mount = Mount(self.mock_adapter)

    def test_list_mounted_secrets_engines(self):
        self.mock_adapter.get.return_value = {"data": {"secret/": {"type": "kv"}}}
        result = self.mount.list_mounted_secrets_engines()
        self.assertEqual(result, {"data": {"secret/": {"type": "kv"}}})
        self.mock_adapter.get.assert_called_once_with("/v1/sys/mounts")

    def test_retrieve_mount_option(self):
        self.mock_adapter.get.return_value = {"data": {"secret/": {"options": {"version": "2"}}}}
        result = self.mount.retrieve_mount_option(
            mount_point="secret",
            option_name="version",
            default_value="1",
        )
        self.assertEqual(result, "2")
        self.mock_adapter.get.assert_called_once_with("/v1/sys/mounts")

    def test_retrieve_mount_option_default_value(self):
        self.mock_adapter.get.return_value = {"data": {"secret/": {"options": None}}}
        result = self.mount.retrieve_mount_option(
            mount_point="secret",
            option_name="version",
            default_value="1",
        )
        self.assertEqual(result, "1")
        self.mock_adapter.get.assert_called_once_with("/v1/sys/mounts")

    def test_enable_secrets_engine(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.mount.enable_secrets_engine(
            backend_type="kv",
            path="secret",
            description="Test KV engine",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/mounts/secret",
            json={
                "type": "kv",
                "description": "Test KV engine",
                "config": None,
                "options": None,
                "plugin_name": None,
                "local": False,
                "seal_wrap": False,
            },
        )

    def test_disable_secrets_engine(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.mount.disable_secrets_engine(path="secret")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/mounts/secret",
        )

    def test_read_mount_configuration(self):
        self.mock_adapter.get.return_value = {"data": {"default_lease_ttl": 3600}}
        result = self.mount.read_mount_configuration(path="secret")
        self.assertEqual(result, {"data": {"default_lease_ttl": 3600}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/mounts/secret/tune",
        )

    def test_tune_mount_configuration(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.mount.tune_mount_configuration(
            path="secret",
            default_lease_ttl=3600,
            max_lease_ttl=7200,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/mounts/secret/tune",
            json={
                "default_lease_ttl": 3600,
                "max_lease_ttl": 7200,
            },
        )

    def test_move_backend(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.mount.move_backend(
            from_path="old_secret",
            to_path="new_secret",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/remount",
            json={
                "from": "old_secret",
                "to": "new_secret",
            },
        )


class TestAsyncMount(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Mock the _adapter attribute of the Mount class
        self.mock_adapter = mock.AsyncMock()
        self.mount = AsyncMount(self.mock_adapter)

    async def test_list_mounted_secrets_engines(self):
        self.mock_adapter.get.return_value = {"data": {"secret/": {"type": "kv"}}}
        result = await self.mount.list_mounted_secrets_engines()
        self.assertEqual(result, {"data": {"secret/": {"type": "kv"}}})
        self.mock_adapter.get.assert_called_once_with("/v1/sys/mounts")

    async def test_retrieve_mount_option(self):
        self.mock_adapter.get.return_value = {"data": {"secret/": {"options": {"version": "2"}}}}
        result = await self.mount.retrieve_mount_option(
            mount_point="secret",
            option_name="version",
            default_value="1",
        )
        self.assertEqual(result, "2")
        self.mock_adapter.get.assert_called_once_with("/v1/sys/mounts")

    async def test_retrieve_mount_option_default_value(self):
        self.mock_adapter.get.return_value = {"data": {"secret/": {"options": None}}}
        result = await self.mount.retrieve_mount_option(
            mount_point="secret",
            option_name="version",
            default_value="1",
        )
        self.assertEqual(result, "1")
        self.mock_adapter.get.assert_called_once_with("/v1/sys/mounts")

    async def test_enable_secrets_engine(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.mount.enable_secrets_engine(
            backend_type="kv",
            path="secret",
            description="Test KV engine",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/mounts/secret",
            json={
                "type": "kv",
                "description": "Test KV engine",
                "config": None,
                "options": None,
                "plugin_name": None,
                "local": False,
                "seal_wrap": False,
            },
        )

    async def test_disable_secrets_engine(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.mount.disable_secrets_engine(path="secret")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/mounts/secret",
        )

    async def test_read_mount_configuration(self):
        self.mock_adapter.get.return_value = {"data": {"default_lease_ttl": 3600}}
        result = await self.mount.read_mount_configuration(path="secret")
        self.assertEqual(result, {"data": {"default_lease_ttl": 3600}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/mounts/secret/tune",
        )

    async def test_tune_mount_configuration(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.mount.tune_mount_configuration(
            path="secret",
            default_lease_ttl=3600,
            max_lease_ttl=7200,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/mounts/secret/tune",
            json={
                "default_lease_ttl": 3600,
                "max_lease_ttl": 7200,
            },
        )

    async def test_move_backend(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.mount.move_backend(
            from_path="old_secret",
            to_path="new_secret",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/remount",
            json={
                "from": "old_secret",
                "to": "new_secret",
            },
        )
