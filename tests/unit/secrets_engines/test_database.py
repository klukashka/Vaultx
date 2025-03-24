import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.database import Database as AsyncDatabase
from vaultx.api.secrets_engines.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.database = Database(self.mock_adapter)

    def test_configure_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-connection",
            "plugin_name": "postgresql-database-plugin",
            "verify_connection": True,
            "allowed_roles": ["role1", "role2"],
            "root_rotation_statements": ["ALTER USER WITH PASSWORD '{{password}}';"],
        }
        result = self.database.configure(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "plugin_name": "postgresql-database-plugin",
            "verify_connection": True,
            "allowed_roles": ["role1", "role2"],
            "root_rotation_statements": ["ALTER USER WITH PASSWORD '{{password}}';"],
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/config/test-connection",
            json=expected_params,
        )

    def test_rotate_root_credentials_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.database.rotate_root_credentials(name="test-connection")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/rotate-root/test-connection",
        )

    def test_read_connection_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-connection"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.database.read_connection(name="test-connection")
        self.assertEqual(result.json(), {"data": {"name": "test-connection"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/database/config/test-connection",
        )

    def test_list_connections_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["connection1", "connection2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.database.list_connections()
        self.assertEqual(result.json(), {"data": {"keys": ["connection1", "connection2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/database/config",
        )

    def test_delete_connection_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.database.delete_connection(name="test-connection")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/database/config/test-connection",
        )

    def test_reset_connection_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.database.reset_connection(name="test-connection")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/reset/test-connection",
        )

    def test_create_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "db_name": "test-connection",
            "creation_statements": ["CREATE USER '{{name}}' WITH PASSWORD '{{password}}';"],
            "default_ttl": 3600,
            "max_ttl": 86400,
            "revocation_statements": ["DROP USER '{{name}}';"],
            "rollback_statements": ["DROP USER '{{name}}';"],
            "renew_statements": ["ALTER USER '{{name}}' WITH PASSWORD '{{password}}';"],
        }
        result = self.database.create_role(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "db_name": "test-connection",
            "creation_statements": ["CREATE USER '{{name}}' WITH PASSWORD '{{password}}';"],
            "default_ttl": 3600,
            "max_ttl": 86400,
            "revocation_statements": ["DROP USER '{{name}}';"],
            "rollback_statements": ["DROP USER '{{name}}';"],
            "renew_statements": ["ALTER USER '{{name}}' WITH PASSWORD '{{password}}';"],
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/roles/test-role",
            json=expected_params,
        )

    def test_create_static_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-static-role",
            "db_name": "test-connection",
            "username": "test-user",
            "rotation_statements": ["ALTER USER '{{name}}' WITH PASSWORD '{{password}}';"],
            "rotation_period": 86400,
        }
        result = self.database.create_static_role(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "db_name": "test-connection",
            "username": "test-user",
            "rotation_statements": ["ALTER USER '{{name}}' WITH PASSWORD '{{password}}';"],
            "rotation_period": 86400,
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/static-roles/test-static-role",
            json=expected_params,
        )

    def test_read_role_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.database.read_role(name="test-role")
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/database/roles/test-role",
        )

    def test_read_static_role_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-static-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.database.read_static_role(name="test-static-role")
        self.assertEqual(result.json(), {"data": {"name": "test-static-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/database/static-roles/test-static-role",
        )

    def test_list_roles_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.database.list_roles()
        self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/database/roles",
        )

    def test_list_static_roles_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["static-role1", "static-role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.database.list_static_roles()
        self.assertEqual(result.json(), {"data": {"keys": ["static-role1", "static-role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/database/static-roles",
        )

    def test_delete_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.database.delete_role(name="test-role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/database/roles/test-role",
        )

    def test_delete_static_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.database.delete_static_role(name="test-static-role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/database/static-roles/test-static-role",
        )

    def test_generate_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.database.generate_credentials(name="test-role")
        self.assertEqual(result.json(), {"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/database/creds/test-role",
        )

    def test_get_static_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.database.get_static_credentials(name="test-static-role")
        self.assertEqual(result.json(), {"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/database/static-creds/test-static-role",
        )

    def test_rotate_static_role_credentials_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.database.rotate_static_role_credentials(name="test-static-role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/rotate-role/test-static-role",
        )


class TestAsyncDatabase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.database = AsyncDatabase(self.mock_adapter)

    async def test_configure_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-connection",
            "plugin_name": "postgresql-database-plugin",
            "verify_connection": True,
            "allowed_roles": ["role1", "role2"],
            "root_rotation_statements": ["ALTER USER WITH PASSWORD '{{password}}';"],
        }
        result = await self.database.configure(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "plugin_name": "postgresql-database-plugin",
            "verify_connection": True,
            "allowed_roles": ["role1", "role2"],
            "root_rotation_statements": ["ALTER USER WITH PASSWORD '{{password}}';"],
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/config/test-connection",
            json=expected_params,
        )

    async def test_rotate_root_credentials_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.database.rotate_root_credentials(name="test-connection")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/rotate-root/test-connection",
        )

    async def test_read_connection_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-connection"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.database.read_connection(name="test-connection")
        self.assertEqual(result.json(), {"data": {"name": "test-connection"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/database/config/test-connection",
        )

    async def test_list_connections_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["connection1", "connection2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.database.list_connections()
        self.assertEqual(result.json(), {"data": {"keys": ["connection1", "connection2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/database/config",
        )

    async def test_delete_connection_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.database.delete_connection(name="test-connection")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/database/config/test-connection",
        )

    async def test_reset_connection_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.database.reset_connection(name="test-connection")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/reset/test-connection",
        )

    async def test_create_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "db_name": "test-connection",
            "creation_statements": ["CREATE USER '{{name}}' WITH PASSWORD '{{password}}';"],
            "default_ttl": 3600,
            "max_ttl": 86400,
            "revocation_statements": ["DROP USER '{{name}}';"],
            "rollback_statements": ["DROP USER '{{name}}';"],
            "renew_statements": ["ALTER USER '{{name}}' WITH PASSWORD '{{password}}';"],
        }
        result = await self.database.create_role(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "db_name": "test-connection",
            "creation_statements": ["CREATE USER '{{name}}' WITH PASSWORD '{{password}}';"],
            "default_ttl": 3600,
            "max_ttl": 86400,
            "revocation_statements": ["DROP USER '{{name}}';"],
            "rollback_statements": ["DROP USER '{{name}}';"],
            "renew_statements": ["ALTER USER '{{name}}' WITH PASSWORD '{{password}}';"],
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/roles/test-role",
            json=expected_params,
        )

    async def test_create_static_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-static-role",
            "db_name": "test-connection",
            "username": "test-user",
            "rotation_statements": ["ALTER USER '{{name}}' WITH PASSWORD '{{password}}';"],
            "rotation_period": 86400,
        }
        result = await self.database.create_static_role(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)

        expected_params = {
            "db_name": "test-connection",
            "username": "test-user",
            "rotation_statements": ["ALTER USER '{{name}}' WITH PASSWORD '{{password}}';"],
            "rotation_period": 86400,
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/static-roles/test-static-role",
            json=expected_params,
        )

    async def test_read_role_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.database.read_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/database/roles/test-role",
        )

    async def test_read_static_role_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-static-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.database.read_static_role(name="test-static-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-static-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/database/static-roles/test-static-role",
        )

    async def test_list_roles_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.database.list_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/database/roles",
        )

    async def test_list_static_roles_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["static-role1", "static-role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.database.list_static_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["static-role1", "static-role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/database/static-roles",
        )

    async def test_delete_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.database.delete_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/database/roles/test-role",
        )

    async def test_delete_static_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.database.delete_static_role(name="test-static-role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/database/static-roles/test-static-role",
        )

    async def test_generate_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.database.generate_credentials(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/database/creds/test-role",
        )

    async def test_get_static_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.database.get_static_credentials(name="test-static-role")
        self.assertEqual(result.json(), {"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/database/static-creds/test-static-role",
        )

    async def test_rotate_static_role_credentials_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.database.rotate_static_role_credentials(name="test-static-role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/database/rotate-role/test-static-role",
        )
