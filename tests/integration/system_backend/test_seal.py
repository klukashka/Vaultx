from unittest import IsolatedAsyncioTestCase, TestCase

from tests.utils.vaultx_integration_test_case import AsyncVaultxIntegrationTestCase, VaultxIntegrationTestCase


class TestSeal(VaultxIntegrationTestCase, TestCase):
    def test_unseal_multi(self):
        cls = type(self)

        self.client.sys.seal()

        keys = cls.manager.keys

        result = self.client.sys.submit_unseal_keys(keys[0:2])

        self.assertTrue(result["sealed"])  # type: ignore
        self.assertEqual(result["progress"], 2)  # type: ignore

        result = self.client.sys.submit_unseal_key(reset=True)
        self.assertEqual(result["progress"], 0)
        result = self.client.sys.submit_unseal_keys(keys[1:3])
        self.assertTrue(result["sealed"])  # type: ignore
        self.assertEqual(result["progress"], 2)  # type: ignore
        self.client.sys.submit_unseal_keys(keys[0:1])
        result = self.client.sys.submit_unseal_keys(keys[2:3])
        self.assertFalse(result["sealed"])  # type: ignore

    def test_seal_unseal(self):
        cls = type(self)

        self.assertFalse(self.client.sys.is_sealed())

        self.client.sys.seal()

        self.assertTrue(self.client.sys.is_sealed())

        cls.manager.unseal()

        self.assertFalse(self.client.sys.is_sealed())


class TestAsyncSeal(AsyncVaultxIntegrationTestCase, IsolatedAsyncioTestCase):
    async def test_unseal_multi(self):
        cls = type(self)

        await self.client.sys.seal()

        keys = cls.manager.keys

        result = await self.client.sys.submit_unseal_keys(keys[0:2])

        self.assertTrue(result["sealed"])  # type: ignore
        self.assertEqual(result["progress"], 2)  # type: ignore

        result = await self.client.sys.submit_unseal_key(reset=True)
        self.assertEqual(result["progress"], 0)
        result = await self.client.sys.submit_unseal_keys(keys[1:3])
        self.assertTrue(result["sealed"])  # type: ignore
        self.assertEqual(result["progress"], 2)  # type: ignore
        await self.client.sys.submit_unseal_keys(keys[0:1])
        result = await self.client.sys.submit_unseal_keys(keys[2:3])
        self.assertFalse(result["sealed"])  # type: ignore

    async def test_seal_unseal(self):
        cls = type(self)

        self.assertFalse(await self.client.sys.is_sealed())

        await self.client.sys.seal()

        self.assertTrue(await self.client.sys.is_sealed())

        cls.manager.unseal()

        self.assertFalse(await self.client.sys.is_sealed())
