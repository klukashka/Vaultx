import unittest
from unittest import mock

from httpx import Response

from vaultx.adapters import VaultxResponse
from vaultx.api.async_auth_methods.jwt import Jwt as AsyncJwt
from vaultx.api.auth_methods.jwt import Jwt


class TestJwt(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.jwt = Jwt(self.mock_adapter)

    def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.jwt.configure(oidc_discovery_url="https://example.com")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_config(self):
        mock_response = Response(200, json={"data": {"oidc_discovery_url": "https://example.com"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.jwt.read_config()
        self.assertEqual(result.value["data"], {"oidc_discovery_url": "https://example.com"})
        self.mock_adapter.get.assert_called_once()

    def test_create_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.jwt.create_role(
            name="test_role",
            user_claim="sub",
            allowed_redirect_uris=["https://example.com/callback"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.jwt.read_role(name="test_role")
        self.assertEqual(result.value["data"], {"name": "test_role"})
        self.mock_adapter.get.assert_called_once()

    def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.jwt.list_roles()
        self.assertEqual(result.value["data"], {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.jwt.delete_role(name="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_oidc_authorization_url_request(self):
        self.mock_adapter.post.return_value = Response(200, json={"data": {"auth_url": "https://example.com/auth"}})
        result = self.jwt.oidc_authorization_url_request(role="test_role", redirect_uri="https://example.com/callback")
        self.assertEqual(result.json()["data"], {"auth_url": "https://example.com/auth"})
        self.mock_adapter.post.assert_called_once()

    def test_oidc_callback(self):
        self.mock_adapter.get.return_value = Response(200, json={"data": {"token": "test_token"}})
        result = self.jwt.oidc_callback(state="test_state", nonce="test_nonce", code="test_code")
        self.assertEqual(result.json()["data"], {"token": "test_token"})
        self.mock_adapter.get.assert_called_once()

    def test_jwt_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = self.jwt.jwt_login(role="test_role", jwt="test_jwt")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()


class TestAsyncJwt(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.jwt = AsyncJwt(self.mock_adapter)

    async def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.jwt.configure(oidc_discovery_url="https://example.com")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_config(self):
        mock_response = Response(200, json={"data": {"oidc_discovery_url": "https://example.com"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.jwt.read_config()
        self.assertEqual(result.value["data"], {"oidc_discovery_url": "https://example.com"})
        self.mock_adapter.get.assert_called_once()

    async def test_create_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.jwt.create_role(
            name="test_role",
            user_claim="sub",
            allowed_redirect_uris=["https://example.com/callback"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.jwt.read_role(name="test_role")
        self.assertEqual(result.value["data"], {"name": "test_role"})
        self.mock_adapter.get.assert_called_once()

    async def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.jwt.list_roles()
        self.assertEqual(result.value["data"], {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    async def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.jwt.delete_role(name="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_oidc_authorization_url_request(self):
        self.mock_adapter.post.return_value = Response(200, json={"data": {"auth_url": "https://example.com/auth"}})
        result = await self.jwt.oidc_authorization_url_request(
            role="test_role", redirect_uri="https://example.com/callback"
        )
        self.assertEqual(result.json()["data"], {"auth_url": "https://example.com/auth"})
        self.mock_adapter.post.assert_called_once()

    async def test_oidc_callback(self):
        self.mock_adapter.get.return_value = Response(200, json={"data": {"token": "test_token"}})
        result = await self.jwt.oidc_callback(state="test_state", nonce="test_nonce", code="test_code")
        self.assertEqual(result.json()["data"], {"token": "test_token"})
        self.mock_adapter.get.assert_called_once()

    async def test_jwt_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = await self.jwt.jwt_login(role="test_role", jwt="test_jwt")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()
