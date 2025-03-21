import unittest
from unittest import mock
from httpx import Response
from vaultx import exceptions
from vaultx.api.auth_methods.azure import Azure
from vaultx.api.async_auth_methods.azure import Azure as AsyncAzure
from vaultx.adapters import VaultxResponse


class TestAzure(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.azure = Azure(self.mock_adapter)

    def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.azure.configure(
            tenant_id="test_tenant_id",
            resource="test_resource",
            environment="AzurePublicCloud",
            client_id="test_client_id",
            client_secret="test_client_secret",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            self.azure.configure(
                tenant_id="test_tenant_id",
                resource="test_resource",
                environment="InvalidEnvironment",
            )

    def test_read_config(self):
        mock_response = Response(200, json={"data": {"tenant_id": "test_tenant_id"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.azure.read_config()
        self.assertEqual(result, {"tenant_id": "test_tenant_id"})
        self.mock_adapter.get.assert_called_once()

    def test_delete_config(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.azure.delete_config()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_create_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.azure.create_role(
            name="test_role",
            policies=["policy1", "policy2"],
            ttl="1h",
            max_ttl="2h",
            bound_service_principal_ids=["sp1", "sp2"],
            bound_group_ids=["group1", "group2"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            self.azure.create_role(name="test_role", policies=123)  # type: ignore

    def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.azure.read_role(name="test_role")
        self.assertEqual(result, {"name": "test_role"})
        self.mock_adapter.get.assert_called_once()

    def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.azure.list_roles()
        self.assertEqual(result, {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.azure.delete_role(name="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = self.azure.login(role="test_role", jwt="test_jwt")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()


class TestAsyncAzure(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.azure = AsyncAzure(self.mock_adapter)

    async def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.azure.configure(
            tenant_id="test_tenant_id",
            resource="test_resource",
            environment="AzurePublicCloud",
            client_id="test_client_id",
            client_secret="test_client_secret",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            await self.azure.configure(
                tenant_id="test_tenant_id",
                resource="test_resource",
                environment="InvalidEnvironment",
            )

    async def test_read_config(self):
        mock_response = Response(200, json={"data": {"tenant_id": "test_tenant_id"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.azure.read_config()
        self.assertEqual(result, {"tenant_id": "test_tenant_id"})
        self.mock_adapter.get.assert_called_once()

    async def test_delete_config(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.azure.delete_config()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_create_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.azure.create_role(
            name="test_role",
            policies=["policy1", "policy2"],
            ttl="1h",
            max_ttl="2h",
            bound_service_principal_ids=["sp1", "sp2"],
            bound_group_ids=["group1", "group2"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            await self.azure.create_role(name="test_role", policies=123)  # type: ignore

    async def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.azure.read_role(name="test_role")
        self.assertEqual(result, {"name": "test_role"})
        self.mock_adapter.get.assert_called_once()

    async def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.azure.list_roles()
        self.assertEqual(result, {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    async def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.azure.delete_role(name="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = await self.azure.login(role="test_role", jwt="test_jwt")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()
