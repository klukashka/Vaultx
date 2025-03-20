import json
import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.azure import Azure as AsyncAzure
from vaultx.api.secrets_engines.azure import Azure
from vaultx.exceptions import VaultxError


class TestAzure(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.azure = Azure(self.mock_adapter)

    def test_configure_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "subscription_id": "test-subscription-id",
            "tenant_id": "test-tenant-id",
            "client_id": "test-client-id",
            "client_secret": "test-client-secret",
            "environment": "AzurePublicCloud",
        }
        result = self.azure.configure(**params)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/azure/config",
            json=params,
        )

    def test_configure_with_invalid_environment_raises_error(self):
        with self.assertRaises(VaultxError) as context:
            self.azure.configure(
                subscription_id="test-subscription-id",
                tenant_id="test-tenant-id",
                environment="InvalidEnvironment",
            )

        self.assertEqual(
            str(context.exception),
            'invalid environment argument provided "InvalidEnvironment", supported environments: '
            '"AzurePublicCloud,AzureUSGovernmentCloud,AzureChinaCloud,AzureGermanCloud"',
        )

    def test_read_config_returns_response(self):
        mock_response = {"data": {"subscription_id": "test-subscription-id"}}
        self.mock_adapter.get.return_value = mock_response

        result = self.azure.read_config()
        self.assertEqual(result, {"subscription_id": "test-subscription-id"})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/azure/config",
        )

    def test_delete_config_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.azure.delete_config()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/azure/config",
        )

    def test_create_or_update_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "azure_roles": [{"role_name": "Contributor", "scope": "/subscriptions/test-subscription-id"}],
            "ttl": "1h",
            "max_ttl": "24h",
        }
        result = self.azure.create_or_update_role(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "azure_roles": json.dumps(params["azure_roles"]),
            "ttl": "1h",
            "max_ttl": "24h",
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/azure/roles/test-role",
            json=expected_params,
        )

    def test_list_roles_returns_response(self):
        mock_response = {"data": {"keys": ["role1", "role2"]}}
        self.mock_adapter.list.return_value = mock_response

        result = self.azure.list_roles()
        self.assertEqual(result, {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/azure/roles",
        )

    def test_generate_credentials_returns_response(self):
        mock_response = {"data": {"client_id": "test-client-id", "client_secret": "test-secret"}}
        self.mock_adapter.get.return_value = mock_response

        result = self.azure.generate_credentials(name="test-role")
        self.assertEqual(result, {"client_id": "test-client-id", "client_secret": "test-secret"})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/azure/creds/test-role",
        )


class TestAsyncAzure(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.azure = AsyncAzure(self.mock_adapter)

    async def test_configure_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "subscription_id": "test-subscription-id",
            "tenant_id": "test-tenant-id",
            "client_id": "test-client-id",
            "client_secret": "test-client-secret",
            "environment": "AzurePublicCloud",
        }
        result = await self.azure.configure(**params)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/azure/config",
            json=params,
        )

    async def test_read_config_returns_response(self):
        mock_response = {"data": {"subscription_id": "test-subscription-id"}}
        self.mock_adapter.get.return_value = mock_response

        result = await self.azure.read_config()
        self.assertEqual(result, {"subscription_id": "test-subscription-id"})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/azure/config",
        )

    async def test_delete_config_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.azure.delete_config()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/azure/config",
        )

    async def test_create_or_update_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "azure_roles": [{"role_name": "Contributor", "scope": "/subscriptions/test-subscription-id"}],
            "ttl": "1h",
            "max_ttl": "24h",
        }
        result = await self.azure.create_or_update_role(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "azure_roles": json.dumps(params["azure_roles"]),
            "ttl": "1h",
            "max_ttl": "24h",
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/azure/roles/test-role",
            json=expected_params,
        )

    async def test_list_roles_returns_response(self):
        mock_response = {"data": {"keys": ["role1", "role2"]}}
        self.mock_adapter.list.return_value = mock_response

        result = await self.azure.list_roles()
        self.assertEqual(result, {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/azure/roles",
        )

    async def test_generate_credentials_returns_response(self):
        mock_response = {"data": {"client_id": "test-client-id", "client_secret": "test-secret"}}
        self.mock_adapter.get.return_value = mock_response

        result = await self.azure.generate_credentials(name="test-role")
        self.assertEqual(result, {"client_id": "test-client-id", "client_secret": "test-secret"})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/azure/creds/test-role",
        )
