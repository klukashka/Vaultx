import unittest
from unittest import mock

from httpx import Response

from vaultx import exceptions
from vaultx.adapters import VaultxResponse
from vaultx.api.async_auth_methods.aws import Aws as AsyncAws
from vaultx.api.async_auth_methods.aws import SigV4Auth as AsyncSigV4Auth
from vaultx.api.async_auth_methods.aws import generate_sigv4_auth_request as async_generate_sigv4_auth_request
from vaultx.api.auth_methods.aws import Aws, SigV4Auth, generate_sigv4_auth_request


class TestSigV4Auth(unittest.TestCase):
    def setUp(self):
        self.access_key = "test_access_key"
        self.secret_key = "test_secret_key"
        self.session_token = "test_session_token"
        self.region = "us-east-1"
        self.sigv4_auth = SigV4Auth(self.access_key, self.secret_key, self.session_token, self.region)

    def test_add_auth(self):
        request = generate_sigv4_auth_request()
        self.sigv4_auth.add_auth(request)
        self.assertIn("Authorization", request.headers)
        self.assertIn("X-Amz-Date", request.headers)
        if self.session_token:
            self.assertIn("X-Amz-Security-Token", request.headers)


class TestAsyncSigV4Auth(unittest.TestCase):
    def setUp(self):
        self.access_key = "test_access_key"
        self.secret_key = "test_secret_key"
        self.session_token = "test_session_token"
        self.region = "us-east-1"
        self.sigv4_auth = AsyncSigV4Auth(self.access_key, self.secret_key, self.session_token, self.region)

    def test_add_auth(self):
        request = async_generate_sigv4_auth_request()
        self.sigv4_auth.add_auth(request)
        self.assertIn("Authorization", request.headers)
        self.assertIn("X-Amz-Date", request.headers)
        if self.session_token:
            self.assertIn("X-Amz-Security-Token", request.headers)


