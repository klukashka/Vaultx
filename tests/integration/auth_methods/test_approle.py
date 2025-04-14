from unittest import IsolatedAsyncioTestCase, TestCase, skipIf

from parameterized import parameterized  # type: ignore

from tests import utils
from tests.utils.vaultx_integration_test_case import AsyncVaultxIntegrationTestCase, VaultxIntegrationTestCase
from vaultx import exceptions


@skipIf(utils.vault_version_lt("0.6.2"), "AppRole endpoints standardized in version 0.6.2")
class TestAppRole(VaultxIntegrationTestCase, TestCase):
    TEST_MOUNT_POINT = "approle-test"
    TEST_ROLE_NAME = "testrole"
    TEST_ROLE_ID = "test_role_id"
    TEST_SECRET_ID = "custom_secret"

    def setUp(self):
        super().setUp()
        if "%s/" % self.TEST_MOUNT_POINT not in self.client.sys.list_auth_methods():
            self.client.sys.enable_auth_method(
                method_type="approle",
                path=self.TEST_MOUNT_POINT,
            )
        self.client.auth.approle.create_or_update_approle(
            role_name=self.TEST_ROLE_NAME,
            token_policies=["default"],
            mount_point=self.TEST_MOUNT_POINT,
        )
        self.client.auth.approle.update_role_id(
            role_name=self.TEST_ROLE_NAME,
            role_id=self.TEST_ROLE_ID,
            mount_point=self.TEST_MOUNT_POINT,
        )

    def tearDown(self):
        super().tearDown()
        self.client.sys.disable_auth_method(path=self.TEST_MOUNT_POINT)

    def _secret_id(self):
        secret_id_response = self.client.auth.approle.generate_secret_id(
            role_name=self.TEST_ROLE_NAME,
            cidr_list=["127.0.0.1/32"],
            mount_point=self.TEST_MOUNT_POINT,
        )
        return secret_id_response["data"]

    @parameterized.expand(
        [
            ("create test role", "default", None),
            ("bad token type", "bad_token", exceptions.VaultxError),
        ]
    )
    def test_create_or_update_approle(self, test_label, token_type, raises):
        if raises is not None:
            with self.assertRaises(raises) as cm:
                self.client.auth.approle.create_or_update_approle(
                    role_name="testrole2",
                    token_policies=["default"],
                    token_type=token_type,
                    mount_point=self.TEST_MOUNT_POINT,
                )
            self.assertIn(member="unsupported token_type", container=str(cm.exception))
        else:
            response = self.client.auth.approle.create_or_update_approle(
                role_name="testrole2",
                token_policies=["default"],
                mount_point=self.TEST_MOUNT_POINT,
            )

            self.assertEqual(first=bool(response), second=True)

    def test_list_roles(self):
        response = self.client.auth.approle.list_roles(mount_point=self.TEST_MOUNT_POINT)

        self.assertEqual(first=len(response["data"]["keys"]), second=1)

    def test_read_role(self):
        response = self.client.auth.approle.read_role(role_name=self.TEST_ROLE_NAME, mount_point=self.TEST_MOUNT_POINT)

        self.assertEqual(first=response["data"]["token_type"], second="default")

    def test_delete_role(self):
        response = self.client.auth.approle.delete_role(
            role_name=self.TEST_ROLE_NAME, mount_point=self.TEST_MOUNT_POINT
        )

        self.assertEqual(first=204, second=response.status)

    def test_read_role_id(self):
        response = self.client.auth.approle.read_role_id(
            role_name=self.TEST_ROLE_NAME, mount_point=self.TEST_MOUNT_POINT
        )

        self.assertEqual(first=self.TEST_ROLE_ID, second=response["data"]["role_id"])

    @parameterized.expand(
        [
            ("good request, no metadata", None, None, None),
            ("good request, good metadata", None, {"a": "val1", "B": "two"}, 300),
            ("good request, good metadata", None, {"a": "val1", "B": "two"}, "5m"),
            ("bad metadata option", exceptions.VaultxError, "bad", None),
        ]
    )
    def test_generate_secret_id(self, test_label, raises, metadata, wrap_ttl):
        if raises is not None:
            with self.assertRaises(raises) as cm:
                self.client.auth.approle.generate_secret_id(
                    role_name=self.TEST_ROLE_NAME,
                    metadata=metadata,
                    mount_point=self.TEST_MOUNT_POINT,
                    wrap_ttl=wrap_ttl,
                )
            self.assertIn(member="unsupported metadata argument", container=str(cm.exception))
        else:
            response = self.client.auth.approle.generate_secret_id(
                role_name=self.TEST_ROLE_NAME,
                cidr_list=["127.0.0.1/32"],
                mount_point=self.TEST_MOUNT_POINT,
                metadata=metadata,
                wrap_ttl=wrap_ttl,
            )
            if wrap_ttl is not None:
                assert "wrap_info" in response
                assert isinstance(response["wrap_info"]["ttl"], int)
                assert response["wrap_info"]["ttl"] == 300  # NOTE: hardcoded for now because of string formats
            else:
                self.assertIn(member="secret_id", container=response["data"], msg=response)

    @parameterized.expand(
        [
            ("good request, no metadata", None, None, None),
            ("good request, good metadata", None, {"a": "val1", "B": "two"}, 300),
            ("good request, good metadata", None, {"a": "val1", "B": "two"}, "5m"),
            ("bad metadata option", exceptions.VaultxError, "bad", None),
        ]
    )
    def test_create_custom_secret_id(self, test_label, raises, metadata, wrap_ttl):
        if raises is not None:
            with self.assertRaises(raises) as cm:
                self.client.auth.approle.create_custom_secret_id(
                    role_name=self.TEST_ROLE_NAME,
                    secret_id=self.TEST_SECRET_ID,
                    cidr_list=["127.0.0.1/32"],
                    metadata=metadata,
                    mount_point=self.TEST_MOUNT_POINT,
                    wrap_ttl=wrap_ttl,
                )
            self.assertIn(member="unsupported metadata argument", container=str(cm.exception))
        else:
            response = self.client.auth.approle.create_custom_secret_id(
                role_name=self.TEST_ROLE_NAME,
                secret_id=self.TEST_SECRET_ID,
                cidr_list=["127.0.0.1/32"],
                mount_point=self.TEST_MOUNT_POINT,
                metadata=metadata,
                wrap_ttl=wrap_ttl,
            )
            if wrap_ttl is not None:
                assert "wrap_info" in response
                assert isinstance(response["wrap_info"]["ttl"], int)
                assert response["wrap_info"]["ttl"] == 300  # NOTE: hardcoded for now because of string formats
            else:
                self.assertEqual(first=self.TEST_SECRET_ID, second=response["data"]["secret_id"])

    def test_read_secret_id(self):
        secret_id_response = self._secret_id()

        response = self.client.auth.approle.read_secret_id(
            role_name=self.TEST_ROLE_NAME,
            secret_id=secret_id_response["secret_id"],
            mount_point=self.TEST_MOUNT_POINT,
        )

        self.assertEqual(first=0, second=response["data"]["secret_id_num_uses"])

    def test_destroy_secret_id(self):
        secret_id_response = self._secret_id()

        response = self.client.auth.approle.destroy_secret_id(
            role_name=self.TEST_ROLE_NAME,
            secret_id=secret_id_response["secret_id"],
            mount_point=self.TEST_MOUNT_POINT,
        )

        self.assertEqual(first=204, second=response.status)

    def test_list_secret_id_accessors(self):
        self._secret_id()

        response = self.client.auth.approle.list_secret_id_accessors(
            role_name=self.TEST_ROLE_NAME, mount_point=self.TEST_MOUNT_POINT
        )

        self.assertEqual(first=1, second=len(response["data"]["keys"]))

    def test_read_secret_id_accessor(self):
        secret_id_response = self._secret_id()

        response = self.client.auth.approle.read_secret_id_accessor(
            role_name=self.TEST_ROLE_NAME,
            secret_id_accessor=secret_id_response["secret_id_accessor"],
            mount_point=self.TEST_MOUNT_POINT,
        )

        self.assertEqual(
            first=secret_id_response["secret_id_accessor"],
            second=response["data"]["secret_id_accessor"],
        )
        self.assertEqual(first="127.0.0.1/32", second=response["data"]["cidr_list"][0])

    def test_destroy_secret_id_accessor(self):
        secret_id_response = self._secret_id()

        response = self.client.auth.approle.read_secret_id_accessor(
            role_name=self.TEST_ROLE_NAME,
            secret_id_accessor=secret_id_response["secret_id_accessor"],
            mount_point=self.TEST_MOUNT_POINT,
        )
        self.assertEqual(
            first=secret_id_response["secret_id_accessor"],
            second=response["data"]["secret_id_accessor"],
        )

        response = self.client.auth.approle.destroy_secret_id_accessor(
            role_name=self.TEST_ROLE_NAME,
            secret_id_accessor=secret_id_response["secret_id_accessor"],
            mount_point=self.TEST_MOUNT_POINT,
        )
        self.assertEqual(first=204, second=response.status)


