import unittest
from unittest import mock
from unittest.mock import AsyncMock

from httpx import Response

from vaultx import exceptions
from vaultx.api.async_system_backend.auth import Auth as AsyncAuth
from vaultx.api.system_backend.auth import Auth


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.auth = Auth(self.mock_adapter)

    def test_list_auth_methods_returns_response(self):
        mock_response = Response(200, json={"data": {"token/": {"type": "token"}}})
        self.mock_adapter.get.return_value = mock_response

        result = self.auth.list_auth_methods()

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"token/": {"type": "token"}}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/auth",
        )

    def test_enable_auth_method_with_all_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.auth.enable_auth_method(
            method_type="github",
            description="GitHub auth method",
            config={"default_lease_ttl": "1h"},
            plugin_name="vault-plugin-auth-github",
            local=True,
            path="github-auth",
        )

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/auth/github-auth",
            json={
                "type": "github",
                "description": "GitHub auth method",
                "config": {"default_lease_ttl": "1h"},
                "plugin_name": "vault-plugin-auth-github",
                "local": True,
            },
        )

    def test_enable_auth_method_with_minimal_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.auth.enable_auth_method(method_type="token")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/auth/token",
            json={"type": "token", "local": False},
        )

    def test_disable_auth_method_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.auth.disable_auth_method(path="github-auth")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/auth/github-auth",
        )

    def test_read_auth_method_tuning_returns_response(self):
        mock_response = Response(200, json={"data": {"default_lease_ttl": 3600}})
        self.mock_adapter.get.return_value = mock_response

        result = self.auth.read_auth_method_tuning(path="github-auth")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"default_lease_ttl": 3600}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/auth/github-auth/tune",
        )

    def test_tune_auth_method_with_all_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.auth.tune_auth_method(
            path="github-auth",
            default_lease_ttl=3600,
            max_lease_ttl=7200,
            description="Updated GitHub auth method",
            audit_non_hmac_request_keys=["key1", "key2"],
            audit_non_hmac_response_keys=["key3", "key4"],
            listing_visibility="unauth",
            passthrough_request_headers=["header1", "header2"],
        )

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/auth/github-auth/tune",
            json={
                "default_lease_ttl": 3600,
                "max_lease_ttl": 7200,
                "description": "Updated GitHub auth method",
                "audit_non_hmac_request_keys": "key1,key2",
                "audit_non_hmac_response_keys": "key3,key4",
                "listing_visibility": "unauth",
                "passthrough_request_headers": "header1,header2",
            },
        )

    def test_tune_auth_method_with_minimal_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.auth.tune_auth_method(path="github-auth", default_lease_ttl=3600)

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/auth/github-auth/tune",
            json={"default_lease_ttl": 3600},
        )

    def test_tune_auth_method_with_invalid_listing_visibility_raises_error(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.auth.tune_auth_method(path="github-auth", listing_visibility="invalid")

        self.assertEqual(
            str(context.exception),
            'invalid listing_visibility argument provided: "invalid"; valid values: "unauth" or ""',
        )


class TestAsyncAuth(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.mock_adapter.get = AsyncMock()
        self.mock_adapter.post = AsyncMock()
        self.mock_adapter.delete = AsyncMock()
        self.auth = AsyncAuth(self.mock_adapter)

    async def test_list_auth_methods_returns_response(self):
        mock_response = Response(200, json={"data": {"token/": {"type": "token"}}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.auth.list_auth_methods()

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"token/": {"type": "token"}}})

        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/auth")

    async def test_enable_auth_method_with_all_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.auth.enable_auth_method(
            method_type="github",
            description="GitHub auth method",
            config={"default_lease_ttl": "1h"},
            plugin_name="vault-plugin-auth-github",
            local=True,
            path="github-auth",
        )

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)

        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/auth/github-auth",
            json={
                "type": "github",
                "description": "GitHub auth method",
                "config": {"default_lease_ttl": "1h"},
                "plugin_name": "vault-plugin-auth-github",
                "local": True,
            },
        )

    async def test_enable_auth_method_with_minimal_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.auth.enable_auth_method(method_type="token")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)

        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/auth/token",
            json={"type": "token", "local": False},
        )

    async def test_disable_auth_method_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.auth.disable_auth_method(path="github-auth")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)

        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/auth/github-auth")

    async def test_read_auth_method_tuning_returns_response(self):
        mock_response = Response(200, json={"data": {"default_lease_ttl": 3600}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.auth.read_auth_method_tuning(path="github-auth")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"default_lease_ttl": 3600}})

        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/auth/github-auth/tune")

    async def test_tune_auth_method_with_all_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.auth.tune_auth_method(
            path="github-auth",
            default_lease_ttl=3600,
            max_lease_ttl=7200,
            description="Updated GitHub auth method",
            audit_non_hmac_request_keys=["key1", "key2"],
            audit_non_hmac_response_keys=["key3", "key4"],
            listing_visibility="unauth",
            passthrough_request_headers=["header1", "header2"],
        )

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)

        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/auth/github-auth/tune",
            json={
                "default_lease_ttl": 3600,
                "max_lease_ttl": 7200,
                "description": "Updated GitHub auth method",
                "audit_non_hmac_request_keys": "key1,key2",
                "audit_non_hmac_response_keys": "key3,key4",
                "listing_visibility": "unauth",
                "passthrough_request_headers": "header1,header2",
            },
        )

    async def test_tune_auth_method_with_minimal_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.auth.tune_auth_method(path="github-auth", default_lease_ttl=3600)

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)

        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/auth/github-auth/tune",
            json={"default_lease_ttl": 3600},
        )

    async def test_tune_auth_method_with_invalid_listing_visibility_raises_error(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.auth.tune_auth_method(path="github-auth", listing_visibility="invalid")

        self.assertEqual(
            str(context.exception),
            'invalid listing_visibility argument provided: "invalid"; valid values: "unauth" or ""',
        )
