import unittest
from unittest import mock

from httpx import Response

from vaultx import exceptions
from vaultx.adapters import VaultxResponse
from vaultx.api.async_auth_methods.kubernetes import Kubernetes as AsyncKubernetes
from vaultx.api.auth_methods.kubernetes import Kubernetes


class TestKubernetes(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.kubernetes = Kubernetes(self.mock_adapter)

    def test_configure_with_valid_certificate(self):
        valid_cert = "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----"
        self.mock_adapter.post.return_value = Response(204)
        result = self.kubernetes.configure(
            kubernetes_host="https://k8s.example.com",
            kubernetes_ca_cert=valid_cert,
            token_reviewer_jwt="test_jwt",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_configure_with_invalid_certificate(self):
        invalid_cert = "invalid_certificate_format"
        with self.assertRaises(exceptions.VaultxError):
            self.kubernetes.configure(
                kubernetes_host="https://k8s.example.com",
                kubernetes_ca_cert=invalid_cert,
                token_reviewer_jwt="test_jwt",
            )

    def test_read_config(self):
        mock_response = Response(200, json={"data": {"kubernetes_host": "https://k8s.example.com"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.kubernetes.read_config()
        self.assertEqual(result, {"kubernetes_host": "https://k8s.example.com"})
        self.mock_adapter.get.assert_called_once()

    def test_create_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.kubernetes.create_role(
            name="test_role",
            bound_service_account_names=["sa1", "sa2"],
            bound_service_account_namespaces=["ns1", "ns2"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.kubernetes.read_role(name="test_role")
        self.assertEqual(result, {"name": "test_role"})
        self.mock_adapter.get.assert_called_once()

    def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.kubernetes.list_roles()
        self.assertEqual(result, {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.kubernetes.delete_role(name="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = self.kubernetes.login(role="test_role", jwt="test_jwt")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()


class TestAsyncKubernetes(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.kubernetes = AsyncKubernetes(self.mock_adapter)

    async def test_configure_with_valid_certificate(self):
        valid_cert = "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----"
        self.mock_adapter.post.return_value = Response(204)
        result = await self.kubernetes.configure(
            kubernetes_host="https://k8s.example.com",
            kubernetes_ca_cert=valid_cert,
            token_reviewer_jwt="test_jwt",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_configure_with_invalid_certificate(self):
        invalid_cert = "invalid_certificate_format"
        with self.assertRaises(exceptions.VaultxError):
            await self.kubernetes.configure(
                kubernetes_host="https://k8s.example.com",
                kubernetes_ca_cert=invalid_cert,
                token_reviewer_jwt="test_jwt",
            )

    async def test_read_config(self):
        mock_response = Response(200, json={"data": {"kubernetes_host": "https://k8s.example.com"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.kubernetes.read_config()
        self.assertEqual(result, {"kubernetes_host": "https://k8s.example.com"})
        self.mock_adapter.get.assert_called_once()

    async def test_create_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.kubernetes.create_role(
            name="test_role",
            bound_service_account_names=["sa1", "sa2"],
            bound_service_account_namespaces=["ns1", "ns2"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.kubernetes.read_role(name="test_role")
        self.assertEqual(result, {"name": "test_role"})
        self.mock_adapter.get.assert_called_once()

    async def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.kubernetes.list_roles()
        self.assertEqual(result, {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    async def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.kubernetes.delete_role(name="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_login(self):
        mock_response = Response(200, json={"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.return_value = VaultxResponse(mock_response)
        result = await self.kubernetes.login(role="test_role", jwt="test_jwt")
        self.assertEqual(result.value, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()
