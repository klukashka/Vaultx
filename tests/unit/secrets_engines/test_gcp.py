import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.gcp import Gcp as AsyncGcp
from vaultx.api.secrets_engines.gcp import Gcp
from vaultx.exceptions import VaultxError


class TestGcp(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.gcp = Gcp(self.mock_adapter)

    def test_configure_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "credentials": "test-credentials",
            "ttl": "1h",
            "max_ttl": "24h",
        }
        result = self.gcp.configure(**params)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/config",
            json=params,
        )

    def test_rotate_root_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"new_key": "test-key"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.gcp.rotate_root_credentials()
        self.assertEqual(result.json(), {"data": {"new_key": "test-key"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/config/rotate-root",
        )

    def test_read_config_returns_response(self):
        mock_response = Response(200, json={"data": {"ttl": "1h"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.gcp.read_config()
        self.assertEqual(result.json(), {"data": {"ttl": "1h"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/config",
        )

    def test_create_or_update_roleset_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-roleset",
            "project": "test-project",
            "bindings": '{"role": "roles/viewer"}',
            "secret_type": "access_token",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
        }
        result = self.gcp.create_or_update_roleset(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "project": "test-project",
            "bindings": '{"role": "roles/viewer"}',
            "secret_type": "access_token",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/roleset/test-roleset",
            json=expected_params,
        )

    def test_create_or_update_roleset_with_invalid_secret_type_raises_error(self):
        with self.assertRaises(VaultxError) as context:
            self.gcp.create_or_update_roleset(
                name="test-roleset",
                project="test-project",
                bindings='{"role": "roles/viewer"}',
                secret_type="invalid_type",
            )

        self.assertEqual(
            str(context.exception),
            'unsupported secret_type argument provided "invalid_type", '
            'supported types: "access_token,service_account_key"',
        )

    def test_rotate_roleset_account_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.gcp.rotate_roleset_account(name="test-roleset")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/roleset/test-roleset/rotate",
        )

    def test_rotate_roleset_account_key_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.gcp.rotate_roleset_account_key(name="test-roleset")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/roleset/test-roleset/rotate-key",
        )

    def test_read_roleset_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-roleset"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.gcp.read_roleset(name="test-roleset")
        self.assertEqual(result.json(), {"data": {"name": "test-roleset"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/roleset/test-roleset",
        )

    def test_list_rolesets_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["roleset1", "roleset2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.gcp.list_rolesets()
        self.assertEqual(result.json(), {"data": {"keys": ["roleset1", "roleset2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/gcp/rolesets",
        )

    def test_delete_roleset_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.gcp.delete_roleset(name="test-roleset")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/gcp/roleset/test-roleset",
        )

    def test_generate_oauth2_access_token_returns_response(self):
        mock_response = Response(200, json={"data": {"token": "test-token"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.gcp.generate_oauth2_access_token(roleset="test-roleset")
        self.assertEqual(result.json(), {"data": {"token": "test-token"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/token/test-roleset",
        )

    def test_generate_service_account_key_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "test-key"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.gcp.generate_service_account_key(roleset="test-roleset")
        self.assertEqual(result.json(), {"data": {"key": "test-key"}})

        expected_params = {
            "key_algorithm": "KEY_ALG_RSA_2048",
            "key_type": "TYPE_GOOGLE_CREDENTIALS_FILE",
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/key/test-roleset",
            json=expected_params,
        )

    def test_generate_service_account_key_with_invalid_method_raises_error(self):
        with self.assertRaises(VaultxError) as context:
            self.gcp.generate_service_account_key(roleset="test-roleset", method="PUT")

        self.assertEqual(
            str(context.exception),
            '"method" parameter provided invalid value; POST or GET allowed, "PUT" provided',
        )

    def test_create_or_update_static_account_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-static-account",
            "service_account_email": "test@example.com",
            "bindings": '{"role": "roles/viewer"}',
            "secret_type": "access_token",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
        }
        result = self.gcp.create_or_update_static_account(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "service_account_email": "test@example.com",
            "bindings": '{"role": "roles/viewer"}',
            "secret_type": "access_token",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account",
            json=expected_params,
        )

    def test_rotate_static_account_key_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.gcp.rotate_static_account_key(name="test-static-account")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account/rotate-key",
        )

    def test_read_static_account_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-static-account"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.gcp.read_static_account(name="test-static-account")
        self.assertEqual(result.json(), {"data": {"name": "test-static-account"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account",
        )

    def test_list_static_accounts_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["static-account1", "static-account2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.gcp.list_static_accounts()
        self.assertEqual(result.json(), {"data": {"keys": ["static-account1", "static-account2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/gcp/static-accounts",
        )

    def test_delete_static_account_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.gcp.delete_static_account(name="test-static-account")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account",
        )

    def test_generate_static_account_oauth2_access_token_returns_response(self):
        mock_response = Response(200, json={"data": {"token": "test-token"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.gcp.generate_static_account_oauth2_access_token(name="test-static-account")
        self.assertEqual(result.json(), {"data": {"token": "test-token"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account/token",
        )

    def test_generate_static_account_service_account_key_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "test-key"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.gcp.generate_static_account_service_account_key(name="test-static-account")
        self.assertEqual(result.json(), {"data": {"key": "test-key"}})

        expected_params = {
            "key_algorithm": "KEY_ALG_RSA_2048",
            "key_type": "TYPE_GOOGLE_CREDENTIALS_FILE",
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account/key",
            json=expected_params,
        )

    def test_create_or_update_impersonated_account_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-impersonated-account",
            "service_account_email": "test@example.com",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
            "ttl": "1h",
        }
        result = self.gcp.create_or_update_impersonated_account(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "service_account_email": "test@example.com",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
            "ttl": "1h",
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/impersonated-account/test-impersonated-account",
            json=expected_params,
        )

    def test_read_impersonated_account_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-impersonated-account"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.gcp.read_impersonated_account(name="test-impersonated-account")
        self.assertEqual(result.json(), {"data": {"name": "test-impersonated-account"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/impersonated-account/test-impersonated-account",
        )

    def test_list_impersonated_accounts_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["impersonated-account1", "impersonated-account2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.gcp.list_impersonated_accounts()
        self.assertEqual(result.json(), {"data": {"keys": ["impersonated-account1", "impersonated-account2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/gcp/impersonated-accounts",
        )

    def test_delete_impersonated_account_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.gcp.delete_impersonated_account(name="test-impersonated-account")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/gcp/impersonated-account/test-impersonated-account",
        )

    def test_generate_impersonated_account_oauth2_access_token_returns_response(self):
        mock_response = Response(200, json={"data": {"token": "test-token"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.gcp.generate_impersonated_account_oauth2_access_token(name="test-impersonated-account")
        self.assertEqual(result.json(), {"data": {"token": "test-token"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/impersonated-account/test-impersonated-account/token",
        )


class TestAsyncGcp(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.gcp = AsyncGcp(self.mock_adapter)

    async def test_configure_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "credentials": "test-credentials",
            "ttl": "1h",
            "max_ttl": "24h",
        }
        result = await self.gcp.configure(**params)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/config",
            json=params,
        )

    async def test_rotate_root_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"new_key": "test-key"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.gcp.rotate_root_credentials()
        self.assertEqual(result.json(), {"data": {"new_key": "test-key"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/config/rotate-root",
        )

    async def test_read_config_returns_response(self):
        mock_response = Response(200, json={"data": {"ttl": "1h"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.gcp.read_config()
        self.assertEqual(result.json(), {"data": {"ttl": "1h"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/config",
        )

    async def test_create_or_update_roleset_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-roleset",
            "project": "test-project",
            "bindings": '{"role": "roles/viewer"}',
            "secret_type": "access_token",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
        }
        result = await self.gcp.create_or_update_roleset(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "project": "test-project",
            "bindings": '{"role": "roles/viewer"}',
            "secret_type": "access_token",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/roleset/test-roleset",
            json=expected_params,
        )

    async def test_create_or_update_roleset_with_invalid_secret_type_raises_error(self):
        with self.assertRaises(VaultxError) as context:
            await self.gcp.create_or_update_roleset(
                name="test-roleset",
                project="test-project",
                bindings='{"role": "roles/viewer"}',
                secret_type="invalid_type",
            )

        self.assertEqual(
            str(context.exception),
            'unsupported secret_type argument provided "invalid_type", '
            'supported types: "access_token,service_account_key"',
        )

    async def test_rotate_roleset_account_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.gcp.rotate_roleset_account(name="test-roleset")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/roleset/test-roleset/rotate",
        )

    async def test_rotate_roleset_account_key_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.gcp.rotate_roleset_account_key(name="test-roleset")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/roleset/test-roleset/rotate-key",
        )

    async def test_read_roleset_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-roleset"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.gcp.read_roleset(name="test-roleset")
        self.assertEqual(result.json(), {"data": {"name": "test-roleset"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/roleset/test-roleset",
        )

    async def test_list_rolesets_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["roleset1", "roleset2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.gcp.list_rolesets()
        self.assertEqual(result.json(), {"data": {"keys": ["roleset1", "roleset2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/gcp/rolesets",
        )

    async def test_delete_roleset_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.gcp.delete_roleset(name="test-roleset")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/gcp/roleset/test-roleset",
        )

    async def test_generate_oauth2_access_token_returns_response(self):
        mock_response = Response(200, json={"data": {"token": "test-token"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.gcp.generate_oauth2_access_token(roleset="test-roleset")
        self.assertEqual(result.json(), {"data": {"token": "test-token"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/token/test-roleset",
        )

    async def test_generate_service_account_key_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "test-key"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.gcp.generate_service_account_key(roleset="test-roleset")
        self.assertEqual(result.json(), {"data": {"key": "test-key"}})

        expected_params = {
            "key_algorithm": "KEY_ALG_RSA_2048",
            "key_type": "TYPE_GOOGLE_CREDENTIALS_FILE",
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/key/test-roleset",
            json=expected_params,
        )

    async def test_generate_service_account_key_with_invalid_method_raises_error(self):
        with self.assertRaises(VaultxError) as context:
            await self.gcp.generate_service_account_key(roleset="test-roleset", method="PUT")

        self.assertEqual(
            str(context.exception),
            '"method" parameter provided invalid value; POST or GET allowed, "PUT" provided',
        )

    async def test_create_or_update_static_account_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-static-account",
            "service_account_email": "test@example.com",
            "bindings": '{"role": "roles/viewer"}',
            "secret_type": "access_token",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
        }
        result = await self.gcp.create_or_update_static_account(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "service_account_email": "test@example.com",
            "bindings": '{"role": "roles/viewer"}',
            "secret_type": "access_token",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account",
            json=expected_params,
        )

    async def test_rotate_static_account_key_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.gcp.rotate_static_account_key(name="test-static-account")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account/rotate-key",
        )

    async def test_read_static_account_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-static-account"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.gcp.read_static_account(name="test-static-account")
        self.assertEqual(result.json(), {"data": {"name": "test-static-account"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account",
        )

    async def test_list_static_accounts_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["static-account1", "static-account2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.gcp.list_static_accounts()
        self.assertEqual(result.json(), {"data": {"keys": ["static-account1", "static-account2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/gcp/static-accounts",
        )

    async def test_delete_static_account_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.gcp.delete_static_account(name="test-static-account")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account",
        )

    async def test_generate_static_account_oauth2_access_token_returns_response(self):
        mock_response = Response(200, json={"data": {"token": "test-token"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.gcp.generate_static_account_oauth2_access_token(name="test-static-account")
        self.assertEqual(result.json(), {"data": {"token": "test-token"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account/token",
        )

    async def test_generate_static_account_service_account_key_returns_response(self):
        mock_response = Response(200, json={"data": {"key": "test-key"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.gcp.generate_static_account_service_account_key(name="test-static-account")
        self.assertEqual(result.json(), {"data": {"key": "test-key"}})

        expected_params = {
            "key_algorithm": "KEY_ALG_RSA_2048",
            "key_type": "TYPE_GOOGLE_CREDENTIALS_FILE",
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/static-account/test-static-account/key",
            json=expected_params,
        )

    async def test_create_or_update_impersonated_account_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-impersonated-account",
            "service_account_email": "test@example.com",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
            "ttl": "1h",
        }
        result = await self.gcp.create_or_update_impersonated_account(**params)
        self.assertEqual(result.status_code, 204)

        expected_params = {
            "service_account_email": "test@example.com",
            "token_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
            "ttl": "1h",
        }
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/gcp/impersonated-account/test-impersonated-account",
            json=expected_params,
        )

    async def test_read_impersonated_account_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-impersonated-account"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.gcp.read_impersonated_account(name="test-impersonated-account")
        self.assertEqual(result.json(), {"data": {"name": "test-impersonated-account"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/impersonated-account/test-impersonated-account",
        )

    async def test_list_impersonated_accounts_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["impersonated-account1", "impersonated-account2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.gcp.list_impersonated_accounts()
        self.assertEqual(result.json(), {"data": {"keys": ["impersonated-account1", "impersonated-account2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/gcp/impersonated-accounts",
        )

    async def test_delete_impersonated_account_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.gcp.delete_impersonated_account(name="test-impersonated-account")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/gcp/impersonated-account/test-impersonated-account",
        )

    async def test_generate_impersonated_account_oauth2_access_token_returns_response(self):
        mock_response = Response(200, json={"data": {"token": "test-token"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.gcp.generate_impersonated_account_oauth2_access_token(name="test-impersonated-account")
        self.assertEqual(result.json(), {"data": {"token": "test-token"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/gcp/impersonated-account/test-impersonated-account/token",
        )
