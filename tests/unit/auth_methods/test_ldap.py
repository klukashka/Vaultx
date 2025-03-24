import unittest
from unittest import mock

from httpx import Response

from vaultx import exceptions
from vaultx.adapters import VaultxResponse
from vaultx.api.async_auth_methods.ldap import Ldap as AsyncLdap
from vaultx.api.auth_methods.ldap import Ldap


class TestLdap(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.ldap = Ldap(self.mock_adapter)
        self.default_mount_point = "ldap"

    def test_configure(self):
        # Test successful configuration
        self.mock_adapter.post.return_value = Response(204)
        result = self.ldap.configure(
            userdn="ou=Users,dc=example,dc=com",
            groupdn="ou=Groups,dc=example,dc=com",
            url="ldap://ldap.example.com",
            mount_point=self.default_mount_point,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        # Test with all optional parameters
        self.mock_adapter.post.return_value = Response(204)
        result = self.ldap.configure(
            userdn="ou=Users,dc=example,dc=com",
            groupdn="ou=Groups,dc=example,dc=com",
            url="ldap://ldap.example.com",
            case_sensitive_names=True,
            starttls=True,
            tls_min_version="tls12",
            tls_max_version="tls12",
            insecure_tls=False,
            certificate="test_cert",
            binddn="cn=admin,dc=example,dc=com",
            bindpass="test_password",
            userattr="uid",
            discoverdn=True,
            deny_null_bind=False,
            upndomain="example.com",
            groupfilter="(&(objectClass=group)(member={{.UserDN}}))",
            groupattr="member",
            use_token_groups=True,
            token_ttl="1h",
            token_max_ttl="2h",
            mount_point=self.default_mount_point,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url=f"/v1/auth/{self.default_mount_point}/config",
            json={
                "userdn": "ou=Users,dc=example,dc=com",
                "groupdn": "ou=Groups,dc=example,dc=com",
                "url": "ldap://ldap.example.com",
                "case_sensitive_names": True,
                "starttls": True,
                "tls_min_version": "tls12",
                "tls_max_version": "tls12",
                "insecure_tls": False,
                "certificate": "test_cert",
                "binddn": "cn=admin,dc=example,dc=com",
                "bindpass": "test_password",
                "userattr": "uid",
                "discoverdn": True,
                "deny_null_bind": False,
                "upndomain": "example.com",
                "groupfilter": "(&(objectClass=group)(member={{.UserDN}}))",
                "groupattr": "member",
                "use_token_groups": True,
                "token_ttl": "1h",
                "token_max_ttl": "2h",
            },
        )

    def test_read_configuration(self):
        # Test successful read
        mock_response = Response(200, json={"data": {"userdn": "ou=Users,dc=example,dc=com"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.ldap.read_configuration(mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"data": {"userdn": "ou=Users,dc=example,dc=com"}})
        self.mock_adapter.get.assert_called_once()

        # Test with custom mount point
        custom_mount_point = "custom-ldap"
        mock_response = Response(200, json={"data": {"userdn": "ou=Users,dc=example,dc=com"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.ldap.read_configuration(mount_point=custom_mount_point)
        self.assertEqual(result.value, {"data": {"userdn": "ou=Users,dc=example,dc=com"}})
        self.mock_adapter.get.assert_called_with(url=f"/v1/auth/{custom_mount_point}/config")

    def test_create_or_update_group(self):
        # Test successful group creation/update
        self.mock_adapter.post.return_value = Response(204)
        result = self.ldap.create_or_update_group(
            name="test_group", policies=["policy1"], mount_point=self.default_mount_point
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        # Test with empty policies
        self.mock_adapter.post.return_value = Response(204)
        result = self.ldap.create_or_update_group(name="test_group", policies=[], mount_point=self.default_mount_point)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url=f"/v1/auth/{self.default_mount_point}/groups/test_group",
            json={"policies": ""},
        )

        # Test with invalid policies type
        with self.assertRaises(exceptions.VaultxError):
            self.ldap.create_or_update_group(
                name="test_group", policies="policy1", mount_point=self.default_mount_point  # type: ignore
            )

    def test_list_groups(self):
        # Test successful list
        mock_response = Response(200, json={"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.ldap.list_groups(mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.assert_called_once()

    def test_read_group(self):
        # Test successful read
        mock_response = Response(200, json={"data": {"name": "test_group"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.ldap.read_group(name="test_group", mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"data": {"name": "test_group"}})
        self.mock_adapter.get.assert_called_once()

    def test_delete_group(self):
        # Test successful delete
        self.mock_adapter.delete.return_value = Response(204)
        result = self.ldap.delete_group(name="test_group", mount_point=self.default_mount_point)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_create_or_update_user(self):
        # Test successful user creation/update
        self.mock_adapter.post.return_value = Response(204)
        result = self.ldap.create_or_update_user(
            username="test_user", policies=["policy1"], mount_point=self.default_mount_point
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        # Test with groups
        self.mock_adapter.post.return_value = Response(204)
        result = self.ldap.create_or_update_user(
            username="test_user", policies=["policy1"], groups=["group1"], mount_point=self.default_mount_point
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url=f"/v1/auth/{self.default_mount_point}/users/test_user",
            json={"policies": "policy1", "groups": "group1"},
        )

        # Test with invalid policies type
        with self.assertRaises(exceptions.VaultxError):
            self.ldap.create_or_update_user(
                username="test_user", policies="policy1", mount_point=self.default_mount_point  # type: ignore
            )

    def test_list_users(self):
        # Test successful list
        mock_response = Response(200, json={"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.ldap.list_users(mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.assert_called_once()

    def test_read_user(self):
        # Test successful read
        mock_response = Response(200, json={"data": {"username": "test_user"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.ldap.read_user(username="test_user", mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"data": {"username": "test_user"}})
        self.mock_adapter.get.assert_called_once()

    def test_delete_user(self):
        # Test successful delete
        self.mock_adapter.delete.return_value = Response(204)
        result = self.ldap.delete_user(username="test_user", mount_point=self.default_mount_point)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_login(self):
        # Test successful login
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = self.ldap.login(username="test_user", password="test_password", mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()


class TestAsyncLdap(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.ldap = AsyncLdap(self.mock_adapter)
        self.default_mount_point = "ldap"

    async def test_configure(self):
        # Test successful configuration
        self.mock_adapter.post.return_value = Response(204)
        result = await self.ldap.configure(
            userdn="ou=Users,dc=example,dc=com",
            groupdn="ou=Groups,dc=example,dc=com",
            url="ldap://ldap.example.com",
            mount_point=self.default_mount_point,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_configuration(self):
        # Test successful read
        mock_response = Response(200, json={"data": {"userdn": "ou=Users,dc=example,dc=com"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.ldap.read_configuration(mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"data": {"userdn": "ou=Users,dc=example,dc=com"}})
        self.mock_adapter.get.assert_called_once()

    async def test_create_or_update_group(self):
        # Test successful group creation/update
        self.mock_adapter.post.return_value = Response(204)
        result = await self.ldap.create_or_update_group(
            name="test_group", policies=["policy1"], mount_point=self.default_mount_point
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_list_groups(self):
        # Test successful list
        mock_response = Response(200, json={"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.ldap.list_groups(mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.assert_called_once()

    async def test_read_group(self):
        # Test successful read
        mock_response = Response(200, json={"data": {"name": "test_group"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.ldap.read_group(name="test_group", mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"data": {"name": "test_group"}})
        self.mock_adapter.get.assert_called_once()

    async def test_delete_group(self):
        # Test successful delete
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.ldap.delete_group(name="test_group", mount_point=self.default_mount_point)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_create_or_update_user(self):
        # Test successful user creation/update
        self.mock_adapter.post.return_value = Response(204)
        result = await self.ldap.create_or_update_user(
            username="test_user", policies=["policy1"], mount_point=self.default_mount_point
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_list_users(self):
        # Test successful list
        mock_response = Response(200, json={"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.ldap.list_users(mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"data": {"keys": ["user1", "user2"]}})
        self.mock_adapter.list.assert_called_once()

    async def test_read_user(self):
        # Test successful read
        mock_response = Response(200, json={"data": {"username": "test_user"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.ldap.read_user(username="test_user", mount_point=self.default_mount_point)
        self.assertEqual(result.value, {"data": {"username": "test_user"}})
        self.mock_adapter.get.assert_called_once()

    async def test_delete_user(self):
        # Test successful delete
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.ldap.delete_user(username="test_user", mount_point=self.default_mount_point)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_login(self):
        # Test successful login
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = await self.ldap.login(
            username="test_user", password="test_password", mount_point=self.default_mount_point
        )
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()
