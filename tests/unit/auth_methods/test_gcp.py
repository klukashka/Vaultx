import unittest
from unittest import mock

from httpx import Response

from vaultx import exceptions
from vaultx.adapters import VaultxResponse
from vaultx.api.async_auth_methods.gcp import Gcp as AsyncGcp
from vaultx.api.auth_methods.gcp import Gcp


class TestGcp(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.gcp = Gcp(self.mock_adapter)

    def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.gcp.configure(credentials="test_credentials")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_config(self):
        mock_response = Response(200, json={"data": {"credentials": "test_credentials"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.gcp.read_config()
        self.assertEqual(result, {"credentials": "test_credentials"})
        self.mock_adapter.get.assert_called_once()

    def test_delete_config(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.gcp.delete_config()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_create_role_iam(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.gcp.create_role(
            name="test_role",
            role_type="iam",
            project_id="test_project",
            bound_service_accounts=["sa1@test.com", "sa2@test.com"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_create_role_gce(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.gcp.create_role(
            name="test_role",
            role_type="gce",
            project_id="test_project",
            bound_zones=["us-central1-a"],
            bound_regions=["us-central1"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_create_role_invalid_type(self):
        with self.assertRaises(exceptions.VaultxError):
            self.gcp.create_role(
                name="test_role",
                role_type="invalid_type",
                project_id="test_project",
            )

    def test_edit_service_accounts_on_iam_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.gcp.edit_service_accounts_on_iam_role(
            name="test_role",
            add=["sa1@test.com"],
            remove=["sa2@test.com"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_edit_labels_on_gce_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.gcp.edit_labels_on_gce_role(
            name="test_role",
            add=["key1:value1"],
            remove=["key2"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.gcp.read_role(name="test_role")
        self.assertEqual(result, {"name": "test_role"})
        self.mock_adapter.get.assert_called_once()

    def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.gcp.list_roles()
        self.assertEqual(result, {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.gcp.delete_role(role="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = self.gcp.login(role="test_role", jwt="test_jwt")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()


class TestAsyncGcp(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.gcp = AsyncGcp(self.mock_adapter)

    async def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.gcp.configure(credentials="test_credentials")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_config(self):
        mock_response = Response(200, json={"data": {"credentials": "test_credentials"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.gcp.read_config()
        self.assertEqual(result, {"credentials": "test_credentials"})
        self.mock_adapter.get.assert_called_once()

    async def test_delete_config(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.gcp.delete_config()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_create_role_iam(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.gcp.create_role(
            name="test_role",
            role_type="iam",
            project_id="test_project",
            bound_service_accounts=["sa1@test.com", "sa2@test.com"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_create_role_gce(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.gcp.create_role(
            name="test_role",
            role_type="gce",
            project_id="test_project",
            bound_zones=["us-central1-a"],
            bound_regions=["us-central1"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_create_role_invalid_type(self):
        with self.assertRaises(exceptions.VaultxError):
            await self.gcp.create_role(
                name="test_role",
                role_type="invalid_type",
                project_id="test_project",
            )

    async def test_edit_service_accounts_on_iam_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.gcp.edit_service_accounts_on_iam_role(
            name="test_role",
            add=["sa1@test.com"],
            remove=["sa2@test.com"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_edit_labels_on_gce_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.gcp.edit_labels_on_gce_role(
            name="test_role",
            add=["key1:value1"],
            remove=["key2"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.gcp.read_role(name="test_role")
        self.assertEqual(result, {"name": "test_role"})
        self.mock_adapter.get.assert_called_once()

    async def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.gcp.list_roles()
        self.assertEqual(result, {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    async def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.gcp.delete_role(role="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = await self.gcp.login(role="test_role", jwt="test_jwt")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()
