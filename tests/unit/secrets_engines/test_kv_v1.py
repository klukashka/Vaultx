import unittest
from unittest import mock

from httpx import Response

from vaultx import exceptions
from vaultx.api.async_secrets_engines.kv_v1 import KvV1 as AsyncKvV1
from vaultx.api.secrets_engines.kv_v1 import KvV1


class TestKvV1(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.kv_v1 = KvV1(self.mock_adapter)

    def test_read_secret_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.kv_v1.read_secret(path="my-secret")
        self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/secret/my-secret",
        )

    def test_read_secret_with_custom_mount_point_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.kv_v1.read_secret(path="my-secret", mount_point="custom-mount")
        self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/custom-mount/my-secret",
        )

    def test_list_secrets_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["secret1/", "secret2/"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.kv_v1.list_secrets(path="my-folder")
        self.assertEqual(result.json(), {"data": {"keys": ["secret1/", "secret2/"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/secret/my-folder",
        )

    def test_create_or_update_secret_with_post_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        secret = {"key": "value"}
        result = self.kv_v1.create_or_update_secret(path="my-secret", secret=secret, method="POST")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/my-secret",
            json=secret,
        )

    def test_create_or_update_secret_with_put_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.put.return_value = mock_response

        secret = {"key": "value"}
        result = self.kv_v1.create_or_update_secret(path="my-secret", secret=secret, method="PUT")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/secret/my-secret",
            json=secret,
        )

    def test_create_or_update_secret_without_method_uses_post_for_new_secret(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response
        self.mock_adapter.get.side_effect = exceptions.VaultxError("Secret not found")

        secret = {"key": "value"}
        result = self.kv_v1.create_or_update_secret(path="my-secret", secret=secret)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/my-secret",
            json=secret,
        )

    def test_create_or_update_secret_without_method_uses_put_for_existing_secret(self):
        mock_response = Response(204)
        self.mock_adapter.put.return_value = mock_response
        self.mock_adapter.get.return_value = Response(200, json={"data": {"key": "value"}})

        secret = {"key": "value"}
        result = self.kv_v1.create_or_update_secret(path="my-secret", secret=secret)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/secret/my-secret",
            json=secret,
        )

    def test_create_or_update_secret_with_invalid_method_raises_error(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.kv_v1.create_or_update_secret(path="my-secret", secret={"key": "value"}, method="PATCH")

        self.assertEqual(
            str(context.exception),
            '"method" parameter provided invalid value; POST or PUT allowed, "PATCH" provided',
        )

    def test_delete_secret_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.kv_v1.delete_secret(path="my-secret")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/secret/my-secret",
        )


class TestAsyncKvV1(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.kv_v1 = AsyncKvV1(self.mock_adapter)

    async def test_read_secret_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.kv_v1.read_secret(path="my-secret")
        self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/secret/my-secret",
        )

    async def test_read_secret_with_custom_mount_point_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.kv_v1.read_secret(path="my-secret", mount_point="custom-mount")
        self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/custom-mount/my-secret",
        )

    async def test_list_secrets_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["secret1/", "secret2/"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.kv_v1.list_secrets(path="my-folder")
        self.assertEqual(result.json(), {"data": {"keys": ["secret1/", "secret2/"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/secret/my-folder",
        )

    async def test_create_or_update_secret_with_post_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        secret = {"key": "value"}
        result = await self.kv_v1.create_or_update_secret(path="my-secret", secret=secret, method="POST")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/my-secret",
            json=secret,
        )

    async def test_create_or_update_secret_with_put_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.put.return_value = mock_response

        secret = {"key": "value"}
        result = await self.kv_v1.create_or_update_secret(path="my-secret", secret=secret, method="PUT")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/secret/my-secret",
            json=secret,
        )

    async def test_create_or_update_secret_without_method_uses_post_for_new_secret(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response
        self.mock_adapter.get.side_effect = exceptions.VaultxError("Secret not found")

        secret = {"key": "value"}
        result = await self.kv_v1.create_or_update_secret(path="my-secret", secret=secret)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/secret/my-secret",
            json=secret,
        )

    async def test_create_or_update_secret_without_method_uses_put_for_existing_secret(self):
        mock_response = Response(204)
        self.mock_adapter.put.return_value = mock_response
        self.mock_adapter.get.return_value = Response(200, json={"data": {"key": "value"}})

        secret = {"key": "value"}
        result = await self.kv_v1.create_or_update_secret(path="my-secret", secret=secret)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/secret/my-secret",
            json=secret,
        )

    async def test_create_or_update_secret_with_invalid_method_raises_error(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.kv_v1.create_or_update_secret(path="my-secret", secret={"key": "value"}, method="PATCH")

        self.assertEqual(
            str(context.exception),
            '"method" parameter provided invalid value; POST or PUT allowed, "PATCH" provided',
        )

    async def test_delete_secret_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.kv_v1.delete_secret(path="my-secret")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/secret/my-secret",
        )
