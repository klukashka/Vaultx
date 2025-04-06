import logging
from unittest import IsolatedAsyncioTestCase, TestCase

from parameterized import param, parameterized  # type: ignore

from tests.utils.vaultx_integration_test_case import AsyncVaultxIntegrationTestCase, VaultxIntegrationTestCase
from vaultx import exceptions


class TestApprole(VaultxIntegrationTestCase, TestCase):
    TEST_MOUNT_POINT = "approle"

    def setUp(self):
        super().setUp()
        self.client.sys.enable_auth_method(
            method_type="approle",
            path=self.TEST_MOUNT_POINT,
        )

    def tearDown(self):
        self.client.token = self.manager.root_token
        self.client.sys.disable_auth_method(path=self.TEST_MOUNT_POINT)
        super().tearDown()

    @parameterized.expand(
        [
            param(
                "no secret ids",
                num_secrets_to_create=0,
                raises=exceptions.VaultxError,
            ),
            param(
                "one secret id",
                num_secrets_to_create=1,
            ),
            param(
                "two secret ids",
                num_secrets_to_create=2,
            ),
        ]
    )
    def test_list_role_secrets(self, label, num_secrets_to_create=0, raises=None):
        test_role_name = "testrole"
        self.client.auth.approle.create_or_update_approle(
            role_name=test_role_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        for _ in range(num_secrets_to_create):
            self.client.auth.approle.generate_secret_id(
                role_name=test_role_name,
                mount_point=self.TEST_MOUNT_POINT,
            )

        if raises is not None:
            with self.assertRaises(raises):
                self.client.auth.approle.list_secret_id_accessors(
                    role_name=test_role_name,
                    mount_point=self.TEST_MOUNT_POINT,
                )
        else:
            list_role_secrets_response = self.client.auth.approle.list_secret_id_accessors(
                role_name=test_role_name,
                mount_point=self.TEST_MOUNT_POINT,
            )
            logging.debug("list_role_secrets_response: %s" % list_role_secrets_response)
            self.assertEqual(
                first=num_secrets_to_create,
                second=len(list_role_secrets_response["data"]["keys"]),
            )

    def test_create_role(self):
        self.client.auth.approle.create_or_update_approle("testrole")

        result = self.client.read("auth/approle/role/testrole")
        lib_result = self.client.auth.approle.read_role("testrole")
        if result is not None:
            result_dict = result.value
            lib_result_dict = lib_result.value
            del result_dict["request_id"]
            del lib_result_dict["request_id"]

            self.assertEqual(result_dict, lib_result_dict)

    def test_delete_role(self):
        test_role_name = "test-role"

        self.client.auth.approle.create_or_update_approle(test_role_name)
        # We add a second dummy test role so we can still hit the /role?list=true route after deleting the first role
        self.client.auth.approle.create_or_update_approle("test-role-2")

        # Ensure our created role shows up when calling list_roles as expected
        result = self.client.auth.approle.list_roles()
        actual_list_role_keys = result["data"]["keys"]
        self.assertIn(
            member=test_role_name,
            container=actual_list_role_keys,
        )

        # Now delete the role and verify its absence when calling list_roles
        self.client.auth.approle.delete_role(test_role_name)
        result = self.client.auth.approle.list_roles()
        actual_list_role_keys = result["data"]["keys"]
        self.assertNotIn(
            member=test_role_name,
            container=actual_list_role_keys,
        )

    def test_create_delete_role_secret_id(self):
        self.client.auth.approle.create_or_update_approle("testrole")
        create_result = self.client.auth.approle.generate_secret_id("testrole", {"foo": "bar"})
        secret_id = create_result["data"]["secret_id"]
        result = self.client.auth.approle.read_secret_id("testrole", secret_id)
        self.assertEqual(result["data"]["metadata"]["foo"], "bar")
        self.client.auth.approle.destroy_secret_id("testrole", secret_id)
        missing_secret_response = self.client.auth.approle.read_secret_id("testrole", secret_id)
        self.assertEqual(
            first=missing_secret_response.status,
            second=204,
        )

    def test_auth_approle(self):
        self.client.auth.approle.create_or_update_approle("testrole")
        create_result = self.client.auth.approle.generate_secret_id("testrole", {"foo": "bar"})
        secret_id = create_result["data"]["secret_id"]
        role_id = self.client.auth.approle.read_role_id("testrole")["data"]["role_id"]
        logging.debug("role_id: %s" % role_id)
        result = self.client.auth.approle.login(role_id, secret_id)
        self.assertEqual(result["auth"]["metadata"]["foo"], "bar")
        self.assertEqual(self.client.token, result["auth"]["client_token"])
        self.assertTrue(self.client.is_authenticated())

    def test_auth_approle_dont_use_token(self):
        self.client.auth.approle.create_or_update_approle("testrole")
        create_result = self.client.auth.approle.generate_secret_id("testrole", {"foo": "bar"})
        secret_id = create_result["data"]["secret_id"]
        role_id = self.client.auth.approle.read_role_id("testrole")["data"]["role_id"]
        result = self.client.auth.approle.login(role_id, secret_id, use_token=False)
        self.assertEqual(result["auth"]["metadata"]["foo"], "bar")
        self.assertNotEqual(self.client.token, result["auth"]["client_token"])


class TestAsyncApprole(AsyncVaultxIntegrationTestCase, IsolatedAsyncioTestCase):
    TEST_MOUNT_POINT = "approle"

    async def asyncSetUp(self):
        await super().asyncSetUp()
        await self.client.sys.enable_auth_method(
            method_type="approle",
            path=self.TEST_MOUNT_POINT,
        )

    async def asyncTearDown(self):
        self.client.token = self.manager.root_token
        await self.client.sys.disable_auth_method(path=self.TEST_MOUNT_POINT)
        await super().asyncTearDown()

    @parameterized.expand(
        [
            param(
                "no secret ids",
                num_secrets_to_create=0,
                raises=exceptions.HTTPError,
            ),
            param(
                "one secret id",
                num_secrets_to_create=1,
            ),
            param(
                "two secret ids",
                num_secrets_to_create=2,
            ),
        ]
    )
    async def test_list_role_secrets(self, label, num_secrets_to_create=0, raises=None):
        test_role_name = "testrole"
        await self.client.auth.approle.create_or_update_approle(
            role_name=test_role_name,
            mount_point=self.TEST_MOUNT_POINT,
        )
        for _ in range(num_secrets_to_create):
            await self.client.auth.approle.generate_secret_id(
                role_name=test_role_name,
                mount_point=self.TEST_MOUNT_POINT,
            )

        if raises is not None:
            with self.assertRaises(raises):
                await self.client.auth.approle.list_secret_id_accessors(
                    role_name=test_role_name,
                    mount_point=self.TEST_MOUNT_POINT,
                )
        else:
            list_role_secrets_response = await self.client.auth.approle.list_secret_id_accessors(
                role_name=test_role_name,
                mount_point=self.TEST_MOUNT_POINT,
            )
            logging.debug("list_role_secrets_response: %s" % list_role_secrets_response)
            self.assertEqual(
                first=num_secrets_to_create,
                second=len(list_role_secrets_response["data"]["keys"]),
            )

    async def test_create_role(self):
        await self.client.auth.approle.create_or_update_approle("testrole")

        result = await self.client.read("auth/approle/role/testrole")
        lib_result = await self.client.auth.approle.read_role("testrole")
        if result is not None:
            result_dict = result.value
            lib_result_dict = lib_result.value
            del result_dict["request_id"]
            del lib_result_dict["request_id"]

            self.assertEqual(result_dict, lib_result_dict)

    async def test_delete_role(self):
        test_role_name = "test-role"

        await self.client.auth.approle.create_or_update_approle(test_role_name)
        # We add a second dummy test role so we can still hit the /role?list=true route after deleting the first role
        await self.client.auth.approle.create_or_update_approle("test-role-2")

        # Ensure our created role shows up when calling list_roles as expected
        result = await self.client.auth.approle.list_roles()
        actual_list_role_keys = result["data"]["keys"]
        self.assertIn(
            member=test_role_name,
            container=actual_list_role_keys,
        )

        # Now delete the role and verify its absence when calling list_roles
        await self.client.auth.approle.delete_role(test_role_name)
        result = await self.client.auth.approle.list_roles()
        actual_list_role_keys = result["data"]["keys"]
        self.assertNotIn(
            member=test_role_name,
            container=actual_list_role_keys,
        )

    async def test_create_delete_role_secret_id(self):
        await self.client.auth.approle.create_or_update_approle("testrole")
        create_result = await self.client.auth.approle.generate_secret_id("testrole", {"foo": "bar"})
        secret_id = create_result["data"]["secret_id"]
        result = await self.client.auth.approle.read_secret_id("testrole", secret_id)
        self.assertEqual(result["data"]["metadata"]["foo"], "bar")
        await self.client.auth.approle.destroy_secret_id("testrole", secret_id)
        missing_secret_response = await self.client.auth.approle.read_secret_id("testrole", secret_id)
        self.assertEqual(
            first=missing_secret_response.status,
            second=204,
        )

    async def test_auth_approle(self):
        await self.client.auth.approle.create_or_update_approle("testrole")
        create_result = await self.client.auth.approle.generate_secret_id("testrole", {"foo": "bar"})
        secret_id = create_result["data"]["secret_id"]
        role_id = (await self.client.auth.approle.read_role_id("testrole"))["data"]["role_id"]
        logging.debug("role_id: %s" % role_id)
        result = await self.client.auth.approle.login(role_id, secret_id)
        self.assertEqual(result["auth"]["metadata"]["foo"], "bar")
        self.assertEqual(self.client.token, result["auth"]["client_token"])
        self.assertTrue(await self.client.is_authenticated())

    async def test_auth_approle_dont_use_token(self):
        await self.client.auth.approle.create_or_update_approle("testrole")
        create_result = await self.client.auth.approle.generate_secret_id("testrole", {"foo": "bar"})
        secret_id = create_result["data"]["secret_id"]
        role_id = (await self.client.auth.approle.read_role_id("testrole"))["data"]["role_id"]
        result = await self.client.auth.approle.login(role_id, secret_id, use_token=False)
        self.assertEqual(result["auth"]["metadata"]["foo"], "bar")
        self.assertNotEqual(self.client.token, result["auth"]["client_token"])