@skipIf(utils.vault_version_lt("0.6.2"), "AppRole endpoints standardized in version 0.6.2")
class TestAsyncAppRole(AsyncVaultxIntegrationTestCase, IsolatedAsyncioTestCase):
    TEST_MOUNT_POINT = "approle-test"
    TEST_ROLE_NAME = "testrole"
    TEST_ROLE_ID = "test_role_id"
    TEST_SECRET_ID = "custom_secret"

    async def asyncSetUp(self):
        await super().asyncSetUp()
        if "%s/" % self.TEST_MOUNT_POINT not in await self.client.sys.list_auth_methods():
            await self.client.sys.enable_auth_method(
                method_type="approle",
                path=self.TEST_MOUNT_POINT,
            )
        await self.client.auth.approle.create_or_update_approle(
            role_name=self.TEST_ROLE_NAME,
            token_policies=["default"],
            mount_point=self.TEST_MOUNT_POINT,
        )
        await self.client.auth.approle.update_role_id(
            role_name=self.TEST_ROLE_NAME,
            role_id=self.TEST_ROLE_ID,
            mount_point=self.TEST_MOUNT_POINT,
        )

    async def asyncTearDown(self):
        await self.client.sys.disable_auth_method(path=self.TEST_MOUNT_POINT)
        await super().asyncTearDown()

    async def _secret_id(self):
        secret_id_response = await self.client.auth.approle.generate_secret_id(
            role_name=self.TEST_ROLE_NAME,
            cidr_list=["127.0.0.1/32"],
            mount_point=self.TEST_MOUNT_POINT,
        )
        return secret_id_response["data"]

    @parameterized.expand(
        [
            ("create test role", "default", None),
            ("bad token type", "bad_token", exceptions.VaultxError),
        ]
    )
    async def test_create_or_update_approle(self, test_label, token_type, raises):
        if raises is not None:
            with self.assertRaises(raises) as cm:
                await self.client.auth.approle.create_or_update_approle(
                    role_name="testrole2",
                    token_policies=["default"],
                    token_type=token_type,
                    mount_point=self.TEST_MOUNT_POINT,
                )
            self.assertIn(member="unsupported token_type", container=str(cm.exception))
        else:
            response = await self.client.auth.approle.create_or_update_approle(
                role_name="testrole2",
                token_policies=["default"],
                mount_point=self.TEST_MOUNT_POINT,
            )

            self.assertEqual(first=bool(response), second=True)

    async def test_list_roles(self):
        response = await self.client.auth.approle.list_roles(mount_point=self.TEST_MOUNT_POINT)

        self.assertEqual(first=len(response["data"]["keys"]), second=1)

    async def test_read_role(self):
        response = await self.client.auth.approle.read_role(
            role_name=self.TEST_ROLE_NAME, mount_point=self.TEST_MOUNT_POINT
        )

        self.assertEqual(first=response["data"]["token_type"], second="default")

    async def test_delete_role(self):
        response = await self.client.auth.approle.delete_role(
            role_name=self.TEST_ROLE_NAME, mount_point=self.TEST_MOUNT_POINT
        )

        self.assertEqual(first=204, second=response.status)

    async def test_read_role_id(self):
        response = await self.client.auth.approle.read_role_id(
            role_name=self.TEST_ROLE_NAME, mount_point=self.TEST_MOUNT_POINT
        )

        self.assertEqual(first=self.TEST_ROLE_ID, second=response["data"]["role_id"])

    @parameterized.expand(
        [
            ("good request, no metadata", None, None, None),
            ("good request, good metadata", None, {"a": "val1", "B": "two"}, 300),
            ("good request, good metadata", None, {"a": "val1", "B": "two"}, "5m"),
            ("bad metadata option", exceptions.VaultxError, "bad", None),
        ]
    )
    async def test_generate_secret_id(self, test_label, raises, metadata, wrap_ttl):
        if raises is not None:
            with self.assertRaises(raises) as cm:
                await self.client.auth.approle.generate_secret_id(
                    role_name=self.TEST_ROLE_NAME,
                    metadata=metadata,
                    mount_point=self.TEST_MOUNT_POINT,
                    wrap_ttl=wrap_ttl,
                )
            self.assertIn(member="unsupported metadata argument", container=str(cm.exception))
        else:
            response = await self.client.auth.approle.generate_secret_id(
                role_name=self.TEST_ROLE_NAME,
                cidr_list=["127.0.0.1/32"],
                mount_point=self.TEST_MOUNT_POINT,
                metadata=metadata,
                wrap_ttl=wrap_ttl,
            )
            if wrap_ttl is not None:
                assert "wrap_info" in response
                assert isinstance(response["wrap_info"]["ttl"], int)
                assert response["wrap_info"]["ttl"] == 300  # NOTE: hardcoded for now because of string formats
            else:
                self.assertIn(member="secret_id", container=response["data"], msg=response)

    @parameterized.expand(
        [
            ("good request, no metadata", None, None, None),
            ("good request, good metadata", None, {"a": "val1", "B": "two"}, 300),
            ("good request, good metadata", None, {"a": "val1", "B": "two"}, "5m"),
            ("bad metadata option", exceptions.VaultxError, "bad", None),
        ]
    )
    async def test_create_custom_secret_id(self, test_label, raises, metadata, wrap_ttl):
        if raises is not None:
            with self.assertRaises(raises) as cm:
                await self.client.auth.approle.create_custom_secret_id(
                    role_name=self.TEST_ROLE_NAME,
                    secret_id=self.TEST_SECRET_ID,
                    cidr_list=["127.0.0.1/32"],
                    metadata=metadata,
                    mount_point=self.TEST_MOUNT_POINT,
                    wrap_ttl=wrap_ttl,
                )
            self.assertIn(member="unsupported metadata argument", container=str(cm.exception))
        else:
            response = await self.client.auth.approle.create_custom_secret_id(
                role_name=self.TEST_ROLE_NAME,
                secret_id=self.TEST_SECRET_ID,
                cidr_list=["127.0.0.1/32"],
                mount_point=self.TEST_MOUNT_POINT,
                metadata=metadata,
                wrap_ttl=wrap_ttl,
            )
            if wrap_ttl is not None:
                assert "wrap_info" in response
                assert isinstance(response["wrap_info"]["ttl"], int)
                assert response["wrap_info"]["ttl"] == 300  # NOTE: hardcoded for now because of string formats
            else:
                self.assertEqual(first=self.TEST_SECRET_ID, second=response["data"]["secret_id"])

    async def test_read_secret_id(self):
        secret_id_response = await self._secret_id()

        response = await self.client.auth.approle.read_secret_id(
            role_name=self.TEST_ROLE_NAME,
            secret_id=secret_id_response["secret_id"],
            mount_point=self.TEST_MOUNT_POINT,
        )

        self.assertEqual(first=0, second=response["data"]["secret_id_num_uses"])

    async def test_destroy_secret_id(self):
        secret_id_response = await self._secret_id()

        response = await self.client.auth.approle.destroy_secret_id(
            role_name=self.TEST_ROLE_NAME,
            secret_id=secret_id_response["secret_id"],
            mount_point=self.TEST_MOUNT_POINT,
        )

        self.assertEqual(first=204, second=response.status)

    async def test_list_secret_id_accessors(self):
        await self._secret_id()

        response = await self.client.auth.approle.list_secret_id_accessors(
            role_name=self.TEST_ROLE_NAME, mount_point=self.TEST_MOUNT_POINT
        )

        self.assertEqual(first=1, second=len(response["data"]["keys"]))

    async def test_read_secret_id_accessor(self):
        secret_id_response = await self._secret_id()

        response = await self.client.auth.approle.read_secret_id_accessor(
            role_name=self.TEST_ROLE_NAME,
            secret_id_accessor=secret_id_response["secret_id_accessor"],
            mount_point=self.TEST_MOUNT_POINT,
        )

        self.assertEqual(
            first=secret_id_response["secret_id_accessor"],
            second=response["data"]["secret_id_accessor"],
        )
        self.assertEqual(first="127.0.0.1/32", second=response["data"]["cidr_list"][0])

    async def test_destroy_secret_id_accessor(self):
        secret_id_response = await self._secret_id()

        response = await self.client.auth.approle.read_secret_id_accessor(
            role_name=self.TEST_ROLE_NAME,
            secret_id_accessor=secret_id_response["secret_id_accessor"],
            mount_point=self.TEST_MOUNT_POINT,
        )
        self.assertEqual(
            first=secret_id_response["secret_id_accessor"],
            second=response["data"]["secret_id_accessor"],
        )

        response = await self.client.auth.approle.destroy_secret_id_accessor(
            role_name=self.TEST_ROLE_NAME,
            secret_id_accessor=secret_id_response["secret_id_accessor"],
            mount_point=self.TEST_MOUNT_POINT,
        )
        self.assertEqual(first=204, second=response.status)
