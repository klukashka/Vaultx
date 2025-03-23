import unittest
from unittest import mock

from httpx import Response

from vaultx import exceptions
from vaultx.adapters import VaultxResponse
from vaultx.api.async_auth_methods.radius import Radius as AsyncRadius
from vaultx.api.auth_methods.radius import Radius


class TestRadius(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.radius = Radius(self.mock_adapter)

    def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.radius.configure(
            host="radius.example.com",
            secret="test_secret",
            port=1812,
            unregistered_user_policies=["policy1", "policy2"],
            dial_timeout=10,
            nas_port=10,
            mount_point="radius",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/auth/radius/config",
            json={
                "host": "radius.example.com",
                "secret": "test_secret",
                "port": 1812,
                "unregistered_user_policies": "policy1,policy2",
                "dial_timeout": 10,
                "nas_port": 10,
            },
        )

        self.mock_adapter.post.return_value = Response(204)
        result = self.radius.configure(
            host="radius.example.com",
            secret="test_secret",
            mount_point="radius",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url="/v1/auth/radius/config",
            json={
                "host": "radius.example.com",
                "secret": "test_secret",
            },
        )

        with self.assertRaises(exceptions.VaultxError) as context:
            self.radius.configure(
                host="radius.example.com",
                secret="test_secret",
                unregistered_user_policies="policy1",  # type: ignore
                mount_point="radius",
            )
        self.assertIn(
            '"unregistered_user_policies" argument must be an instance of list or None', str(context.exception)
        )

    def test_read_configuration(self):
        mock_response = Response(200, json={"data": {"host": "radius.example.com"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.radius.read_configuration(mount_point="radius")
        self.assertEqual(result.value, {"data": {"host": "radius.example.com"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/auth/radius/config")

    def test_register_user(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.radius.register_user(
            username="test_user",
            policies=["policy1", "policy2"],
            mount_point="radius",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/auth/radius/users/test_user",
            json={"policies": "policy1,policy2"},
        )

        self.mock_adapter.post.return_value = Response(204)
        result = self.radius.register_user(
            username="test_user",
            mount_point="radius",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url="/v1/auth/radius/users/test_user",
            json={},
        )

        with self.assertRaises(exceptions.VaultxError) as context:
            self.radius.register_user(
                username="test_user",
                policies="policy1",  # type: ignore
                mount_point="radius",
            )
        self.assertIn('"policies" argument must be an instance of list or None', str(context.exception))

    def test_list_users(self):
        mock_response = Response(200, json={"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.radius.list_users(mount_point="radius")
        self.assertEqual(result.value, {"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.assert_called_once_with(url="/v1/auth/radius/users")

    def test_read_user(self):
        mock_response = Response(200, json={"data": {"username": "test_user"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.radius.read_user(username="test_user", mount_point="radius")
        self.assertEqual(result.value, {"data": {"username": "test_user"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/auth/radius/users/test_user")

    def test_delete_user(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.radius.delete_user(username="test_user", mount_point="radius")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/auth/radius/users/test_user")

    def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = self.radius.login(
            username="test_user",
            password="test_password",
            mount_point="radius",
        )
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once_with(
            url="/v1/auth/radius/login/test_user",
            use_token=True,
            json={"password": "test_password"},
        )


class TestAsyncRadius(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.radius = AsyncRadius(self.mock_adapter)

    async def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.radius.configure(
            host="radius.example.com",
            secret="test_secret",
            port=1812,
            unregistered_user_policies=["policy1", "policy2"],
            dial_timeout=10,
            nas_port=10,
            mount_point="radius",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/auth/radius/config",
            json={
                "host": "radius.example.com",
                "secret": "test_secret",
                "port": 1812,
                "unregistered_user_policies": "policy1,policy2",
                "dial_timeout": 10,
                "nas_port": 10,
            },
        )

        self.mock_adapter.post.return_value = Response(204)
        result = await self.radius.configure(
            host="radius.example.com",
            secret="test_secret",
            mount_point="radius",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url="/v1/auth/radius/config",
            json={
                "host": "radius.example.com",
                "secret": "test_secret",
            },
        )

        with self.assertRaises(exceptions.VaultxError) as context:
            await self.radius.configure(
                host="radius.example.com",
                secret="test_secret",
                unregistered_user_policies="policy1",  # type: ignore
                mount_point="radius",
            )
        self.assertIn(
            '"unregistered_user_policies" argument must be an instance of list or None', str(context.exception)
        )

    async def test_read_configuration(self):
        mock_response = Response(200, json={"data": {"host": "radius.example.com"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.radius.read_configuration(mount_point="radius")
        self.assertEqual(result.value, {"data": {"host": "radius.example.com"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/auth/radius/config")

    async def test_register_user(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.radius.register_user(
            username="test_user",
            policies=["policy1", "policy2"],
            mount_point="radius",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/auth/radius/users/test_user",
            json={"policies": "policy1,policy2"},
        )

        self.mock_adapter.post.return_value = Response(204)
        result = await self.radius.register_user(
            username="test_user",
            mount_point="radius",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url="/v1/auth/radius/users/test_user",
            json={},
        )

        with self.assertRaises(exceptions.VaultxError) as context:
            await self.radius.register_user(
                username="test_user",
                policies="policy1",  # type: ignore
                mount_point="radius",
            )
        self.assertIn('"policies" argument must be an instance of list or None', str(context.exception))

    async def test_list_users(self):
        mock_response = Response(200, json={"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.radius.list_users(mount_point="radius")
        self.assertEqual(result.value, {"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.assert_called_once_with(url="/v1/auth/radius/users")

    async def test_read_user(self):
        mock_response = Response(200, json={"data": {"username": "test_user"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.radius.read_user(username="test_user", mount_point="radius")
        self.assertEqual(result.value, {"data": {"username": "test_user"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/auth/radius/users/test_user")

    async def test_delete_user(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.radius.delete_user(username="test_user", mount_point="radius")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/auth/radius/users/test_user")

    async def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = await self.radius.login(
            username="test_user",
            password="test_password",
            mount_point="radius",
        )
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once_with(
            url="/v1/auth/radius/login/test_user",
            use_token=True,
            json={"password": "test_password"},
        )
