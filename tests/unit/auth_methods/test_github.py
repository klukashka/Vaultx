import unittest
from unittest import mock

from httpx import Response

from vaultx import exceptions
from vaultx.adapters import VaultxResponse
from vaultx.api.async_auth_methods.github import Github as AsyncGithub
from vaultx.api.auth_methods.github import Github


class TestGithub(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.github = Github(self.mock_adapter)

    def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.github.configure(organization="test_org")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_configuration(self):
        mock_response = Response(200, json={"data": {"organization": "test_org"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.github.read_configuration()
        self.assertEqual(result.value["data"], {"organization": "test_org"})
        self.mock_adapter.get.assert_called_once()

    def test_map_team(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.github.map_team(team_name="test_team", policies=["policy1", "policy2"])
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            self.github.map_team(team_name="test_team", policies="invalid_policies")  # type: ignore

    def test_read_team_mapping(self):
        mock_response = Response(200, json={"data": {"value": "policy1,policy2"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.github.read_team_mapping(team_name="test_team")
        self.assertEqual(result.value["data"], {"value": "policy1,policy2"})
        self.mock_adapter.get.assert_called_once()

    def test_map_user(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.github.map_user(user_name="test_user", policies=["policy1", "policy2"])
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            self.github.map_user(user_name="test_user", policies="invalid_policies")  # type: ignore

    def test_read_user_mapping(self):
        mock_response = Response(200, json={"data": {"value": "policy1,policy2"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.github.read_user_mapping(user_name="test_user")
        self.assertEqual(result.value["data"], {"value": "policy1,policy2"})
        self.mock_adapter.get.assert_called_once()

    def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = self.github.login(token="test_token")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()


class TestAsyncGithub(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.github = AsyncGithub(self.mock_adapter)

    async def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.github.configure(organization="test_org")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_configuration(self):
        mock_response = Response(200, json={"data": {"organization": "test_org"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.github.read_configuration()
        self.assertEqual(result.value["data"], {"organization": "test_org"})
        self.mock_adapter.get.assert_called_once()

    async def test_map_team(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.github.map_team(team_name="test_team", policies=["policy1", "policy2"])
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            await self.github.map_team(team_name="test_team", policies="invalid_policies")  # type: ignore

    async def test_read_team_mapping(self):
        mock_response = Response(200, json={"data": {"value": "policy1,policy2"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.github.read_team_mapping(team_name="test_team")
        self.assertEqual(result.value["data"], {"value": "policy1,policy2"})
        self.mock_adapter.get.assert_called_once()

    async def test_map_user(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.github.map_user(user_name="test_user", policies=["policy1", "policy2"])
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            await self.github.map_user(user_name="test_user", policies="invalid_policies")  # type: ignore

    async def test_read_user_mapping(self):
        mock_response = Response(200, json={"data": {"value": "policy1,policy2"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.github.read_user_mapping(user_name="test_user")
        self.assertEqual(result.value["data"], {"value": "policy1,policy2"})
        self.mock_adapter.get.assert_called_once()

    async def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = await self.github.login(token="test_token")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()
