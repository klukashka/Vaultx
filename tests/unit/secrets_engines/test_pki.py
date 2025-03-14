import unittest
from unittest import mock

from httpx import Response

from vaultx.api.secrets_engines.pki import Pki
from vaultx.api.async_secrets_engines.pki import Pki as AsyncPki


class TestPki(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.pki = Pki(self.mock_adapter)

    def test_read_ca_certificate(self):
        mock_response = Response(200, text="-----BEGIN CERTIFICATE-----")
        self.mock_adapter.get.return_value = mock_response

        result = self.pki.read_ca_certificate()
        self.assertEqual(result, "-----BEGIN CERTIFICATE-----")
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/ca/pem",
        )

    def test_read_ca_certificate_chain(self):
        mock_response = Response(200, text="-----BEGIN CERTIFICATE-----")
        self.mock_adapter.get.return_value = mock_response

        result = self.pki.read_ca_certificate_chain()
        self.assertEqual(result, "-----BEGIN CERTIFICATE-----")
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/ca_chain",
        )

    def test_read_certificate(self):
        mock_response = Response(200, json={"data": {"serial": "12345"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.pki.read_certificate(serial="12345")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"serial": "12345"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/cert/12345",
        )

    def test_list_certificates(self):
        mock_response = Response(200, json={"data": {"keys": ["cert1", "cert2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.pki.list_certificates()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["cert1", "cert2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/pki/certs",
        )

    def test_submit_ca_information(self):
        mock_response = Response(200, json={"data": {"message": "CA information submitted"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.submit_ca_information(pem_bundle="-----BEGIN CERTIFICATE-----")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "CA information submitted"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/config/ca",
            json={"pem_bundle": "-----BEGIN CERTIFICATE-----"},
        )

    def test_read_crl_configuration(self):
        mock_response = Response(200, json={"data": {"expiry": "24h"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.pki.read_crl_configuration()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"expiry": "24h"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/config/crl",
        )

    def test_set_crl_configuration(self):
        mock_response = Response(200, json={"data": {"message": "CRL configuration updated"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.set_crl_configuration(expiry="24h", disable=False)
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "CRL configuration updated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/config/crl",
            json={"expiry": "24h", "disable": False},
        )

    def test_read_urls(self):
        mock_response = Response(200, json={"data": {"issuing_certificates": ["http://example.com"]}})
        self.mock_adapter.get.return_value = mock_response

        result = self.pki.read_urls()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"issuing_certificates": ["http://example.com"]}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/config/urls",
        )

    def test_set_urls(self):
        mock_response = Response(200, json={"data": {"message": "URLs updated"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.set_urls(params={"issuing_certificates": ["http://example.com"]})
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "URLs updated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/config/urls",
            json={"issuing_certificates": ["http://example.com"]},
        )

    def test_read_crl(self):
        mock_response = Response(200, text="-----BEGIN X509 CRL-----")
        self.mock_adapter.get.return_value = mock_response

        result = self.pki.read_crl()
        self.assertEqual(result, "-----BEGIN X509 CRL-----")
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/crl/pem",
        )

    def test_rotate_crl(self):
        mock_response = Response(200, json={"data": {"message": "CRL rotated"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.pki.rotate_crl()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "CRL rotated"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/crl/rotate",
        )

    def test_generate_intermediate(self):
        mock_response = Response(200, json={"data": {"csr": "-----BEGIN CERTIFICATE REQUEST-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.generate_intermediate(_type="exported", common_name="example.com")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"csr": "-----BEGIN CERTIFICATE REQUEST-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/intermediate/generate/exported",
            json={"common_name": "example.com"},
            wrap_ttl=None,
        )

    def test_set_signed_intermediate(self):
        mock_response = Response(200, json={"data": {"message": "Intermediate certificate set"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.set_signed_intermediate(certificate="-----BEGIN CERTIFICATE-----")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Intermediate certificate set"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/intermediate/set-signed",
            json={"certificate": "-----BEGIN CERTIFICATE-----"},
        )

    def test_generate_certificate(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.generate_certificate(name="test-role", common_name="example.com")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/issue/test-role",
            json={"common_name": "example.com"},
            wrap_ttl=None,
        )

    def test_revoke_certificate(self):
        mock_response = Response(200, json={"data": {"message": "Certificate revoked"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.revoke_certificate(serial_number="12345")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Certificate revoked"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/revoke",
            json={"serial_number": "12345"},
        )

    def test_create_or_update_role(self):
        mock_response = Response(200, json={"data": {"message": "Role created/updated"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.create_or_update_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Role created/updated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/roles/test-role",
            json={"name": "test-role"},
        )

    def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.pki.read_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/roles/test-role",
        )

    def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.pki.list_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/pki/roles",
        )

    def test_delete_role(self):
        mock_response = Response(200, json={"data": {"message": "Role deleted"}})
        self.mock_adapter.delete.return_value = mock_response

        result = self.pki.delete_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Role deleted"}})
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/pki/roles/test-role",
        )

    def test_generate_root(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.generate_root(_type="exported", common_name="example.com")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/root/generate/exported",
            json={"common_name": "example.com"},
            wrap_ttl=None,
        )

    def test_delete_root(self):
        mock_response = Response(200, json={"data": {"message": "Root deleted"}})
        self.mock_adapter.delete.return_value = mock_response

        result = self.pki.delete_root()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Root deleted"}})
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/pki/root",
        )

    def test_sign_intermediate(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.sign_intermediate(csr="-----BEGIN CERTIFICATE REQUEST-----", common_name="example.com")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/root/sign-intermediate",
            json={"csr": "-----BEGIN CERTIFICATE REQUEST-----", "common_name": "example.com"},
        )

    def test_sign_self_issued(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.sign_self_issued(certificate="-----BEGIN CERTIFICATE-----")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/root/sign-self-issued",
            json={"certificate": "-----BEGIN CERTIFICATE-----"},
        )

    def test_sign_certificate(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.sign_certificate(name="test-role", csr="-----BEGIN CERTIFICATE REQUEST-----", common_name="example.com")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/sign/test-role",
            json={"csr": "-----BEGIN CERTIFICATE REQUEST-----", "common_name": "example.com"},
        )

    def test_sign_verbatim(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.sign_verbatim(csr="-----BEGIN CERTIFICATE REQUEST-----")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/sign-verbatim",
            json={"csr": "-----BEGIN CERTIFICATE REQUEST-----"},
        )

    def test_tidy(self):
        mock_response = Response(200, json={"data": {"message": "Tidy operation started"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.tidy()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Tidy operation started"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/tidy",
            json={},
        )

    def test_read_issuer(self):
        mock_response = Response(200, json={"data": {"issuer_ref": "12345"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.pki.read_issuer(issuer_ref="12345")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"issuer_ref": "12345"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/issuer/12345",
        )

    def test_list_issuers(self):
        mock_response = Response(200, json={"data": {"keys": ["issuer1", "issuer2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.pki.list_issuers()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["issuer1", "issuer2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/pki/issuers",
        )

    def test_update_issuer(self):
        mock_response = Response(200, json={"data": {"message": "Issuer updated"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.update_issuer(issuer_ref="12345", extra_params={"key": "value"})
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Issuer updated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/issuer/12345",
            json={"key": "value"},
        )

    def test_revoke_issuer(self):
        mock_response = Response(200, json={"data": {"message": "Issuer revoked"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.pki.revoke_issuer(issuer_ref="12345")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Issuer revoked"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/issuer/12345/revoke",
        )

    def test_delete_issuer(self):
        mock_response = Response(200, json={"data": {"message": "Issuer deleted"}})
        self.mock_adapter.delete.return_value = mock_response

        result = self.pki.delete_issuer(issuer_ref="12345")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Issuer deleted"}})
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/pki/issuer/12345",
        )


class TestAsyncPki(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.pki = AsyncPki(self.mock_adapter)

    async def test_read_ca_certificate_async(self):
        mock_response = Response(200, text="-----BEGIN CERTIFICATE-----")
        self.mock_adapter.get.return_value = mock_response

        result = await self.pki.read_ca_certificate()
        self.assertEqual(result, "-----BEGIN CERTIFICATE-----")
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/ca/pem",
        )

    async def test_read_ca_certificate_chain_async(self):
        mock_response = Response(200, text="-----BEGIN CERTIFICATE-----")
        self.mock_adapter.get.return_value = mock_response

        result = await self.pki.read_ca_certificate_chain()
        self.assertEqual(result, "-----BEGIN CERTIFICATE-----")
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/ca_chain",
        )

    async def test_read_certificate_async(self):
        mock_response = Response(200, json={"data": {"serial": "12345"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.pki.read_certificate(serial="12345")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"serial": "12345"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/cert/12345",
        )

    async def test_list_certificates_async(self):
        mock_response = Response(200, json={"data": {"keys": ["cert1", "cert2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.pki.list_certificates()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["cert1", "cert2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/pki/certs",
        )

    async def test_submit_ca_information_async(self):
        mock_response = Response(200, json={"data": {"message": "CA information submitted"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.submit_ca_information(pem_bundle="-----BEGIN CERTIFICATE-----")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "CA information submitted"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/config/ca",
            json={"pem_bundle": "-----BEGIN CERTIFICATE-----"},
        )

    async def test_read_crl_configuration_async(self):
        mock_response = Response(200, json={"data": {"expiry": "24h"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.pki.read_crl_configuration()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"expiry": "24h"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/config/crl",
        )

    async def test_set_crl_configuration_async(self):
        mock_response = Response(200, json={"data": {"message": "CRL configuration updated"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.set_crl_configuration(expiry="24h", disable=False)
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "CRL configuration updated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/config/crl",
            json={"expiry": "24h", "disable": False},
        )

    async def test_read_urls_async(self):
        mock_response = Response(200, json={"data": {"issuing_certificates": ["http://example.com"]}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.pki.read_urls()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"issuing_certificates": ["http://example.com"]}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/config/urls",
        )

    async def test_set_urls_async(self):
        mock_response = Response(200, json={"data": {"message": "URLs updated"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.set_urls(params={"issuing_certificates": ["http://example.com"]})
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "URLs updated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/config/urls",
            json={"issuing_certificates": ["http://example.com"]},
        )

    async def test_read_crl_async(self):
        mock_response = Response(200, text="-----BEGIN X509 CRL-----")
        self.mock_adapter.get.return_value = mock_response

        result = await self.pki.read_crl()
        self.assertEqual(result, "-----BEGIN X509 CRL-----")
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/crl/pem",
        )

    async def test_rotate_crl_async(self):
        mock_response = Response(200, json={"data": {"message": "CRL rotated"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.pki.rotate_crl()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "CRL rotated"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/crl/rotate",
        )

    async def test_generate_intermediate_async(self):
        mock_response = Response(200, json={"data": {"csr": "-----BEGIN CERTIFICATE REQUEST-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.generate_intermediate(_type="exported", common_name="example.com")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"csr": "-----BEGIN CERTIFICATE REQUEST-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/intermediate/generate/exported",
            json={"common_name": "example.com"},
            wrap_ttl=None,
        )

    async def test_set_signed_intermediate_async(self):
        mock_response = Response(200, json={"data": {"message": "Intermediate certificate set"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.set_signed_intermediate(certificate="-----BEGIN CERTIFICATE-----")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Intermediate certificate set"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/intermediate/set-signed",
            json={"certificate": "-----BEGIN CERTIFICATE-----"},
        )

    async def test_generate_certificate_async(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.generate_certificate(name="test-role", common_name="example.com")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/issue/test-role",
            json={"common_name": "example.com"},
            wrap_ttl=None,
        )

    async def test_revoke_certificate_async(self):
        mock_response = Response(200, json={"data": {"message": "Certificate revoked"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.revoke_certificate(serial_number="12345")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Certificate revoked"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/revoke",
            json={"serial_number": "12345"},
        )

    async def test_create_or_update_role_async(self):
        mock_response = Response(200, json={"data": {"message": "Role created/updated"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.create_or_update_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Role created/updated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/roles/test-role",
            json={"name": "test-role"},
        )

    async def test_read_role_async(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.pki.read_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/roles/test-role",
        )

    async def test_list_roles_async(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.pki.list_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/pki/roles",
        )

    async def test_delete_role_async(self):
        mock_response = Response(200, json={"data": {"message": "Role deleted"}})
        self.mock_adapter.delete.return_value = mock_response

        result = await self.pki.delete_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Role deleted"}})
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/pki/roles/test-role",
        )

    async def test_generate_root_async(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.generate_root(_type="exported", common_name="example.com")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/root/generate/exported",
            json={"common_name": "example.com"},
            wrap_ttl=None,
        )

    async def test_delete_root_async(self):
        mock_response = Response(200, json={"data": {"message": "Root deleted"}})
        self.mock_adapter.delete.return_value = mock_response

        result = await self.pki.delete_root()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Root deleted"}})
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/pki/root",
        )

    async def test_sign_intermediate_async(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.sign_intermediate(csr="-----BEGIN CERTIFICATE REQUEST-----", common_name="example.com")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/root/sign-intermediate",
            json={"csr": "-----BEGIN CERTIFICATE REQUEST-----", "common_name": "example.com"},
        )

    async def test_sign_self_issued_async(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.sign_self_issued(certificate="-----BEGIN CERTIFICATE-----")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/root/sign-self-issued",
            json={"certificate": "-----BEGIN CERTIFICATE-----"},
        )

    async def test_sign_certificate_async(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.sign_certificate(name="test-role", csr="-----BEGIN CERTIFICATE REQUEST-----", common_name="example.com")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/sign/test-role",
            json={"csr": "-----BEGIN CERTIFICATE REQUEST-----", "common_name": "example.com"},
        )

    async def test_sign_verbatim_async(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.sign_verbatim(csr="-----BEGIN CERTIFICATE REQUEST-----")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/sign-verbatim",
            json={"csr": "-----BEGIN CERTIFICATE REQUEST-----"},
        )

    async def test_tidy_async(self):
        mock_response = Response(200, json={"data": {"message": "Tidy operation started"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.tidy()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Tidy operation started"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/tidy",
            json={},
        )

    async def test_read_issuer_async(self):
        mock_response = Response(200, json={"data": {"issuer_ref": "12345"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.pki.read_issuer(issuer_ref="12345")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"issuer_ref": "12345"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/pki/issuer/12345",
        )

    async def test_list_issuers_async(self):
        mock_response = Response(200, json={"data": {"keys": ["issuer1", "issuer2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.pki.list_issuers()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["issuer1", "issuer2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/pki/issuers",
        )

    async def test_update_issuer_async(self):
        mock_response = Response(200, json={"data": {"message": "Issuer updated"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.update_issuer(issuer_ref="12345", extra_params={"key": "value"})
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Issuer updated"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/issuer/12345",
            json={"key": "value"},
        )

    async def test_revoke_issuer_async(self):
        mock_response = Response(200, json={"data": {"message": "Issuer revoked"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.pki.revoke_issuer(issuer_ref="12345")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Issuer revoked"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/pki/issuer/12345/revoke",
        )

    async def test_delete_issuer_async(self):
        mock_response = Response(200, json={"data": {"message": "Issuer deleted"}})
        self.mock_adapter.delete.return_value = mock_response

        result = await self.pki.delete_issuer(issuer_ref="12345")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"message": "Issuer deleted"}})
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/pki/issuer/12345",
        )
