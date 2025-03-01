import unittest
from unittest import mock

from httpx import Response

from vaultx.api.system_backend import Wrapping


class TestWrapping(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.wrapping = Wrapping(self.mock_adapter)

    def test_unwrap_with_token_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.wrapping.unwrap(token="test_token")

        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"key": "value"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/wrapping/unwrap",
            json={"token": "test_token"},
        )

    def test_unwrap_without_token_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "value"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.wrapping.unwrap()

        if isinstance(result, Response):
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

        if isinstance(result, Response):
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

        if isinstance(result, Response):
            self.assertEqual(result.json(), {"wrap_info": {"token": "wrapped_token"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/wrapping/wrap",
            json={},
            headers={"X-Vault-Wrap-TTL": "60"},
        )
