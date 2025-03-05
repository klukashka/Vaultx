import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.kv_v2 import KvV2 as AsyncKvV2
from vaultx.api.secrets_engines.kv_v2 import KvV2


class TestKvV2(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.kv_v2 = KvV2(self.mock_adapter)

    def test_configure_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.kv_v2.configure(max_versions=5, cas_required=True, delete_version_after="1h")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/config",
            json={
                "max_versions": 5,
                "cas_required": True,
                "delete_version_after": "1h",
            },
        )

    def test_read_configuration_returns_response(self):
        mock_response = Response(200, json={"data": {"max_versions": 10}})
        self.mock_adapter.get.return_value = mock_response

        result = self.kv_v2.read_configuration()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"max_versions": 10}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/secret/config",
        )

    def test_read_secret_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.kv_v2.read_secret(path="my-secret")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/secret/data/my-secret",
            params={},  # No query parameters are passed in this case
        )

    def test_read_secret_version_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.kv_v2.read_secret_version(path="my-secret", version=2)
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/secret/data/my-secret",
            params={"version": 2},
        )

    def test_create_or_update_secret_returns_response(self):
        mock_response = Response(200, json={"data": {"version": 1}})
        self.mock_adapter.post.return_value = mock_response

        secret = {"key": "value"}
        result = self.kv_v2.create_or_update_secret(path="my-secret", secret=secret)
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"version": 1}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/data/my-secret",
            json={"options": {}, "data": secret},
        )

    def test_patch_updates_secret_and_returns_response(self):
        mock_read_response = {"data": {"data": {"key": "old-value"}, "metadata": {"version": 1}}}
        mock_write_response = Response(200, json={"data": {"version": 2}})
        self.mock_adapter.get.return_value = mock_read_response
        self.mock_adapter.post.return_value = mock_write_response

        result = self.kv_v2.patch(path="my-secret", secret={"key": "new-value"})
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"version": 2}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/data/my-secret",
            json={"options": {"cas": 1}, "data": {"key": "new-value"}},
        )

    def test_delete_latest_version_of_secret_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.kv_v2.delete_latest_version_of_secret(path="my-secret")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/secret/data/my-secret",
        )

    def test_delete_secret_versions_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.kv_v2.delete_secret_versions(path="my-secret", versions=[1, 2])
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/delete/my-secret",
            json={"versions": [1, 2]},
        )

    def test_undelete_secret_versions_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.kv_v2.undelete_secret_versions(path="my-secret", versions=[1, 2])
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/undelete/my-secret",
            json={"versions": [1, 2]},
        )

    def test_destroy_secret_versions_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.kv_v2.destroy_secret_versions(path="my-secret", versions=[1, 2])
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/destroy/my-secret",
            json={"versions": [1, 2]},
        )

    def test_list_secrets_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["secret1", "secret2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.kv_v2.list_secrets(path="my-folder")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["secret1", "secret2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/secret/metadata/my-folder",
        )

    def test_read_secret_metadata_returns_response(self):
        mock_response = Response(200, json={"data": {"versions": {"1": {}}}})
        self.mock_adapter.get.return_value = mock_response

        result = self.kv_v2.read_secret_metadata(path="my-secret")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"versions": {"1": {}}}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/secret/metadata/my-secret",
        )

    def test_update_metadata_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.kv_v2.update_metadata(
            path="my-secret",
            max_versions=5,
            cas_required=True,
            delete_version_after="1h",
            custom_metadata={"owner": "team-a"},
        )

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/metadata/my-secret",
            json={
                "max_versions": 5,
                "cas_required": True,
                "delete_version_after": "1h",
                "custom_metadata": {"owner": "team-a"},
            },
        )

    def test_delete_metadata_and_all_versions_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.kv_v2.delete_metadata_and_all_versions(path="my-secret")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/secret/metadata/my-secret",
        )


class TestAsyncKvV2(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.kv_v2 = AsyncKvV2(self.mock_adapter)

    async def test_configure_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.kv_v2.configure(max_versions=5, cas_required=True, delete_version_after="1h")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/config",
            json={
                "max_versions": 5,
                "cas_required": True,
                "delete_version_after": "1h",
            },
        )

    async def test_read_configuration_returns_response(self):
        mock_response = Response(200, json={"data": {"max_versions": 10}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.kv_v2.read_configuration()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"max_versions": 10}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/secret/config",
        )

    async def test_read_secret_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.kv_v2.read_secret(path="my-secret")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/secret/data/my-secret",
            params={},
        )

    async def test_read_secret_version_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.kv_v2.read_secret_version(path="my-secret", version=2)
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/secret/data/my-secret",
            params={"version": 2},
        )

    async def test_create_or_update_secret_returns_response(self):
        mock_response = Response(200, json={"data": {"version": 1}})
        self.mock_adapter.post.return_value = mock_response

        secret = {"key": "value"}
        result = await self.kv_v2.create_or_update_secret(path="my-secret", secret=secret)
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"version": 1}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/data/my-secret",
            json={"options": {}, "data": secret},
        )

    async def test_patch_updates_secret_and_returns_response(self):
        mock_read_response = {"data": {"data": {"key": "old-value"}, "metadata": {"version": 1}}}
        mock_write_response = Response(200, json={"data": {"version": 2}})
        self.mock_adapter.get.return_value = mock_read_response
        self.mock_adapter.post.return_value = mock_write_response

        result = await self.kv_v2.patch(path="my-secret", secret={"key": "new-value"})
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"version": 2}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/data/my-secret",
            json={"options": {"cas": 1}, "data": {"key": "new-value"}},
        )

    async def test_delete_latest_version_of_secret_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.kv_v2.delete_latest_version_of_secret(path="my-secret")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/secret/data/my-secret",
        )

    async def test_delete_secret_versions_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.kv_v2.delete_secret_versions(path="my-secret", versions=[1, 2])
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/delete/my-secret",
            json={"versions": [1, 2]},
        )

    async def test_undelete_secret_versions_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.kv_v2.undelete_secret_versions(path="my-secret", versions=[1, 2])
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/undelete/my-secret",
            json={"versions": [1, 2]},
        )

    async def test_destroy_secret_versions_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.kv_v2.destroy_secret_versions(path="my-secret", versions=[1, 2])
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/destroy/my-secret",
            json={"versions": [1, 2]},
        )

    async def test_list_secrets_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["secret1", "secret2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.kv_v2.list_secrets(path="my-folder")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["secret1", "secret2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/secret/metadata/my-folder",
        )

    async def test_read_secret_metadata_returns_response(self):
        mock_response = Response(200, json={"data": {"versions": {"1": {}}}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.kv_v2.read_secret_metadata(path="my-secret")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"versions": {"1": {}}}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/secret/metadata/my-secret",
        )

    async def test_update_metadata_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.kv_v2.update_metadata(
            path="my-secret",
            max_versions=5,
            cas_required=True,
            delete_version_after="1h",
            custom_metadata={"owner": "team-a"},
        )

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/metadata/my-secret",
            json={
                "max_versions": 5,
                "cas_required": True,
                "delete_version_after": "1h",
                "custom_metadata": {"owner": "team-a"},
            },
        )

    async def test_delete_metadata_and_all_versions_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.kv_v2.delete_metadata_and_all_versions(path="my-secret")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/secret/metadata/my-secret",
        )
