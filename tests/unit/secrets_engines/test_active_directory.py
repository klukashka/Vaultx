import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.active_directory import ActiveDirectory as AsyncActiveDirectory
from vaultx.api.secrets_engines.active_directory import ActiveDirectory


class TestActiveDirectory(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.ad = ActiveDirectory(self.mock_adapter)

    def test_configure_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "binddn": "cn=admin,dc=example,dc=com",
            "bindpass": "password",
            "url": "ldap://localhost",
            "userdn": "ou=users,dc=example,dc=com",
            "upndomain": "example.com",
            "ttl": "1h",
            "max_ttl": "24h",
        }
        result = self.ad.configure(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ad/config",
            json=params,
        )

    def test_configure_with_int_ttl_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "binddn": "cn=admin,dc=example,dc=com",
            "bindpass": "password",
            "url": "ldap://localhost",
            "userdn": "ou=users,dc=example,dc=com",
            "upndomain": "example.com",
            "ttl": 3600,  # Integer TTL
            "max_ttl": 86400,  # Integer max_ttl
        }
        result = self.ad.configure(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ad/config",
            json=params,
        )

    def test_read_config_returns_response(self):
        mock_response = Response(200, json={"data": {"url": "ldap://localhost"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.ad.read_config()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"url": "ldap://localhost"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ad/config",
        )

    def test_create_or_update_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "service_account_name": "svc-account",
            "ttl": "1h",
        }
        result = self.ad.create_or_update_role(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ad/roles/test-role",
            json=params,
        )

    def test_create_or_update_role_with_int_ttl_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "service_account_name": "svc-account",
            "ttl": 3600,  # Integer TTL
        }
        result = self.ad.create_or_update_role(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ad/roles/test-role",
            json=params,
        )

    def test_read_role_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.ad.read_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ad/roles/test-role",
        )

    def test_list_roles_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.ad.list_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/ad/roles",
        )

    def test_delete_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.ad.delete_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/ad/roles/test-role",
        )

    def test_generate_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "password": "test-pass"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.ad.generate_credentials(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"username": "test-user", "password": "test-pass"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ad/creds/test-role",
        )


class TestAsyncActiveDirectory(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.ad = AsyncActiveDirectory(self.mock_adapter)

    async def test_configure_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "binddn": "cn=admin,dc=example,dc=com",
            "bindpass": "password",
            "url": "ldap://localhost",
            "userdn": "ou=users,dc=example,dc=com",
            "upndomain": "example.com",
            "ttl": "1h",
            "max_ttl": "24h",
        }
        result = await self.ad.configure(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ad/config",
            json=params,
        )

    async def test_read_config_returns_response(self):
        mock_response = Response(200, json={"data": {"url": "ldap://localhost"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.ad.read_config()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"url": "ldap://localhost"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ad/config",
        )

    async def test_create_or_update_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "service_account_name": "svc-account",
            "ttl": "1h",
        }
        result = await self.ad.create_or_update_role(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ad/roles/test-role",
            json=params,
        )

    async def test_read_role_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.ad.read_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ad/roles/test-role",
        )

    async def test_list_roles_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.ad.list_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/ad/roles",
        )

    async def test_delete_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.ad.delete_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/ad/roles/test-role",
        )

    async def test_generate_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "password": "test-pass"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.ad.generate_credentials(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"username": "test-user", "password": "test-pass"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ad/creds/test-role",
        )
