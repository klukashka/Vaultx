import unittest
from unittest import mock

from httpx import Response

from vaultx.adapters import Adapter
from vaultx.api.async_auth_methods.userpass import Userpass as AsyncUserpass
from vaultx.api.auth_methods.userpass import Userpass


class TestUserpass(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock(spec=Adapter)
        self.userpass = Userpass(adapter=self.mock_adapter)

    def test_create_or_update_user(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.userpass.create_or_update_user(
            username="test_user",
            password="test_password",
            policies="policy1,policy2",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_list_user(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["user1", "user2"]}}
        result = self.userpass.list_user()
        self.assertEqual(result, {"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.assert_called_once()

    def test_read_user(self):
        # Test reading a user
        self.mock_adapter.get.return_value = {"data": {"username": "test_user"}}
        result = self.userpass.read_user(username="test_user")
        self.assertEqual(result, {"data": {"username": "test_user"}})
        self.mock_adapter.get.assert_called_once()

    def test_delete_user(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.userpass.delete_user(username="test_user")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_update_password_on_user(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.userpass.update_password_on_user(
            username="test_user",
            password="new_password",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_login(self):
        self.mock_adapter.login.return_value = {"auth": {"client_token": "test_token"}}
        result = self.userpass.login(
            username="test_user",
            password="test_password",
        )
        self.assertEqual(result, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()


class TestAsyncUserpass(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.userpass = AsyncUserpass(self.mock_adapter)

    async def test_create_or_update_user(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.userpass.create_or_update_user(
            username="test_user",
            password="test_password",
            policies="policy1,policy2",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_list_user(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["user1", "user2"]}}
        result = await self.userpass.list_user()
        self.assertEqual(result, {"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.assert_called_once()

    async def test_read_user(self):
        self.mock_adapter.get.return_value = {"data": {"username": "test_user"}}
        result = await self.userpass.read_user(username="test_user")
        self.assertEqual(result, {"data": {"username": "test_user"}})
        self.mock_adapter.get.assert_called_once()

    async def test_delete_user(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.userpass.delete_user(username="test_user")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_update_password_on_user(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.userpass.update_password_on_user(
            username="test_user",
            password="new_password",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_login(self):
        self.mock_adapter.login.return_value = {"auth": {"client_token": "test_token"}}
        result = await self.userpass.login(
            username="test_user",
            password="test_password",
        )
        self.assertEqual(result, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()
