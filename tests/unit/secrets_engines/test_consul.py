import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.consul import Consul as AsyncConsul
from vaultx.api.secrets_engines.consul import Consul


class TestConsul(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.consul = Consul(self.mock_adapter)

    def test_configure_access_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "address": "127.0.0.1:8500",
            "token": "test-token",
            "scheme": "http",
        }
        result = self.consul.configure_access(**params)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/consul/config/access",
            json=params,
        )

    def test_create_or_update_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "token_type": "client",
            "policy": "test-policy",
            "policies": ["policy1", "policy2"],
            "local": True,
            "ttl": "1h",
            "max_ttl": "24h",
        }
        result = self.consul.create_or_update_role(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "token_type": "client",
            "policy": "test-policy",
            "policies": ["policy1", "policy2"],
            "local": True,
            "ttl": "1h",
            "max_ttl": "24h",
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/consul/roles/test-role",
            json=expected_params,
        )

    def test_read_role_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.consul.read_role(name="test-role")
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/consul/roles/test-role",
        )

    def test_list_roles_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.consul.list_roles()
        self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/consul/roles",
        )

    def test_delete_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.consul.delete_role(name="test-role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/consul/roles/test-role",
        )

    def test_generate_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"token": "test-token"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.consul.generate_credentials(name="test-role")
        self.assertEqual(result.json(), {"data": {"token": "test-token"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/consul/creds/test-role",
        )


class TestAsyncConsul(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.consul = AsyncConsul(self.mock_adapter)

    async def test_configure_access_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "address": "127.0.0.1:8500",
            "token": "test-token",
            "scheme": "http",
        }
        result = await self.consul.configure_access(**params)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/consul/config/access",
            json=params,
        )

    async def test_create_or_update_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "token_type": "client",
            "policy": "test-policy",
            "policies": ["policy1", "policy2"],
            "local": True,
            "ttl": "1h",
            "max_ttl": "24h",
        }
        result = await self.consul.create_or_update_role(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "token_type": "client",
            "policy": "test-policy",
            "policies": ["policy1", "policy2"],
            "local": True,
            "ttl": "1h",
            "max_ttl": "24h",
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/consul/roles/test-role",
            json=expected_params,
        )

    async def test_read_role_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.consul.read_role(name="test-role")
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/consul/roles/test-role",
        )

    async def test_list_roles_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.consul.list_roles()
        self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/consul/roles",
        )

    async def test_delete_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.consul.delete_role(name="test-role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/consul/roles/test-role",
        )

    async def test_generate_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"token": "test-token"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.consul.generate_credentials(name="test-role")
        self.assertEqual(result.json(), {"data": {"token": "test-token"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/consul/creds/test-role",
        )
