import logging
from unittest import TestCase
from unittest.async_case import IsolatedAsyncioTestCase

from parameterized import param, parameterized  # type: ignore

from tests.utils.vaultx_integration_test_case import AsyncVaultxIntegrationTestCase, VaultxIntegrationTestCase
from vaultx import exceptions


class TestAudit(VaultxIntegrationTestCase, TestCase):
    TEST_AUDIT_DEVICE_PATH = "test-tempfile"

    def tearDown(self):
        self.client.sys.disable_audit_device(path=self.TEST_AUDIT_DEVICE_PATH)

    def test_audit_backend_manipulation(self):
        options = {"path": "/tmp/vault.audit.log"}

        self.client.sys.enable_audit_device(
            device_type="file",
            options=options,
            path=self.TEST_AUDIT_DEVICE_PATH,
        )
        self.assertIn(
            member="%s/" % self.TEST_AUDIT_DEVICE_PATH,
            container=self.client.sys.list_enabled_audit_devices()["data"],
        )

        self.client.sys.disable_audit_device(
            path=self.TEST_AUDIT_DEVICE_PATH,
        )
        self.assertNotIn(
            member="%s/" % self.TEST_AUDIT_DEVICE_PATH,
            container=self.client.sys.list_enabled_audit_devices()["data"],
        )

    @parameterized.expand(
        [
            param(
                "hash returned",
            ),
            param(
                "audit backend not enabled",
                enable_first=False,
                raises=exceptions.HTTPError,
                exception_message="400",
            ),
        ]
    )
    def test_audit_hash(
        self,
        label,
        enable_first=True,
        test_input="vaultx-rox",
        raises=None,
        exception_message="",
    ):
        if enable_first:
            options = {"path": "/tmp/vault.audit.log"}
            self.client.sys.enable_audit_device(
                device_type="file",
                options=options,
                path=self.TEST_AUDIT_DEVICE_PATH,
            )

        if raises:
            with self.assertRaises(raises) as cm:
                self.client.sys.calculate_hash(
                    path=self.TEST_AUDIT_DEVICE_PATH,
                    input_to_hash=test_input,
                )
            if exception_message is not None:
                self.assertIn(
                    member=exception_message,
                    container=str(cm.exception),
                )
        else:
            audit_hash_response = self.client.sys.calculate_hash(
                path=self.TEST_AUDIT_DEVICE_PATH,
                input_to_hash=test_input,
            )
            logging.debug("audit_hash_response: %s" % audit_hash_response)
            self.assertIn(
                member="hmac-sha256:",
                container=audit_hash_response["data"]["hash"],
            )


class TestAsyncAudit(AsyncVaultxIntegrationTestCase, IsolatedAsyncioTestCase):
    TEST_AUDIT_DEVICE_PATH = "test-tempfile"

    async def asyncTearDown(self):
        await self.client.sys.disable_audit_device(path=self.TEST_AUDIT_DEVICE_PATH)

    async def test_audit_backend_manipulation(self):
        options = {"path": "/tmp/vault.audit.log"}

        await self.client.sys.enable_audit_device(
            device_type="file",
            options=options,
            path=self.TEST_AUDIT_DEVICE_PATH,
        )
        self.assertIn(
            member="%s/" % self.TEST_AUDIT_DEVICE_PATH,
            container=(await self.client.sys.list_enabled_audit_devices())["data"],
        )

        await self.client.sys.disable_audit_device(
            path=self.TEST_AUDIT_DEVICE_PATH,
        )
        self.assertNotIn(
            member="%s/" % self.TEST_AUDIT_DEVICE_PATH,
            container=(await self.client.sys.list_enabled_audit_devices())["data"],
        )

    @parameterized.expand(
        [
            param(
                "hash returned",
            ),
            param(
                "audit backend not enabled",
                enable_first=False,
                raises=exceptions.HTTPError,
                exception_message="400",
            ),
        ]
    )
    async def test_audit_hash(
        self,
        label,
        enable_first=True,
        test_input="vaultx-rox",
        raises=None,
        exception_message="",
    ):
        if enable_first:
            options = {"path": "/tmp/vault.audit.log"}
            await self.client.sys.enable_audit_device(
                device_type="file",
                options=options,
                path=self.TEST_AUDIT_DEVICE_PATH,
            )

        if raises:
            with self.assertRaises(raises) as cm:
                await self.client.sys.calculate_hash(
                    path=self.TEST_AUDIT_DEVICE_PATH,
                    input_to_hash=test_input,
                )
            if exception_message is not None:
                self.assertIn(
                    member=exception_message,
                    container=str(cm.exception),
                )
        else:
            audit_hash_response = await self.client.sys.calculate_hash(
                path=self.TEST_AUDIT_DEVICE_PATH,
                input_to_hash=test_input,
            )
            logging.debug("audit_hash_response: %s" % audit_hash_response)
            self.assertIn(
                member="hmac-sha256:",
                container=audit_hash_response["data"]["hash"],
            )
