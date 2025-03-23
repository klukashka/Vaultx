import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_system_backend.wrapping import Wrapping as AsyncWrapping
from vaultx.api.system_backend.wrapping import Wrapping


class TestWrapping(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.wrapping = Wrapping(self.mock_adapter)

    def test_unwrap_with_token_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.wrapping.unwrap(token="test_token")

        self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/wrapping/unwrap",
            json={"token": "test_token"},
        )

    def test_unwrap_without_token_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.wrapping.unwrap()

        self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/wrapping/unwrap",
            json={},
        )

    def test_wrap_with_payload_and_ttl_returns_wrapped_token(self):
        mock_response = Response(200, json={"wrap_info": {"token": "wrapped_token"}})
        self.mock_adapter.post.return_value = mock_response

        payload = {"key": "value"}
        ttl = 120
        result = self.wrapping.wrap(payload=payload, ttl=ttl)

        self.assertEqual(result.json(), {"wrap_info": {"token": "wrapped_token"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/wrapping/wrap",
            json=payload,
            headers={"X-Vault-Wrap-TTL": "120"},
        )

    def test_wrap_without_payload_uses_default_values(self):
        mock_response = Response(200, json={"wrap_info": {"token": "wrapped_token"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.wrapping.wrap()

        self.assertEqual(result.json(), {"wrap_info": {"token": "wrapped_token"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/wrapping/wrap",
            json={},
            headers={"X-Vault-Wrap-TTL": "60"},
        )


class TestAsyncWrapping(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.wrapping = AsyncWrapping(self.mock_adapter)

    async def test_unwrap_with_token_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.wrapping.unwrap(token="test_token")

        self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/wrapping/unwrap",
            json={"token": "test_token"},
        )

    async def test_unwrap_without_token_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.wrapping.unwrap()

        self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/wrapping/unwrap",
            json={},
        )

    async def test_wrap_with_payload_and_ttl_returns_wrapped_token(self):
        mock_response = Response(200, json={"wrap_info": {"token": "wrapped_token"}})
        self.mock_adapter.post.return_value = mock_response

        payload = {"key": "value"}
        ttl = 120
        result = await self.wrapping.wrap(payload=payload, ttl=ttl)

        self.assertEqual(result.json(), {"wrap_info": {"token": "wrapped_token"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/wrapping/wrap",
            json=payload,
            headers={"X-Vault-Wrap-TTL": "120"},
        )

    async def test_wrap_without_payload_uses_default_values(self):
        mock_response = Response(200, json={"wrap_info": {"token": "wrapped_token"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.wrapping.wrap()

        self.assertEqual(result.json(), {"wrap_info": {"token": "wrapped_token"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/wrapping/wrap",
            json={},
            headers={"X-Vault-Wrap-TTL": "60"},
        )
