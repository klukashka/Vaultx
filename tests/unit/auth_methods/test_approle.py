import unittest
from unittest import mock

from httpx import Response

from vaultx import exceptions
from vaultx.api.async_auth_methods.approle import AppRole as AsyncAppRole
from vaultx.api.auth_methods.approle import AppRole


class TestAppRole(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.approle = AppRole(self.mock_adapter)

    def test_create_or_update_approle(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.approle.create_or_update_approle(
            role_name="test_role",
            bind_secret_id=True,
            token_policies=["policy1", "policy2"],
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            self.approle.create_or_update_approle(
                role_name="test_role",
                token_type="invalid_type",
            )

    def test_list_roles(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["role1", "role2"]}}
        result = self.approle.list_roles()
        self.assertEqual(result, {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once()

    def test_read_role(self):
        self.mock_adapter.get.return_value = {"data": {"role_name": "test_role"}}
        result = self.approle.read_role(role_name="test_role")
        self.assertEqual(result, {"data": {"role_name": "test_role"}})
        self.mock_adapter.get.assert_called_once()

    def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.approle.delete_role(role_name="test_role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_read_role_id(self):
        self.mock_adapter.get.return_value = {"data": {"role_id": "test_role_id"}}
        result = self.approle.read_role_id(role_name="test_role")
        self.assertEqual(result, {"data": {"role_id": "test_role_id"}})
        self.mock_adapter.get.assert_called_once()

    def test_update_role_id(self):
        self.mock_adapter.post.return_value = {"data": {"role_id": "new_role_id"}}
        result = self.approle.update_role_id(role_name="test_role", role_id="new_role_id")
        self.assertEqual(result, {"data": {"role_id": "new_role_id"}})
        self.mock_adapter.post.assert_called_once()

    def test_generate_secret_id(self):
        self.mock_adapter.post.return_value = {"data": {"secret_id": "test_secret_id"}}
        result = self.approle.generate_secret_id(role_name="test_role")
        self.assertEqual(result, {"data": {"secret_id": "test_secret_id"}})
        self.mock_adapter.post.assert_called_once()

    def test_create_custom_secret_id(self):
        self.mock_adapter.post.return_value = {"data": {"secret_id": "custom_secret_id"}}
        result = self.approle.create_custom_secret_id(role_name="test_role", secret_id="custom_secret_id")
        self.assertEqual(result, {"data": {"secret_id": "custom_secret_id"}})
        self.mock_adapter.post.assert_called_once()

    def test_read_secret_id(self):
        self.mock_adapter.post.return_value = {"data": {"secret_id": "test_secret_id"}}
        result = self.approle.read_secret_id(role_name="test_role", secret_id="test_secret_id")
        self.assertEqual(result, {"data": {"secret_id": "test_secret_id"}})
        self.mock_adapter.post.assert_called_once()

    def test_destroy_secret_id(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.approle.destroy_secret_id(role_name="test_role", secret_id="test_secret_id")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_list_secret_id_accessors(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["accessor1", "accessor2"]}}
        result = self.approle.list_secret_id_accessors(role_name="test_role")
        self.assertEqual(result, {"data": {"keys": ["accessor1", "accessor2"]}})
        self.mock_adapter.list.assert_called_once()

    def test_read_secret_id_accessor(self):
        self.mock_adapter.post.return_value = {"data": {"secret_id_accessor": "test_accessor"}}
        result = self.approle.read_secret_id_accessor(role_name="test_role", secret_id_accessor="test_accessor")
        self.assertEqual(result, {"data": {"secret_id_accessor": "test_accessor"}})
        self.mock_adapter.post.assert_called_once()

    def test_destroy_secret_id_accessor(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.approle.destroy_secret_id_accessor(role_name="test_role", secret_id_accessor="test_accessor")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_login(self):
        self.mock_adapter.login.return_value = {"auth": {"client_token": "test_token"}}
        result = self.approle.login(role_id="test_role_id", secret_id="test_secret_id")
        self.assertEqual(result, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()


class TestAsyncAppRole(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.approle = AsyncAppRole(self.mock_adapter)

    async def test_create_or_update_approle(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.approle.create_or_update_approle(
            role_name="test_role",
            bind_secret_id=True,
            token_policies=["policy1", "policy2"],
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            await self.approle.create_or_update_approle(
                role_name="test_role",
                token_type="invalid_type",
            )

    async def test_list_roles(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["role1", "role2"]}}
        result = await self.approle.list_roles()
        self.assertEqual(result, {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once()

    async def test_read_role(self):
        self.mock_adapter.get.return_value = {"data": {"role_name": "test_role"}}
        result = await self.approle.read_role(role_name="test_role")
        self.assertEqual(result, {"data": {"role_name": "test_role"}})
        self.mock_adapter.get.assert_called_once()

    async def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.approle.delete_role(role_name="test_role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_read_role_id(self):
        self.mock_adapter.get.return_value = {"data": {"role_id": "test_role_id"}}
        result = await self.approle.read_role_id(role_name="test_role")
        self.assertEqual(result, {"data": {"role_id": "test_role_id"}})
        self.mock_adapter.get.assert_called_once()

    async def test_update_role_id(self):
        self.mock_adapter.post.return_value = {"data": {"role_id": "new_role_id"}}
        result = await self.approle.update_role_id(role_name="test_role", role_id="new_role_id")
        self.assertEqual(result, {"data": {"role_id": "new_role_id"}})
        self.mock_adapter.post.assert_called_once()

    async def test_generate_secret_id(self):
        self.mock_adapter.post.return_value = {"data": {"secret_id": "test_secret_id"}}
        result = await self.approle.generate_secret_id(role_name="test_role")
        self.assertEqual(result, {"data": {"secret_id": "test_secret_id"}})
        self.mock_adapter.post.assert_called_once()

    async def test_create_custom_secret_id(self):
        self.mock_adapter.post.return_value = {"data": {"secret_id": "custom_secret_id"}}
        result = await self.approle.create_custom_secret_id(role_name="test_role", secret_id="custom_secret_id")
        self.assertEqual(result, {"data": {"secret_id": "custom_secret_id"}})
        self.mock_adapter.post.assert_called_once()

    async def test_read_secret_id(self):
        self.mock_adapter.post.return_value = {"data": {"secret_id": "test_secret_id"}}
        result = await self.approle.read_secret_id(role_name="test_role", secret_id="test_secret_id")
        self.assertEqual(result, {"data": {"secret_id": "test_secret_id"}})
        self.mock_adapter.post.assert_called_once()

    async def test_destroy_secret_id(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.approle.destroy_secret_id(role_name="test_role", secret_id="test_secret_id")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_list_secret_id_accessors(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["accessor1", "accessor2"]}}
        result = await self.approle.list_secret_id_accessors(role_name="test_role")
        self.assertEqual(result, {"data": {"keys": ["accessor1", "accessor2"]}})
        self.mock_adapter.list.assert_called_once()

    async def test_read_secret_id_accessor(self):
        self.mock_adapter.post.return_value = {"data": {"secret_id_accessor": "test_accessor"}}
        result = await self.approle.read_secret_id_accessor(role_name="test_role", secret_id_accessor="test_accessor")
        self.assertEqual(result, {"data": {"secret_id_accessor": "test_accessor"}})
        self.mock_adapter.post.assert_called_once()

    async def test_destroy_secret_id_accessor(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.approle.destroy_secret_id_accessor(
            role_name="test_role", secret_id_accessor="test_accessor"
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_login(self):
        self.mock_adapter.login.return_value = {"auth": {"client_token": "test_token"}}
        result = await self.approle.login(role_id="test_role_id", secret_id="test_secret_id")
        self.assertEqual(result, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()
