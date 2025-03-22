import unittest
from unittest import mock
from httpx import Response
from vaultx.api.auth_methods.cert import Cert
from vaultx.api.async_auth_methods.cert import Cert as AsyncCert
from vaultx.adapters import VaultxResponse


class TestCert(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.mock_adapter._kwargs = {"verify": True, "cert": None}
        self.cert = Cert(self.mock_adapter)

    def test_create_ca_certificate_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.cert.create_ca_certificate_role(
            name="test_role",
            certificate="-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_ca_certificate_role(self):
        mock_response = Response(200, json={"data": {"name": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.cert.read_ca_certificate_role(name="test_role")
        self.assertEqual(result.value["data"], {"name": "test_role"})
        self.mock_adapter.get.assert_called_once()

    def test_list_certificate_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = self.cert.list_certificate_roles()
        self.assertEqual(result.value["data"], {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    def test_delete_certificate_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.cert.delete_certificate_role(name="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_configure_tls_certificate(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.cert.configure_tls_certificate(disable_binding=True)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_login_with_valid_cert(self):
        self.mock_adapter.login.return_value = Response(200, json={"auth": {"client_token": "test_token"}})
        result = self.cert.login(
            cert_pem="-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----",
            key_pem="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----",
        )
        self.assertEqual(result.json(), {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()

    def test_login_with_invalid_cert(self):
        with self.assertRaises(FileNotFoundError):
            self.cert.login(cert_pem="invalid_cert")

    def test_login_with_missing_cert(self):
        with self.assertRaises(FileNotFoundError):
            self.cert.login(cert_pem="/path/to/nonexistent/cert.pem")


class TestAsyncCert(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.mock_adapter._kwargs = {"verify": True, "cert": None}
        self.cert = AsyncCert(self.mock_adapter)

    async def test_create_ca_certificate_role(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.cert.create_ca_certificate_role(
            name="test_role",
            certificate="-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_ca_certificate_role(self):
        mock_response = Response(200, json={"data": {"name": "test_role"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.cert.read_ca_certificate_role(name="test_role")
        self.assertEqual(result.value["data"], {"name": "test_role"})
        self.mock_adapter.get.assert_called_once()

    async def test_list_certificate_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = VaultxResponse(mock_response)
        result = await self.cert.list_certificate_roles()
        self.assertEqual(result.value["data"], {"keys": ["role1", "role2"]})
        self.mock_adapter.list.assert_called_once()

    async def test_delete_certificate_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.cert.delete_certificate_role(name="test_role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_configure_tls_certificate(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.cert.configure_tls_certificate(disable_binding=True)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_login_with_valid_cert(self):
        self.mock_adapter.login.return_value = Response(200, json={"auth": {"client_token": "test_token"}})
        result = await self.cert.login(
            cert_pem="-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----",
            key_pem="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----",
        )
        self.assertEqual(result.json(), {"auth": {"client_token": "test_token"}})
        self.mock_adapter.login.assert_called_once()

    async def test_login_with_invalid_cert(self):
        with self.assertRaises(FileNotFoundError):
            await self.cert.login(cert_pem="invalid_cert")

    async def test_login_with_missing_cert(self):
        with self.assertRaises(FileNotFoundError):
            await self.cert.login(cert_pem="/path/to/nonexistent/cert.pem")