class TestAws(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.aws = Aws(self.mock_adapter)

    def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.configure(
            access_key="test_access_key",
            secret_key="test_secret_key",
            endpoint="https://example.com",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_config(self):
        mock_response = Response(200, json={"data": {"access_key": "test_access_key"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.aws.read_config()
        self.assertEqual(result, {"access_key": "test_access_key"})
        self.mock_adapter.get.assert_called_once()

    def test_delete_config(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.aws.delete_config()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_configure_identity_integration(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.configure_identity_integration(iam_alias="role_id", ec2_alias="instance_id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            self.aws.configure_identity_integration(iam_alias="invalid_type")

    def test_read_identity_integration(self):
        mock_response = Response(200, json={"data": {"iam_alias": "role_id"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.aws.read_identity_integration()
        self.assertEqual(result, {"iam_alias": "role_id"})
        self.mock_adapter.get.assert_called_once()

    def test_create_certificate_configuration(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.create_certificate_configuration(cert_name="test_cert", aws_public_cert="test_cert_data")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_certificate_configuration(self):
        mock_response = Response(200, json={"data": {"cert_name": "test_cert"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.aws.read_certificate_configuration(cert_name="test_cert")
        self.assertEqual(result, {"cert_name": "test_cert"})
        self.mock_adapter.get.assert_called_once()

    def test_delete_certificate_configuration(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.aws.delete_certificate_configuration(cert_name="test_cert")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_list_certificate_configurations(self):
        mock_response = Response(200, json={"data": {"keys": ["cert1", "cert2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.aws.list_certificate_configurations()
        self.assertEqual(result, {"keys": ["cert1", "cert2"]})
        self.mock_adapter.list.assert_called_once()

    def test_create_sts_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.create_sts_role(
            account_id="123456789012", sts_role="arn:aws:iam::123456789012:role/test-role"
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_sts_role(self):
        mock_response = Response(200, json={"data": {"account_id": "123456789012"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.aws.read_sts_role(account_id="123456789012")
        self.assertEqual(result, {"account_id": "123456789012"})
        self.mock_adapter.get.assert_called_once()

    def test_list_sts_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["123456789012"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.aws.list_sts_roles()
        self.assertEqual(result, {"keys": ["123456789012"]})
        self.mock_adapter.list.assert_called_once()

    def test_delete_sts_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.aws.delete_sts_role(account_id="123456789012")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_configure_identity_whitelist_tidy(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.configure_identity_whitelist_tidy(safety_buffer="72h")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_identity_whitelist_tidy(self):
        mock_response = Response(200, json={"data": {"safety_buffer": "72h"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.aws.read_identity_whitelist_tidy()
        self.assertEqual(result, {"safety_buffer": "72h"})
        self.mock_adapter.get.assert_called_once()

    def test_delete_identity_whitelist_tidy(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.aws.delete_identity_whitelist_tidy()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_configure_role_tag_blacklist_tidy(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.configure_role_tag_blacklist_tidy(safety_buffer="72h")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_role_tag_blacklist_tidy(self):
        mock_response = Response(200, json={"data": {"safety_buffer": "72h"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.aws.read_role_tag_blacklist_tidy()
        self.assertEqual(result, {"safety_buffer": "72h"})
        self.mock_adapter.get.assert_called_once()

    def test_delete_role_tag_blacklist_tidy(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.aws.delete_role_tag_blacklist_tidy()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_create_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.create_role(role="test_role", auth_type="iam")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_role(self):
        mock_response = Response(200, json={"data": {"role": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.aws.read_role(role="test_role")
        self.assertEqual(result, {"role": "test_role"})
        self.mock_adapter.get.assert_called_once()

    def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.aws.list_roles()
        self.assertEqual(result, {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.aws.delete_role(role="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_create_role_tags(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.create_role_tags(role="test_role", policies=["policy1"])
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_iam_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = self.aws.iam_login(access_key="test_access_key", secret_key="test_secret_key")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()

    def test_ec2_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = self.aws.ec2_login(pkcs7="test_pkcs7")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()

    def test_place_role_tags_in_blacklist(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.place_role_tags_in_blacklist(role_tag="test_role_tag")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_role_tag_blacklist(self):
        mock_response = Response(200, json={"data": {"role_tag": "test_role_tag"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.aws.read_role_tag_blacklist(role_tag="test_role_tag")
        self.assertEqual(result, {"role_tag": "test_role_tag"})
        self.mock_adapter.get.assert_called_once()

    def test_list_blacklist_tags(self):
        mock_response = Response(200, json={"data": {"keys": ["tag1", "tag2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.aws.list_blacklist_tags()
        self.assertEqual(result, {"keys": ["tag1", "tag2"]})
        self.mock_adapter.list.assert_called_once()

    def test_delete_blacklist_tags(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.aws.delete_blacklist_tags(role_tag="test_role_tag")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_tidy_blacklist_tags(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.tidy_blacklist_tags(safety_buffer="72h")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_identity_whitelist(self):
        mock_response = Response(200, json={"data": {"instance_id": "test_instance_id"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.aws.read_identity_whitelist(instance_id="test_instance_id")
        self.assertEqual(result, {"instance_id": "test_instance_id"})
        self.mock_adapter.get.assert_called_once()

    def test_list_identity_whitelist(self):
        mock_response = Response(200, json={"data": {"keys": ["instance1", "instance2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.aws.list_identity_whitelist()
        self.assertEqual(result, {"keys": ["instance1", "instance2"]})
        self.mock_adapter.list.assert_called_once()

    def test_delete_identity_whitelist_entries(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.aws.delete_identity_whitelist_entries(instance_id="test_instance_id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_tidy_identity_whitelist_entries(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.aws.tidy_identity_whitelist_entries(safety_buffer="72h")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()


class TestAsyncAws(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.aws = AsyncAws(self.mock_adapter)

    async def test_configure(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.configure(
            access_key="test_access_key",
            secret_key="test_secret_key",
            endpoint="https://example.com",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_config(self):
        mock_response = Response(200, json={"data": {"access_key": "test_access_key"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.aws.read_config()
        self.assertEqual(result, {"access_key": "test_access_key"})
        self.mock_adapter.get.assert_called_once()

    async def test_delete_config(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.aws.delete_config()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_configure_identity_integration(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.configure_identity_integration(iam_alias="role_id", ec2_alias="instance_id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

        with self.assertRaises(exceptions.VaultxError):
            await self.aws.configure_identity_integration(iam_alias="invalid_type")

    async def test_read_identity_integration(self):
        mock_response = Response(200, json={"data": {"iam_alias": "role_id"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.aws.read_identity_integration()
        self.assertEqual(result, {"iam_alias": "role_id"})
        self.mock_adapter.get.assert_called_once()

    async def test_create_certificate_configuration(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.create_certificate_configuration(
            cert_name="test_cert", aws_public_cert="test_cert_data"
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_certificate_configuration(self):
        mock_response = Response(200, json={"data": {"cert_name": "test_cert"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.aws.read_certificate_configuration(cert_name="test_cert")
        self.assertEqual(result, {"cert_name": "test_cert"})
        self.mock_adapter.get.assert_called_once()

    async def test_delete_certificate_configuration(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.aws.delete_certificate_configuration(cert_name="test_cert")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_list_certificate_configurations(self):
        mock_response = Response(200, json={"data": {"keys": ["cert1", "cert2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.aws.list_certificate_configurations()
        self.assertEqual(result, {"keys": ["cert1", "cert2"]})
        self.mock_adapter.list.assert_called_once()

    async def test_create_sts_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.create_sts_role(
            account_id="123456789012", sts_role="arn:aws:iam::123456789012:role/test-role"
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_sts_role(self):
        mock_response = Response(200, json={"data": {"account_id": "123456789012"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.aws.read_sts_role(account_id="123456789012")
        self.assertEqual(result, {"account_id": "123456789012"})
        self.mock_adapter.get.assert_called_once()

    async def test_list_sts_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["123456789012"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.aws.list_sts_roles()
        self.assertEqual(result, {"keys": ["123456789012"]})
        self.mock_adapter.list.assert_called_once()

    async def test_delete_sts_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.aws.delete_sts_role(account_id="123456789012")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_configure_identity_whitelist_tidy(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.configure_identity_whitelist_tidy(safety_buffer="72h")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_identity_whitelist_tidy(self):
        mock_response = Response(200, json={"data": {"safety_buffer": "72h"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.aws.read_identity_whitelist_tidy()
        self.assertEqual(result, {"safety_buffer": "72h"})
        self.mock_adapter.get.assert_called_once()

    async def test_delete_identity_whitelist_tidy(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.aws.delete_identity_whitelist_tidy()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_configure_role_tag_blacklist_tidy(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.configure_role_tag_blacklist_tidy(safety_buffer="72h")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_role_tag_blacklist_tidy(self):
        mock_response = Response(200, json={"data": {"safety_buffer": "72h"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.aws.read_role_tag_blacklist_tidy()
        self.assertEqual(result, {"safety_buffer": "72h"})
        self.mock_adapter.get.assert_called_once()

    async def test_delete_role_tag_blacklist_tidy(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.aws.delete_role_tag_blacklist_tidy()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_create_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.create_role(role="test_role", auth_type="iam")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_role(self):
        mock_response = Response(200, json={"data": {"role": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.aws.read_role(role="test_role")
        self.assertEqual(result, {"role": "test_role"})
        self.mock_adapter.get.assert_called_once()

    async def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.aws.list_roles()
        self.assertEqual(result, {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    async def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.aws.delete_role(role="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_create_role_tags(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.create_role_tags(role="test_role", policies=["policy1"])
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_iam_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = await self.aws.iam_login(access_key="test_access_key", secret_key="test_secret_key")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()

    async def test_ec2_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = await self.aws.ec2_login(pkcs7="test_pkcs7")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()

    async def test_place_role_tags_in_blacklist(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.place_role_tags_in_blacklist(role_tag="test_role_tag")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_role_tag_blacklist(self):
        mock_response = Response(200, json={"data": {"role_tag": "test_role_tag"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.aws.read_role_tag_blacklist(role_tag="test_role_tag")
        self.assertEqual(result, {"role_tag": "test_role_tag"})
        self.mock_adapter.get.assert_called_once()

    async def test_list_blacklist_tags(self):
        mock_response = Response(200, json={"data": {"keys": ["tag1", "tag2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.aws.list_blacklist_tags()
        self.assertEqual(result, {"keys": ["tag1", "tag2"]})
        self.mock_adapter.list.assert_called_once()

    async def test_delete_blacklist_tags(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.aws.delete_blacklist_tags(role_tag="test_role_tag")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_tidy_blacklist_tags(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.tidy_blacklist_tags(safety_buffer="72h")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_identity_whitelist(self):
        mock_response = Response(200, json={"data": {"instance_id": "test_instance_id"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.aws.read_identity_whitelist(instance_id="test_instance_id")
        self.assertEqual(result, {"instance_id": "test_instance_id"})
        self.mock_adapter.get.assert_called_once()

    async def test_list_identity_whitelist(self):
        mock_response = Response(200, json={"data": {"keys": ["instance1", "instance2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.aws.list_identity_whitelist()
        self.assertEqual(result, {"keys": ["instance1", "instance2"]})
        self.mock_adapter.list.assert_called_once()

    async def test_delete_identity_whitelist_entries(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.aws.delete_identity_whitelist_entries(instance_id="test_instance_id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_tidy_identity_whitelist_entries(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.aws.tidy_identity_whitelist_entries(safety_buffer="72h")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()
