import unittest
from unittest import mock

from httpx import Response

from vaultx.adapters import VaultxResponse
from vaultx.api.async_auth_methods.okta import Okta as AsyncOkta
from vaultx.api.auth_methods.okta import Okta


class TestOkta(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.okta = Okta(self.mock_adapter)

    def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.okta.configure(
            org_name="test_org",
            api_token="test_token",
            base_url="https://test.okta.com",
            ttl="1h",
            max_ttl="2h",
            bypass_okta_mfa=True,
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/auth/okta/config",
            json={
                "org_name": "test_org",
                "api_token": "test_token",
                "base_url": "https://test.okta.com",
                "ttl": "1h",
                "max_ttl": "2h",
                "bypass_okta_mfa": True,
            },
        )

        self.mock_adapter.post.return_value = Response(204)
        result = self.okta.configure(
            org_name="test_org",
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url="/v1/auth/okta/config",
            json={"org_name": "test_org"},
        )

    def test_read_config(self):
        mock_response = Response(200, json={"data": {"org_name": "test_org"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.okta.read_config(mount_point="okta")
        self.assertEqual(result.value, {"data": {"org_name": "test_org"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/auth/okta/config")

    def test_list_users(self):
        mock_response = Response(200, json={"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.okta.list_users(mount_point="okta")
        self.assertEqual(result.value, {"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.assert_called_once_with(url="/v1/auth/okta/users")

    def test_register_user(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.okta.register_user(
            username="test_user",
            groups=["group1", "group2"],
            policies=["policy1", "policy2"],
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/auth/okta/users/test_user",
            json={
                "username": "test_user",
                "groups": ["group1", "group2"],
                "policies": ["policy1", "policy2"],
            },
        )

        self.mock_adapter.post.return_value = Response(204)
        result = self.okta.register_user(
            username="test_user",
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url="/v1/auth/okta/users/test_user",
            json={"username": "test_user"},
        )

    def test_read_user(self):
        mock_response = Response(200, json={"data": {"username": "test_user"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.okta.read_user(username="test_user", mount_point="okta")
        self.assertEqual(result.value, {"data": {"username": "test_user"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/auth/okta/users/test_user", json={"username": "test_user"}
        )

    def test_delete_user(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.okta.delete_user(username="test_user", mount_point="okta")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/auth/okta/users/test_user", json={"username": "test_user"}
        )

    def test_list_groups(self):
        mock_response = Response(200, json={"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.okta.list_groups(mount_point="okta")
        self.assertEqual(result.value, {"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.assert_called_once_with(url="/v1/auth/okta/groups")

    def test_register_group(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.okta.register_group(
            name="test_group",
            policies=["policy1", "policy2"],
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/auth/okta/groups/test_group",
            json={"policies": ["policy1", "policy2"]},
        )

        self.mock_adapter.post.return_value = Response(204)
        result = self.okta.register_group(
            name="test_group",
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url="/v1/auth/okta/groups/test_group",
            json={},
        )

    def test_read_group(self):
        mock_response = Response(200, json={"data": {"name": "test_group"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.okta.read_group(name="test_group", mount_point="okta")
        self.assertEqual(result.value, {"data": {"name": "test_group"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/auth/okta/groups/test_group")

    def test_delete_group(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.okta.delete_group(name="test_group", mount_point="okta")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/auth/okta/groups/test_group", json={"name": "test_group"}
        )

    def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = self.okta.login(
            username="test_user",
            password="test_password",
            mount_point="okta",
        )
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once_with(
            url="/v1/auth/okta/login/test_user",
            use_token=True,
            json={"username": "test_user", "password": "test_password"},
        )


class TestAsyncOkta(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.okta = AsyncOkta(self.mock_adapter)

    async def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.okta.configure(
            org_name="test_org",
            api_token="test_token",
            base_url="https://test.okta.com",
            ttl="1h",
            max_ttl="2h",
            bypass_okta_mfa=True,
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/auth/okta/config",
            json={
                "org_name": "test_org",
                "api_token": "test_token",
                "base_url": "https://test.okta.com",
                "ttl": "1h",
                "max_ttl": "2h",
                "bypass_okta_mfa": True,
            },
        )

        self.mock_adapter.post.return_value = Response(204)
        result = await self.okta.configure(
            org_name="test_org",
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url="/v1/auth/okta/config",
            json={"org_name": "test_org"},
        )

    async def test_read_config(self):
        mock_response = Response(200, json={"data": {"org_name": "test_org"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.okta.read_config(mount_point="okta")
        self.assertEqual(result.value, {"data": {"org_name": "test_org"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/auth/okta/config")

    async def test_list_users(self):
        mock_response = Response(200, json={"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.okta.list_users(mount_point="okta")
        self.assertEqual(result.value, {"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.assert_called_once_with(url="/v1/auth/okta/users")

    async def test_register_user(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.okta.register_user(
            username="test_user",
            groups=["group1", "group2"],
            policies=["policy1", "policy2"],
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/auth/okta/users/test_user",
            json={
                "username": "test_user",
                "groups": ["group1", "group2"],
                "policies": ["policy1", "policy2"],
            },
        )

        self.mock_adapter.post.return_value = Response(204)
        result = await self.okta.register_user(
            username="test_user",
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url="/v1/auth/okta/users/test_user",
            json={"username": "test_user"},
        )

    async def test_read_user(self):
        mock_response = Response(200, json={"data": {"username": "test_user"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.okta.read_user(username="test_user", mount_point="okta")
        self.assertEqual(result.value, {"data": {"username": "test_user"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/auth/okta/users/test_user", json={"username": "test_user"}
        )

    async def test_delete_user(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.okta.delete_user(username="test_user", mount_point="okta")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/auth/okta/users/test_user", json={"username": "test_user"}
        )

    async def test_list_groups(self):
        mock_response = Response(200, json={"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.okta.list_groups(mount_point="okta")
        self.assertEqual(result.value, {"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.assert_called_once_with(url="/v1/auth/okta/groups")

    async def test_register_group(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.okta.register_group(
            name="test_group",
            policies=["policy1", "policy2"],
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/auth/okta/groups/test_group",
            json={"policies": ["policy1", "policy2"]},
        )

        self.mock_adapter.post.return_value = Response(204)
        result = await self.okta.register_group(
            name="test_group",
            mount_point="okta",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url="/v1/auth/okta/groups/test_group",
            json={},
        )

    async def test_read_group(self):
        mock_response = Response(200, json={"data": {"name": "test_group"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.okta.read_group(name="test_group", mount_point="okta")
        self.assertEqual(result.value, {"data": {"name": "test_group"}})
        self.mock_adapter.get.assert_called_once_with(url="/v1/auth/okta/groups/test_group")

    async def test_delete_group(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.okta.delete_group(name="test_group", mount_point="okta")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/auth/okta/groups/test_group", json={"name": "test_group"}
        )

    async def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = await self.okta.login(
            username="test_user",
            password="test_password",
            mount_point="okta",
        )
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once_with(
            url="/v1/auth/okta/login/test_user",
            use_token=True,
            json={"username": "test_user", "password": "test_password"},
        )
