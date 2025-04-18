import logging
from unittest import IsolatedAsyncioTestCase, TestCase, skipIf

from parameterized import param, parameterized  # type: ignore

from tests import utils
from tests.utils.vaultx_integration_test_case import AsyncVaultxIntegrationTestCase, VaultxIntegrationTestCase
from vaultx import exceptions
from vaultx.adapters import VaultxResponse


class TestPki(VaultxIntegrationTestCase, TestCase):
    TEST_MOUNT_POINT = "pki-integration-test"
    TEST_ROLE = "role-test"

    def setUp(self):
        super().setUp()
        self.client.sys.enable_secrets_engine(
            backend_type="pki",
            path=self.TEST_MOUNT_POINT,
        )
        common_name = "Vault integration tests"
        generate_type = "exported"
        self.client.secrets.pki.generate_root(
            _type=generate_type,
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        name = self.TEST_ROLE
        self.client.secrets.pki.create_or_update_role(
            name=name,
            extra_params={
                "allow_any_name": True,
                "ttl": "6h",
                "max_ttl": "12h",
            },
            mount_point=self.TEST_MOUNT_POINT,
        )

    def tearDown(self):
        self.client.sys.disable_secrets_engine(path=self.TEST_MOUNT_POINT)
        super().tearDown()

    # Read CA Certificate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_read_ca_certificate(self, label, raises=False, exception_message=""):
        read_ca_certificate_response = self.client.secrets.pki.read_ca_certificate(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_ca_certificate_response: %s" % read_ca_certificate_response)
        self.assertIsInstance(
            obj=read_ca_certificate_response,
            cls=str,
        )

    # Read CA Certificate Chain
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_read_ca_certificate_chain(self, label, raises=False, exception_message=""):
        read_ca_certificate_chain_response = self.client.secrets.pki.read_ca_certificate_chain(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_ca_certificate_chain_response: %s" % read_ca_certificate_chain_response)
        self.assertIsInstance(
            obj=read_ca_certificate_chain_response,
            cls=str,
        )

    # Read Certificate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_read_certificate(self, label, raises=False, exception_message=""):
        list_certificates_response = self.client.secrets.pki.list_certificates(
            mount_point=self.TEST_MOUNT_POINT,
        )

        serial = list_certificates_response["data"]["keys"][0]
        read_certificate_response = self.client.secrets.pki.read_certificate(
            serial=serial,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_certificate_response: %s" % read_certificate_response)
        self.assertIsInstance(
            obj=read_certificate_response,
            cls=VaultxResponse,
        )

    # List Certificates
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_list_certificates(self, label, raises=False, exception_message=""):
        list_certificates_response = self.client.secrets.pki.list_certificates(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("list_certificates_response: %s" % list_certificates_response)
        self.assertIsInstance(
            obj=list_certificates_response,
            cls=VaultxResponse,
        )

    # Submit CA Information
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_submit_ca_information(self, label, raises=False, exception_message=""):
        pem_bundle = "{ca_key}{ca_crt}".format(
            ca_key="".join(open(utils.get_config_file_path("ca-key.pem")).readlines()),  # noqa: SIM115
            ca_crt="".join(open(utils.get_config_file_path("ca-cert.pem")).readlines()),  # noqa: SIM115
        )
        submit_ca_information_response = self.client.secrets.pki.submit_ca_information(
            pem_bundle=pem_bundle,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("submit_ca_information_response: %s" % submit_ca_information_response)
        self.assertEqual(
            first=bool(submit_ca_information_response),
            second=True,
        )

    # Read CRL Configuration
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_read_crl_configuration(self, label, raises=False, exception_message=""):
        expiry = "72h"
        self.client.secrets.pki.set_crl_configuration(
            expiry=expiry,
            mount_point=self.TEST_MOUNT_POINT,
        )

        read_crl_configuration_response = self.client.secrets.pki.read_crl_configuration(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_crl_configuration_response: %s" % read_crl_configuration_response)
        self.assertIsInstance(
            obj=read_crl_configuration_response,
            cls=VaultxResponse,
        )

    # Set CRL Configuration
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_set_crl_configuration(self, label, raises=False, exception_message=""):
        expiry = "72h"
        disable = False
        set_crl_configuration_response = self.client.secrets.pki.set_crl_configuration(
            expiry=expiry,
            disable=disable,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("set_crl_configuration_response: %s" % set_crl_configuration_response)
        self.assertEqual(
            first=bool(set_crl_configuration_response),
            second=True,
        )

    # Read URLs
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_read_urls(self, label, raises=False, exception_message=""):
        params = {
            "issuing_certificates": ["http://127.0.0.1:8200/v1/pki/ca"],
            "crl_distribution_points": ["http://127.0.0.1:8200/v1/pki/crl"],
        }
        self.client.secrets.pki.set_urls(
            params=params,
            mount_point=self.TEST_MOUNT_POINT,
        )
        read_urls_response = self.client.secrets.pki.read_urls(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_urls_response: %s" % read_urls_response)
        self.assertIsInstance(
            obj=read_urls_response,
            cls=VaultxResponse,
        )

    # Set URLs
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_set_urls(self, label, raises=False, exception_message=""):
        params = {
            "issuing_certificates": ["http://127.0.0.1:8200/v1/pki/ca"],
            "crl_distribution_points": ["http://127.0.0.1:8200/v1/pki/crl"],
        }
        set_urls_response = self.client.secrets.pki.set_urls(
            params=params,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("set_urls_response: %s" % set_urls_response)
        self.assertEqual(
            first=bool(set_urls_response),
            second=True,
        )

    # Read CRL
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_read_crl(self, label, raises=False, exception_message=""):
        expiry = "72h"
        self.client.secrets.pki.set_crl_configuration(
            expiry=expiry,
            mount_point=self.TEST_MOUNT_POINT,
        )

        read_crl_response = self.client.secrets.pki.read_crl(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_crl_response: %s" % read_crl_response)
        self.assertIsInstance(
            obj=read_crl_response,
            cls=str,
        )

    # Rotate CRLs
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_rotate_crl(self, label, raises=False, exception_message=""):
        rotate_crl_response = self.client.secrets.pki.rotate_crl(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("rotate_crl_response: %s" % rotate_crl_response)
        self.assertIsInstance(
            obj=rotate_crl_response,
            cls=VaultxResponse,
        )

    # Generate Intermediate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_generate_intermediate(self, label, raises=False, exception_message=""):
        common_name = "Vault integration tests"
        generate_type = "exported"
        generate_intermediate_response = self.client.secrets.pki.generate_intermediate(
            _type=generate_type,
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("generate_intermediate_response: %s" % generate_intermediate_response)
        self.assertEqual(
            first=bool(generate_intermediate_response),
            second=True,
        )

    # Set Signed Intermediate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_set_signed_intermediate(self, label, raises=False, exception_message=""):
        # Generate intermediate CA mount point
        ca_intermediate_pki_mount_point = "{}-signed-intermediate-ca".format(self.TEST_MOUNT_POINT)
        self.client.sys.enable_secrets_engine(
            backend_type="pki",
            path=ca_intermediate_pki_mount_point,
        )
        # Generate intermediate CA
        common_name = "Vault integration tests intermediate CA"
        generate_type = "exported"
        generate_intermediate_response = self.client.secrets.pki.generate_intermediate(
            _type=generate_type,
            common_name=common_name,
            mount_point=ca_intermediate_pki_mount_point,
        )
        logging.debug("generate_intermediate_response: %s" % generate_intermediate_response)
        csr = generate_intermediate_response["data"]["csr"]

        # Sign intermediate CA
        sign_intermediate_response = self.client.secrets.pki.sign_intermediate(
            csr=csr,
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("sign_intermediate_response: %s" % sign_intermediate_response)
        certificate = sign_intermediate_response["data"]["certificate"]

        # Finally test Set Signed Intermediate
        set_signed_intermediate_response = self.client.secrets.pki.set_signed_intermediate(
            certificate=certificate,
            mount_point=ca_intermediate_pki_mount_point,
        )
        logging.debug("set_signed_intermediate_response: %s" % set_signed_intermediate_response)
        self.assertEqual(
            first=bool(set_signed_intermediate_response),
            second=True,
        )

        # Now clean intermediate CA
        self.client.sys.disable_secrets_engine(path=ca_intermediate_pki_mount_point)

    # Generate Certificate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_generate_certificate(self, label, raises=False, exception_message=""):
        name = self.TEST_ROLE
        common_name = "test.example.com"
        generate_certificate_response = self.client.secrets.pki.generate_certificate(
            name=name,
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("generate_certificate_response: %s" % generate_certificate_response)
        self.assertEqual(
            first=bool(generate_certificate_response),
            second=True,
        )

    # Revoke Certificate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_revoke_certificate(self, label, raises=False, exception_message=""):
        name = self.TEST_ROLE
        common_name = "test.example.com"
        generate_certificate_response = self.client.secrets.pki.generate_certificate(
            name=name,
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("generate_certificate_response: %s" % generate_certificate_response)
        serial_number = generate_certificate_response["data"]["serial_number"]
        logging.debug("serial_number: %s" % serial_number)
        revoke_certificate_response = self.client.secrets.pki.revoke_certificate(
            serial_number=serial_number,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("revoke_certificate_response: %s" % revoke_certificate_response)
        self.assertEqual(
            first=bool(revoke_certificate_response),
            second=True,
        )

    # Create/Update Role
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_create_or_update_role(self, label, raises=False, exception_message=""):
        name = f"{self.TEST_ROLE}-2"
        create_or_update_role_response = self.client.secrets.pki.create_or_update_role(
            name=name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("create_or_update_role_response: %s" % create_or_update_role_response)
        self.assertEqual(
            first=bool(create_or_update_role_response),
            second=True,
        )

    # Read Role
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_read_role(self, label, raises=False, exception_message=""):
        read_role_response = self.client.secrets.pki.read_role(
            name=self.TEST_ROLE,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_role_response: %s" % read_role_response)
        self.assertIsInstance(
            obj=read_role_response,
            cls=VaultxResponse,
        )

    # List Roles
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_list_roles(self, label, raises=False, exception_message=""):
        list_roles_response = self.client.secrets.pki.list_roles(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("list_roles_response: %s" % list_roles_response)
        self.assertIsInstance(
            obj=list_roles_response,
            cls=VaultxResponse,
        )

    # Delete Role
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_delete_role(self, label, raises=False, exception_message=""):
        name = f"{self.TEST_ROLE}-2"
        self.client.secrets.pki.create_or_update_role(
            name=name,
            mount_point=self.TEST_MOUNT_POINT,
        )

        delete_role_response = self.client.secrets.pki.delete_role(
            name=name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("delete_role_response: %s" % delete_role_response)
        self.assertEqual(
            first=bool(delete_role_response),
            second=True,
        )

    # Generate Root
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_generate_root(self, label, raises=False, exception_message=""):
        ca_pki_mount_point = f"{self.TEST_MOUNT_POINT}-test-ca"
        self.client.sys.enable_secrets_engine(
            backend_type="pki",
            path=ca_pki_mount_point,
        )
        common_name = "Vault integration tests"
        generate_type = "exported"
        generate_root_response = self.client.secrets.pki.generate_root(
            _type=generate_type,
            common_name=common_name,
            mount_point=ca_pki_mount_point,
        )
        logging.debug("generate_root_response: %s" % generate_root_response)
        self.assertEqual(
            first=bool(generate_root_response),
            second=True,
        )
        self.client.sys.disable_secrets_engine(path=ca_pki_mount_point)

    # Delete Root
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_delete_root(self, label, raises=False, exception_message=""):
        ca_pki_mount_point = f"{self.TEST_MOUNT_POINT}-test-ca"
        self.client.sys.enable_secrets_engine(
            backend_type="pki",
            path=ca_pki_mount_point,
        )
        common_name = "Vault integration tests"
        generate_type = "exported"
        self.client.secrets.pki.generate_root(
            _type=generate_type,
            common_name=common_name,
            mount_point=ca_pki_mount_point,
        )

        delete_root_response = self.client.secrets.pki.delete_root(
            mount_point=ca_pki_mount_point,
        )
        logging.debug("delete_root_response: %s" % delete_root_response)
        self.assertEqual(
            first=bool(delete_root_response),
            second=True,
        )
        self.client.sys.disable_secrets_engine(path=ca_pki_mount_point)

    # Sign Intermediate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_sign_intermediate(self, label, raises=False, exception_message=""):
        # Generate intermediate CA
        ca_intermediate_pki_mount_point = "{}-intermediate-ca".format(self.TEST_MOUNT_POINT)
        self.client.sys.enable_secrets_engine(
            backend_type="pki",
            path=ca_intermediate_pki_mount_point,
        )
        common_name = "Vault integration tests intermediate CA"
        generate_type = "exported"
        generate_intermediate_response = self.client.secrets.pki.generate_intermediate(
            _type=generate_type,
            common_name=common_name,
            mount_point=ca_intermediate_pki_mount_point,
        )
        logging.debug("generate_intermediate_response: %s" % generate_intermediate_response)
        csr = generate_intermediate_response["data"]["csr"]

        sign_intermediate_response = self.client.secrets.pki.sign_intermediate(
            csr=csr,
            common_name=common_name,
            extra_params={"use_csr_values": True},
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("sign_intermediate_response: %s" % sign_intermediate_response)
        self.assertEqual(
            first=bool(sign_intermediate_response),
            second=True,
        )
        # Now clean intermediate CA
        self.client.sys.disable_secrets_engine(path=ca_intermediate_pki_mount_point)

    # Sign Self-Issued
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_sign_self_issued(self, label, raises=False, exception_message=""):
        sign_self_issued_response = self.client.secrets.pki.sign_self_issued(
            certificate="".join(open(utils.get_config_file_path("ca-cert.pem")).readlines()),  # noqa: SIM115
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("sign_self_issued_response: %s" % sign_self_issued_response)
        self.assertEqual(
            first=bool(sign_self_issued_response),
            second=True,
        )

    # Sign Certificate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_sign_certificate(self, label, raises=False, exception_message=""):
        name = self.TEST_ROLE
        common_name = "another.example.com"
        sign_certificate_response = self.client.secrets.pki.sign_certificate(
            name=name,
            csr="".join(open(utils.get_config_file_path("server-cert.csr")).readlines()),  # noqa: SIM115
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("sign_certificate_response: %s" % sign_certificate_response)
        self.assertEqual(
            first=bool(sign_certificate_response),
            second=True,
        )

    # Sign Verbatim
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_sign_verbatim(self, label, raises=False, exception_message=""):
        name = self.TEST_ROLE
        sign_verbatim_response = self.client.secrets.pki.sign_verbatim(
            csr="".join(open(utils.get_config_file_path("server-cert.csr")).readlines()),  # noqa: SIM115
            name=name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("sign_verbatim_response: %s" % sign_verbatim_response)
        self.assertEqual(
            first=bool(sign_verbatim_response),
            second=True,
        )

    # Tidy
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    def test_tidy(self, label, raises=False, exception_message=""):
        tidy_response = self.client.secrets.pki.tidy(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("tidy_response: %s" % tidy_response)
        self.assertEqual(
            first=bool(tidy_response),
            second=True,
        )

    # Read issuer
    @skipIf(utils.vault_version_lt("1.11.0"), reason="Support added in version 1.11.0.")
    def test_read_issuer(self):
        pki_list_response = self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        self.assertIn(
            member="issuer_name",
            container=self.client.secrets.pki.read_issuer(
                issuer_ref=pki_list_response["data"]["keys"][0],
                mount_point=self.TEST_MOUNT_POINT,
            )["data"].keys(),
        )

    # List issuer
    @skipIf(utils.vault_version_lt("1.11.0"), reason="Support added in version 1.11.0.")
    def test_list_issuers(self):
        pki_list_response = self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        self.assertIn("keys", pki_list_response["data"].keys())

    # Update issuer
    @skipIf(utils.vault_version_lt("1.11.0"), reason="Support added in version 1.11.0.")
    def test_update_issuer(self):
        pki_list_response = self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        new_name = "new_issuer_name"

        self.client.secrets.pki.update_issuer(
            issuer_ref=pki_list_response["data"]["keys"][0],
            mount_point=self.TEST_MOUNT_POINT,
            extra_params={"issuer_name": new_name},
        )

        self.assertEqual(
            first=self.client.secrets.pki.read_issuer(
                issuer_ref=pki_list_response["data"]["keys"][0],
                mount_point=self.TEST_MOUNT_POINT,
            )["data"]["issuer_name"],
            second=new_name,
        )

    # Update issuer - no extra params
    @skipIf(utils.vault_version_lt("1.11.0"), reason="Support added in version 1.11.0.")
    def test_update_issuer_no_extra_param(self):
        pki_list_response = self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        # Read current state of issuer to make sure nothing changes
        pki_read_response = self.client.secrets.pki.read_issuer(
            issuer_ref=pki_list_response["data"]["keys"][0],
            mount_point=self.TEST_MOUNT_POINT,
        )

        pki_update_response = self.client.secrets.pki.update_issuer(
            issuer_ref=pki_list_response["data"]["keys"][0],
            mount_point=self.TEST_MOUNT_POINT,
        )

        self.assertCountEqual(
            first=pki_update_response["data"]["usage"].split(","),
            second=pki_read_response["data"]["usage"].split(","),
        )

    # Revoke issuer
    @skipIf(utils.vault_version_lt("1.12.0"), reason="Support added in version 1.12.0.")
    def test_revoke_issuer(self):
        pki_list_response = self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        self.client.secrets.pki.revoke_issuer(
            issuer_ref=pki_list_response["data"]["keys"][0],
            mount_point=self.TEST_MOUNT_POINT,
        )

        self.assertEqual(
            first=self.client.secrets.pki.read_issuer(
                issuer_ref=pki_list_response["data"]["keys"][0],
                mount_point=self.TEST_MOUNT_POINT,
            )["data"]["revoked"],
            second=True,
        )

    # Revoke issuer
    @skipIf(utils.vault_version_lt("1.11.0"), reason="Support added in version 1.11.0.")
    def test_delete_issuer(self):
        pki_list_response = self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        self.client.secrets.pki.delete_issuer(
            issuer_ref=pki_list_response["data"]["keys"][0],
            mount_point=self.TEST_MOUNT_POINT,
        )

        with self.assertRaises(exceptions.HTTPError):
            self.client.secrets.pki.read_issuer(
                issuer_ref=pki_list_response["data"]["keys"][0],
                mount_point=self.TEST_MOUNT_POINT,
            )


class TestAsyncPki(AsyncVaultxIntegrationTestCase, IsolatedAsyncioTestCase):
    TEST_MOUNT_POINT = "pki-integration-test"
    TEST_ROLE = "role-test"

    async def asyncSetUp(self):
        await super().asyncSetUp()
        await self.client.sys.enable_secrets_engine(
            backend_type="pki",
            path=self.TEST_MOUNT_POINT,
        )
        common_name = "Vault integration tests"
        generate_type = "exported"
        await self.client.secrets.pki.generate_root(
            _type=generate_type,
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        name = self.TEST_ROLE
        await self.client.secrets.pki.create_or_update_role(
            name=name,
            extra_params={
                "allow_any_name": True,
                "ttl": "6h",
                "max_ttl": "12h",
            },
            mount_point=self.TEST_MOUNT_POINT,
        )

    async def asyncTearDown(self):
        await self.client.sys.disable_secrets_engine(path=self.TEST_MOUNT_POINT)
        await super().asyncTearDown()

    # Read CA Certificate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_read_ca_certificate(self, label, raises=False, exception_message=""):
        read_ca_certificate_response = await self.client.secrets.pki.read_ca_certificate(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_ca_certificate_response: %s" % read_ca_certificate_response)
        self.assertIsInstance(
            obj=read_ca_certificate_response,
            cls=str,
        )

    # Read CA Certificate Chain
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_read_ca_certificate_chain(self, label, raises=False, exception_message=""):
        read_ca_certificate_chain_response = await self.client.secrets.pki.read_ca_certificate_chain(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_ca_certificate_chain_response: %s" % read_ca_certificate_chain_response)
        self.assertIsInstance(
            obj=read_ca_certificate_chain_response,
            cls=str,
        )

    # Read Certificate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_read_certificate(self, label, raises=False, exception_message=""):
        list_certificates_response = await self.client.secrets.pki.list_certificates(
            mount_point=self.TEST_MOUNT_POINT,
        )

        serial = list_certificates_response["data"]["keys"][0]
        read_certificate_response = await self.client.secrets.pki.read_certificate(
            serial=serial,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_certificate_response: %s" % read_certificate_response)
        self.assertIsInstance(
            obj=read_certificate_response,
            cls=VaultxResponse,
        )

    # List Certificates
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_list_certificates(self, label, raises=False, exception_message=""):
        list_certificates_response = await self.client.secrets.pki.list_certificates(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("list_certificates_response: %s" % list_certificates_response)
        self.assertIsInstance(
            obj=list_certificates_response,
            cls=VaultxResponse,
        )

    # Submit CA Information
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_submit_ca_information(self, label, raises=False, exception_message=""):
        pem_bundle = "{ca_key}{ca_crt}".format(
            ca_key="".join(open(utils.get_config_file_path("ca-key.pem")).readlines()),  # noqa: SIM115
            ca_crt="".join(open(utils.get_config_file_path("ca-cert.pem")).readlines()),  # noqa: SIM115
        )
        submit_ca_information_response = await self.client.secrets.pki.submit_ca_information(
            pem_bundle=pem_bundle,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("submit_ca_information_response: %s" % submit_ca_information_response)
        self.assertEqual(
            first=bool(submit_ca_information_response),
            second=True,
        )

    # Read CRL Configuration
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_read_crl_configuration(self, label, raises=False, exception_message=""):
        expiry = "72h"
        await self.client.secrets.pki.set_crl_configuration(
            expiry=expiry,
            mount_point=self.TEST_MOUNT_POINT,
        )

        read_crl_configuration_response = await self.client.secrets.pki.read_crl_configuration(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_crl_configuration_response: %s" % read_crl_configuration_response)
        self.assertIsInstance(
            obj=read_crl_configuration_response,
            cls=VaultxResponse,
        )

    # Set CRL Configuration
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_set_crl_configuration(self, label, raises=False, exception_message=""):
        expiry = "72h"
        disable = False
        set_crl_configuration_response = await self.client.secrets.pki.set_crl_configuration(
            expiry=expiry,
            disable=disable,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("set_crl_configuration_response: %s" % set_crl_configuration_response)
        self.assertEqual(
            first=bool(set_crl_configuration_response),
            second=True,
        )

    # Read URLs
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_read_urls(self, label, raises=False, exception_message=""):
        params = {
            "issuing_certificates": ["http://127.0.0.1:8200/v1/pki/ca"],
            "crl_distribution_points": ["http://127.0.0.1:8200/v1/pki/crl"],
        }
        await self.client.secrets.pki.set_urls(
            params=params,
            mount_point=self.TEST_MOUNT_POINT,
        )
        read_urls_response = await self.client.secrets.pki.read_urls(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_urls_response: %s" % read_urls_response)
        self.assertIsInstance(
            obj=read_urls_response,
            cls=VaultxResponse,
        )

    # Set URLs
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_set_urls(self, label, raises=False, exception_message=""):
        params = {
            "issuing_certificates": ["http://127.0.0.1:8200/v1/pki/ca"],
            "crl_distribution_points": ["http://127.0.0.1:8200/v1/pki/crl"],
        }
        set_urls_response = await self.client.secrets.pki.set_urls(
            params=params,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("set_urls_response: %s" % set_urls_response)
        self.assertEqual(
            first=bool(set_urls_response),
            second=True,
        )

    # Read CRL
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_read_crl(self, label, raises=False, exception_message=""):
        expiry = "72h"
        await self.client.secrets.pki.set_crl_configuration(
            expiry=expiry,
            mount_point=self.TEST_MOUNT_POINT,
        )

        read_crl_response = await self.client.secrets.pki.read_crl(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_crl_response: %s" % read_crl_response)
        self.assertIsInstance(
            obj=read_crl_response,
            cls=str,
        )

    # Rotate CRLs
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_rotate_crl(self, label, raises=False, exception_message=""):
        rotate_crl_response = await self.client.secrets.pki.rotate_crl(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("rotate_crl_response: %s" % rotate_crl_response)
        self.assertIsInstance(
            obj=rotate_crl_response,
            cls=VaultxResponse,
        )

    # Generate Intermediate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_generate_intermediate(self, label, raises=False, exception_message=""):
        common_name = "Vault integration tests"
        generate_type = "exported"
        generate_intermediate_response = await self.client.secrets.pki.generate_intermediate(
            _type=generate_type,
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("generate_intermediate_response: %s" % generate_intermediate_response)
        self.assertEqual(
            first=bool(generate_intermediate_response),
            second=True,
        )

    # Set Signed Intermediate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_set_signed_intermediate(self, label, raises=False, exception_message=""):
        # Generate intermediate CA mount point
        ca_intermediate_pki_mount_point = "{}-signed-intermediate-ca".format(self.TEST_MOUNT_POINT)
        await self.client.sys.enable_secrets_engine(
            backend_type="pki",
            path=ca_intermediate_pki_mount_point,
        )
        # Generate intermediate CA
        common_name = "Vault integration tests intermediate CA"
        generate_type = "exported"
        generate_intermediate_response = await self.client.secrets.pki.generate_intermediate(
            _type=generate_type,
            common_name=common_name,
            mount_point=ca_intermediate_pki_mount_point,
        )
        logging.debug("generate_intermediate_response: %s" % generate_intermediate_response)
        csr = generate_intermediate_response["data"]["csr"]

        # Sign intermediate CA
        sign_intermediate_response = await self.client.secrets.pki.sign_intermediate(
            csr=csr,
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("sign_intermediate_response: %s" % sign_intermediate_response)
        certificate = sign_intermediate_response["data"]["certificate"]

        # Finally test Set Signed Intermediate
        set_signed_intermediate_response = await self.client.secrets.pki.set_signed_intermediate(
            certificate=certificate,
            mount_point=ca_intermediate_pki_mount_point,
        )
        logging.debug("set_signed_intermediate_response: %s" % set_signed_intermediate_response)
        self.assertEqual(
            first=bool(set_signed_intermediate_response),
            second=True,
        )

        # Now clean intermediate CA
        await self.client.sys.disable_secrets_engine(path=ca_intermediate_pki_mount_point)

    # Generate Certificate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_generate_certificate(self, label, raises=False, exception_message=""):
        name = self.TEST_ROLE
        common_name = "test.example.com"
        generate_certificate_response = await self.client.secrets.pki.generate_certificate(
            name=name,
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("generate_certificate_response: %s" % generate_certificate_response)
        self.assertEqual(
            first=bool(generate_certificate_response),
            second=True,
        )

    # Revoke Certificate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_revoke_certificate(self, label, raises=False, exception_message=""):
        name = self.TEST_ROLE
        common_name = "test.example.com"
        generate_certificate_response = await self.client.secrets.pki.generate_certificate(
            name=name,
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("generate_certificate_response: %s" % generate_certificate_response)
        serial_number = generate_certificate_response["data"]["serial_number"]
        logging.debug("serial_number: %s" % serial_number)
        revoke_certificate_response = await self.client.secrets.pki.revoke_certificate(
            serial_number=serial_number,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("revoke_certificate_response: %s" % revoke_certificate_response)
        self.assertEqual(
            first=bool(revoke_certificate_response),
            second=True,
        )

    # Create/Update Role
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_create_or_update_role(self, label, raises=False, exception_message=""):
        name = f"{self.TEST_ROLE}-2"
        create_or_update_role_response = await self.client.secrets.pki.create_or_update_role(
            name=name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("create_or_update_role_response: %s" % create_or_update_role_response)
        self.assertEqual(
            first=bool(create_or_update_role_response),
            second=True,
        )

    # Read Role
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_read_role(self, label, raises=False, exception_message=""):
        read_role_response = await self.client.secrets.pki.read_role(
            name=self.TEST_ROLE,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("read_role_response: %s" % read_role_response)
        self.assertIsInstance(
            obj=read_role_response,
            cls=VaultxResponse,
        )

    # List Roles
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_list_roles(self, label, raises=False, exception_message=""):
        list_roles_response = await self.client.secrets.pki.list_roles(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("list_roles_response: %s" % list_roles_response)
        self.assertIsInstance(
            obj=list_roles_response,
            cls=VaultxResponse,
        )

    # Delete Role
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_delete_role(self, label, raises=False, exception_message=""):
        name = f"{self.TEST_ROLE}-2"
        await self.client.secrets.pki.create_or_update_role(
            name=name,
            mount_point=self.TEST_MOUNT_POINT,
        )

        delete_role_response = await self.client.secrets.pki.delete_role(
            name=name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("delete_role_response: %s" % delete_role_response)
        self.assertEqual(
            first=bool(delete_role_response),
            second=True,
        )

    # Generate Root
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_generate_root(self, label, raises=False, exception_message=""):
        ca_pki_mount_point = f"{self.TEST_MOUNT_POINT}-test-ca"
        await self.client.sys.enable_secrets_engine(
            backend_type="pki",
            path=ca_pki_mount_point,
        )
        common_name = "Vault integration tests"
        generate_type = "exported"
        generate_root_response = await self.client.secrets.pki.generate_root(
            _type=generate_type,
            common_name=common_name,
            mount_point=ca_pki_mount_point,
        )
        logging.debug("generate_root_response: %s" % generate_root_response)
        self.assertEqual(
            first=bool(generate_root_response),
            second=True,
        )
        await self.client.sys.disable_secrets_engine(path=ca_pki_mount_point)

    # Delete Root
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_delete_root(self, label, raises=False, exception_message=""):
        ca_pki_mount_point = f"{self.TEST_MOUNT_POINT}-test-ca"
        await self.client.sys.enable_secrets_engine(
            backend_type="pki",
            path=ca_pki_mount_point,
        )
        common_name = "Vault integration tests"
        generate_type = "exported"
        await self.client.secrets.pki.generate_root(
            _type=generate_type,
            common_name=common_name,
            mount_point=ca_pki_mount_point,
        )

        delete_root_response = await self.client.secrets.pki.delete_root(
            mount_point=ca_pki_mount_point,
        )
        logging.debug("delete_root_response: %s" % delete_root_response)
        self.assertEqual(
            first=bool(delete_root_response),
            second=True,
        )
        await self.client.sys.disable_secrets_engine(path=ca_pki_mount_point)

    # Sign Intermediate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_sign_intermediate(self, label, raises=False, exception_message=""):
        # Generate intermediate CA
        ca_intermediate_pki_mount_point = "{}-intermediate-ca".format(self.TEST_MOUNT_POINT)
        await self.client.sys.enable_secrets_engine(
            backend_type="pki",
            path=ca_intermediate_pki_mount_point,
        )
        common_name = "Vault integration tests intermediate CA"
        generate_type = "exported"
        generate_intermediate_response = await self.client.secrets.pki.generate_intermediate(
            _type=generate_type,
            common_name=common_name,
            mount_point=ca_intermediate_pki_mount_point,
        )
        logging.debug("generate_intermediate_response: %s" % generate_intermediate_response)
        csr = generate_intermediate_response["data"]["csr"]

        sign_intermediate_response = await self.client.secrets.pki.sign_intermediate(
            csr=csr,
            common_name=common_name,
            extra_params={"use_csr_values": True},
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("sign_intermediate_response: %s" % sign_intermediate_response)
        self.assertEqual(
            first=bool(sign_intermediate_response),
            second=True,
        )
        # Now clean intermediate CA
        await self.client.sys.disable_secrets_engine(path=ca_intermediate_pki_mount_point)

    # Sign Self-Issued
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_sign_self_issued(self, label, raises=False, exception_message=""):
        sign_self_issued_response = await self.client.secrets.pki.sign_self_issued(
            certificate="".join(open(utils.get_config_file_path("ca-cert.pem")).readlines()),  # noqa: SIM115
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("sign_self_issued_response: %s" % sign_self_issued_response)
        self.assertEqual(
            first=bool(sign_self_issued_response),
            second=True,
        )

    # Sign Certificate
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_sign_certificate(self, label, raises=False, exception_message=""):
        name = self.TEST_ROLE
        common_name = "another.example.com"
        sign_certificate_response = await self.client.secrets.pki.sign_certificate(
            name=name,
            csr="".join(open(utils.get_config_file_path("server-cert.csr")).readlines()),  # noqa: SIM115
            common_name=common_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("sign_certificate_response: %s" % sign_certificate_response)
        self.assertEqual(
            first=bool(sign_certificate_response),
            second=True,
        )

    # Sign Verbatim
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_sign_verbatim(self, label, raises=False, exception_message=""):
        name = self.TEST_ROLE
        sign_verbatim_response = await self.client.secrets.pki.sign_verbatim(
            csr="".join(open(utils.get_config_file_path("server-cert.csr")).readlines()),  # noqa: SIM115
            name=name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("sign_verbatim_response: %s" % sign_verbatim_response)
        self.assertEqual(
            first=bool(sign_verbatim_response),
            second=True,
        )

    # Tidy
    @parameterized.expand(
        [
            param(
                "success",
            ),
        ]
    )
    async def test_tidy(self, label, raises=False, exception_message=""):
        tidy_response = await self.client.secrets.pki.tidy(
            mount_point=self.TEST_MOUNT_POINT,
        )
        logging.debug("tidy_response: %s" % tidy_response)
        self.assertEqual(
            first=bool(tidy_response),
            second=True,
        )

    # Read issuer
    @skipIf(utils.vault_version_lt("1.11.0"), reason="Support added in version 1.11.0.")
    async def test_read_issuer(self):
        pki_list_response = await self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        self.assertIn(
            member="issuer_name",
            container=(
                await self.client.secrets.pki.read_issuer(
                    issuer_ref=pki_list_response["data"]["keys"][0],
                    mount_point=self.TEST_MOUNT_POINT,
                )
            )["data"].keys(),
        )

    # List issuer
    @skipIf(utils.vault_version_lt("1.11.0"), reason="Support added in version 1.11.0.")
    async def test_list_issuers(self):
        pki_list_response = await self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        self.assertIn("keys", pki_list_response["data"].keys())

    # Update issuer
    @skipIf(utils.vault_version_lt("1.11.0"), reason="Support added in version 1.11.0.")
    async def test_update_issuer(self):
        pki_list_response = await self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        new_name = "new_issuer_name"

        await self.client.secrets.pki.update_issuer(
            issuer_ref=pki_list_response["data"]["keys"][0],
            mount_point=self.TEST_MOUNT_POINT,
            extra_params={"issuer_name": new_name},
        )

        self.assertEqual(
            first=(
                await self.client.secrets.pki.read_issuer(
                    issuer_ref=pki_list_response["data"]["keys"][0],
                    mount_point=self.TEST_MOUNT_POINT,
                )
            )["data"]["issuer_name"],
            second=new_name,
        )

    # Update issuer - no extra params
    @skipIf(utils.vault_version_lt("1.11.0"), reason="Support added in version 1.11.0.")
    async def test_update_issuer_no_extra_param(self):
        pki_list_response = await self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        # Read current state of issuer to make sure nothing changes
        pki_read_response = await self.client.secrets.pki.read_issuer(
            issuer_ref=pki_list_response["data"]["keys"][0],
            mount_point=self.TEST_MOUNT_POINT,
        )

        pki_update_response = await self.client.secrets.pki.update_issuer(
            issuer_ref=pki_list_response["data"]["keys"][0],
            mount_point=self.TEST_MOUNT_POINT,
        )

        self.assertCountEqual(
            first=pki_update_response["data"]["usage"].split(","),
            second=pki_read_response["data"]["usage"].split(","),
        )

    # Revoke issuer
    @skipIf(utils.vault_version_lt("1.12.0"), reason="Support added in version 1.12.0.")
    async def test_revoke_issuer(self):
        pki_list_response = await self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        await self.client.secrets.pki.revoke_issuer(
            issuer_ref=pki_list_response["data"]["keys"][0],
            mount_point=self.TEST_MOUNT_POINT,
        )

        self.assertEqual(
            first=(
                await self.client.secrets.pki.read_issuer(
                    issuer_ref=pki_list_response["data"]["keys"][0],
                    mount_point=self.TEST_MOUNT_POINT,
                )
            )["data"]["revoked"],
            second=True,
        )

    # Revoke issuer
    @skipIf(utils.vault_version_lt("1.11.0"), reason="Support added in version 1.11.0.")
    async def test_delete_issuer(self):
        pki_list_response = await self.client.secrets.pki.list_issuers(mount_point=self.TEST_MOUNT_POINT)

        logging.debug("pki_list_response: %s" % pki_list_response)

        await self.client.secrets.pki.delete_issuer(
            issuer_ref=pki_list_response["data"]["keys"][0],
            mount_point=self.TEST_MOUNT_POINT,
        )

        with self.assertRaises(exceptions.HTTPError):
            await self.client.secrets.pki.read_issuer(
                issuer_ref=pki_list_response["data"]["keys"][0],
                mount_point=self.TEST_MOUNT_POINT,
            )
