import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.ldap import Ldap as AsyncLdap
from vaultx.api.secrets_engines.ldap import Ldap


class TestLdap(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.ldap = Ldap(self.mock_adapter)

    def test_configure(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.ldap.configure(
            binddn="cn=admin,dc=example,dc=com",
            bindpass="password",
            url="ldap://localhost",
            userdn="ou=users,dc=example,dc=com",
            userattr="uid",
            upndomain="example.com",
            password_policy="default",
            schema="openldap",
            connection_timeout=30,
            request_timeout=10,
            starttls=True,
            insecure_tls=False,
            certificate="-----BEGIN CERTIFICATE-----",
            client_tls_cert="-----BEGIN CERTIFICATE-----",
            client_tls_key="-----BEGIN PRIVATE KEY-----",
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ldap/config",
            json={
                "binddn": "cn=admin,dc=example,dc=com",
                "bindpass": "password",
                "url": "ldap://localhost",
                "userdn": "ou=users,dc=example,dc=com",
                "userattr": "uid",
                "upndomain": "example.com",
                "password_policy": "default",
                "schema": "openldap",
                "connection_timeout": 30,
                "request_timeout": 10,
                "starttls": True,
                "insecure_tls": False,
                "certificate": "-----BEGIN CERTIFICATE-----",
                "client_tls_cert": "-----BEGIN CERTIFICATE-----",
                "client_tls_key": "-----BEGIN PRIVATE KEY-----",
            },
        )

    def test_read_config(self):
        mock_response = Response(200, json={"data": {"binddn": "cn=admin,dc=example,dc=com"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.ldap.read_config()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"binddn": "cn=admin,dc=example,dc=com"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ldap/config",
        )

    def test_rotate_root(self):
        mock_response = Response(200, json={"data": {"message": "Root credentials rotated"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.ldap.rotate_root()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Root credentials rotated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ldap/rotate-root",
        )

    def test_create_or_update_static_role(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.ldap.create_or_update_static_role(
            name="test-role",
            username="test-user",
            dn="cn=test-user,ou=users,dc=example,dc=com",
            rotation_period="24h",
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ldap/static-role/test-role",
            json={
                "username": "test-user",
                "dn": "cn=test-user,ou=users,dc=example,dc=com",
                "rotation_period": "24h",
            },
        )

    def test_read_static_role(self):
        mock_response = Response(200, json={"data": {"username": "test-user"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.ldap.read_static_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"username": "test-user"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ldap/static-role/test-role",
        )

    def test_list_static_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.ldap.list_static_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/ldap/static-role",
        )

    def test_delete_static_role(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.ldap.delete_static_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/ldap/static-role/test-role",
        )

    def test_generate_static_credentials(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.ldap.generate_static_credentials(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ldap/static-cred/test-role",
        )

    def test_rotate_static_credentials(self):
        mock_response = Response(200, json={"data": {"message": "Credentials rotated"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.ldap.rotate_static_credentials(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Credentials rotated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ldap/rotate-role/test-role",
        )


class TestAsyncLdap(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.ldap = AsyncLdap(self.mock_adapter)

    async def test_configure_async(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.ldap.configure(
            binddn="cn=admin,dc=example,dc=com",
            bindpass="password",
            url="ldap://localhost",
            userdn="ou=users,dc=example,dc=com",
            userattr="uid",
            upndomain="example.com",
            password_policy="default",
            schema="openldap",
            connection_timeout=30,
            request_timeout=10,
            starttls=True,
            insecure_tls=False,
            certificate="-----BEGIN CERTIFICATE-----",
            client_tls_cert="-----BEGIN CERTIFICATE-----",
            client_tls_key="-----BEGIN PRIVATE KEY-----",
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ldap/config",
            json={
                "binddn": "cn=admin,dc=example,dc=com",
                "bindpass": "password",
                "url": "ldap://localhost",
                "userdn": "ou=users,dc=example,dc=com",
                "userattr": "uid",
                "upndomain": "example.com",
                "password_policy": "default",
                "schema": "openldap",
                "connection_timeout": 30,
                "request_timeout": 10,
                "starttls": True,
                "insecure_tls": False,
                "certificate": "-----BEGIN CERTIFICATE-----",
                "client_tls_cert": "-----BEGIN CERTIFICATE-----",
                "client_tls_key": "-----BEGIN PRIVATE KEY-----",
            },
        )

    async def test_read_config_async(self):
        mock_response = Response(200, json={"data": {"binddn": "cn=admin,dc=example,dc=com"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.ldap.read_config()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"binddn": "cn=admin,dc=example,dc=com"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ldap/config",
        )

    async def test_rotate_root_async(self):
        mock_response = Response(200, json={"data": {"message": "Root credentials rotated"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.ldap.rotate_root()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Root credentials rotated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ldap/rotate-root",
        )

    async def test_create_or_update_static_role_async(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.ldap.create_or_update_static_role(
            name="test-role",
            username="test-user",
            dn="cn=test-user,ou=users,dc=example,dc=com",
            rotation_period="24h",
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ldap/static-role/test-role",
            json={
                "username": "test-user",
                "dn": "cn=test-user,ou=users,dc=example,dc=com",
                "rotation_period": "24h",
            },
        )

    async def test_read_static_role_async(self):
        mock_response = Response(200, json={"data": {"username": "test-user"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.ldap.read_static_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"username": "test-user"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ldap/static-role/test-role",
        )

    async def test_list_static_roles_async(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.ldap.list_static_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/ldap/static-role",
        )

    async def test_delete_static_role_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.ldap.delete_static_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/ldap/static-role/test-role",
        )

    async def test_generate_static_credentials_async(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.ldap.generate_static_credentials(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ldap/static-cred/test-role",
        )

    async def test_rotate_static_credentials_async(self):
        mock_response = Response(200, json={"data": {"message": "Credentials rotated"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.ldap.rotate_static_credentials(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Credentials rotated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ldap/rotate-role/test-role",
        )
