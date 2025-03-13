import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.aws import Aws as AsyncAws
from vaultx.api.secrets_engines.aws import Aws
from vaultx.exceptions import VaultxError


class TestAws(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.aws = Aws(self.mock_adapter)

    def test_configure_root_iam_credentials_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "access_key": "test-access-key",
            "secret_key": "test-secret-key",
            "region": "us-east-1",
            "iam_endpoint": "https://iam.example.com",
            "sts_endpoint": "https://sts.example.com",
            "max_retries": 3,
        }
        result = self.aws.configure_root_iam_credentials(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/aws/config/root",
            json=params,
        )

    def test_rotate_root_iam_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"access_key": "new-access-key"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.aws.rotate_root_iam_credentials()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"access_key": "new-access-key"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/aws/config/rotate-root",
        )

    def test_configure_lease_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "lease": "1h",
            "lease_max": "24h",
        }
        result = self.aws.configure_lease(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/aws/config/lease",
            json=params,
        )

    def test_read_lease_config_returns_response(self):
        mock_response = Response(200, json={"data": {"lease": "1h", "lease_max": "24h"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.aws.read_lease_config()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"lease": "1h", "lease_max": "24h"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/aws/config/lease",
        )

    def test_create_or_update_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "credential_type": "iam_user",
            "policy_document": {
                "Version": "2012-10-17",
                "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}],
            },
            "default_sts_ttl": "1h",
            "max_sts_ttl": "24h",
            "role_arns": "arn:aws:iam::123456789012:role/test-role",
            "policy_arns": ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"],
            "iam_tags": ["key=value"],
        }
        result = self.aws.create_or_update_role(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)

    def test_create_or_update_role_with_invalid_credential_type_raises_error(self):
        with self.assertRaises(VaultxError) as context:
            self.aws.create_or_update_role(name="test-role", credential_type="invalid_type")

        self.assertEqual(
            str(context.exception),
            'invalid credential_type argument provided "invalid_type", '
            'supported types: "iam_user, assumed_role, federation_token"',
        )

    def test_read_role_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.aws.read_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/aws/roles/test-role",
        )

    def test_list_roles_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.aws.list_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/aws/roles",
        )

    def test_delete_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.aws.delete_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/aws/roles/test-role",
        )

    def test_generate_credentials_creds_endpoint_returns_response(self):
        mock_response = Response(200, json={"data": {"access_key": "test-access-key", "secret_key": "test-secret-key"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.aws.generate_credentials(name="test-role", endpoint="creds")
        if isinstance(result, Response):
            self.assertEqual(
                result.json(), {"data": {"access_key": "test-access-key", "secret_key": "test-secret-key"}}
            )
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/aws/creds/test-role",
            params={},
        )

    def test_generate_credentials_sts_endpoint_returns_response(self):
        mock_response = Response(200, json={"data": {"access_key": "test-access-key", "secret_key": "test-secret-key"}})
        self.mock_adapter.post.return_value = mock_response

        params = {
            "role_arn": "arn:aws:iam::123456789012:role/test-role",
            "ttl": "1h",
            "role_session_name": "test-session",
        }
        result = self.aws.generate_credentials(name="test-role", endpoint="sts", **params)
        if isinstance(result, Response):
            self.assertEqual(
                result.json(), {"data": {"access_key": "test-access-key", "secret_key": "test-secret-key"}}
            )
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/aws/sts/test-role",
            json=params,
        )

    def test_generate_credentials_with_invalid_endpoint_raises_error(self):
        with self.assertRaises(VaultxError) as context:
            self.aws.generate_credentials(name="test-role", endpoint="invalid_endpoint")

        self.assertEqual(
            str(context.exception),
            'invalid endpoint argument provided "invalid_endpoint", supported types: "creds, sts"',
        )


class TestAsyncAws(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.aws = AsyncAws(self.mock_adapter)

    async def test_configure_root_iam_credentials_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "access_key": "test-access-key",
            "secret_key": "test-secret-key",
            "region": "us-east-1",
            "iam_endpoint": "https://iam.example.com",
            "sts_endpoint": "https://sts.example.com",
            "max_retries": 3,
        }
        result = await self.aws.configure_root_iam_credentials(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/aws/config/root",
            json=params,
        )

    async def test_rotate_root_iam_credentials_returns_response(self):
        mock_response = Response(200, json={"data": {"access_key": "new-access-key"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.aws.rotate_root_iam_credentials()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"access_key": "new-access-key"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/aws/config/rotate-root",
        )

    async def test_configure_lease_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "lease": "1h",
            "lease_max": "24h",
        }
        result = await self.aws.configure_lease(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/aws/config/lease",
            json=params,
        )

    async def test_read_lease_config_returns_response(self):
        mock_response = Response(200, json={"data": {"lease": "1h", "lease_max": "24h"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.aws.read_lease_config()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"lease": "1h", "lease_max": "24h"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/aws/config/lease",
        )

    async def test_create_or_update_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        params = {
            "name": "test-role",
            "credential_type": "iam_user",
            "policy_document": '{"Version": "2012-10-17", "Statement": '
            '[{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}',
            "default_sts_ttl": "1h",
            "max_sts_ttl": "24h",
            "role_arns": "arn:aws:iam::123456789012:role/test-role",
            "policy_arns": ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"],
            "iam_tags": ["key=value"],
        }
        result = await self.aws.create_or_update_role(**params)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)

    async def test_read_role_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.aws.read_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/aws/roles/test-role",
        )

    async def test_list_roles_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.aws.list_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/aws/roles",
        )

    async def test_delete_role_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.aws.delete_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/aws/roles/test-role",
        )

    async def test_generate_credentials_creds_endpoint_returns_response(self):
        mock_response = Response(200, json={"data": {"access_key": "test-access-key", "secret_key": "test-secret-key"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.aws.generate_credentials(name="test-role", endpoint="creds")
        if isinstance(result, Response):
            self.assertEqual(
                result.json(), {"data": {"access_key": "test-access-key", "secret_key": "test-secret-key"}}
            )
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/aws/creds/test-role",
            params={},
        )

    async def test_generate_credentials_sts_endpoint_returns_response(self):
        mock_response = Response(200, json={"data": {"access_key": "test-access-key", "secret_key": "test-secret-key"}})
        self.mock_adapter.post.return_value = mock_response

        params = {
            "role_arn": "arn:aws:iam::123456789012:role/test-role",
            "ttl": "1h",
            "role_session_name": "test-session",
        }
        result = await self.aws.generate_credentials(name="test-role", endpoint="sts", **params)
        if isinstance(result, Response):
            self.assertEqual(
                result.json(), {"data": {"access_key": "test-access-key", "secret_key": "test-secret-key"}}
            )
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/aws/sts/test-role",
            json=params,
        )
