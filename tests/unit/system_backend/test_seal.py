import unittest
from unittest import mock

from httpx import Response

from vaultx.adapters import VaultxResponse
from vaultx.api.async_system_backend.seal import Seal as AsyncSeal
from vaultx.api.system_backend.seal import Seal


class TestSeal(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.seal = Seal(self.mock_adapter)

    def test_is_sealed_true(self):
        self.mock_adapter.get.return_value = {"sealed": True}
        result = self.seal.is_sealed()
        self.assertTrue(result)
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/seal-status")

    def test_is_sealed_false(self):
        self.mock_adapter.get.return_value = {"sealed": False}
        result = self.seal.is_sealed()
        self.assertFalse(result)
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/seal-status")

    def test_read_seal_status(self):
        self.mock_adapter.get.return_value = {"sealed": True}
        result = self.seal.read_seal_status()
        self.assertEqual(result, {"sealed": True})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/seal-status")

    def test_seal(self):
        self.mock_adapter.put.return_value = Response(204)
        result = self.seal.seal()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(url="/v1/sys/seal")

    def test_submit_unseal_key(self):
        self.mock_adapter.put.return_value = VaultxResponse(Response(200, json={"sealed": True}))
        result = self.seal.submit_unseal_key(key="test_key")
        self.assertEqual(result.value, {"sealed": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/unseal",
            json={"key": "test_key", "migrate": False},
        )

    def test_submit_unseal_key_reset(self):
        self.mock_adapter.put.return_value = {"sealed": True}
        result = self.seal.submit_unseal_key(reset=True)
        self.assertEqual(result, {"sealed": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/unseal",
            json={"reset": True, "migrate": False},
        )

    def test_submit_unseal_keys(self):
        self.mock_adapter.put.side_effect = [
            {"sealed": True},
            {"sealed": False},
        ]
        result = self.seal.submit_unseal_keys(keys=["key1", "key2"])
        self.assertEqual(result, {"sealed": False})
        self.assertEqual(self.mock_adapter.put.call_count, 2)

    def test_submit_unseal_keys_no_unseal(self):
        self.mock_adapter.put.return_value = VaultxResponse(Response(200, json={"sealed": True}))
        result = self.seal.submit_unseal_keys(keys=["key1", "key2"])
        self.assertEqual(result.value, {"sealed": True})
        self.assertEqual(self.mock_adapter.put.call_count, 2)


class TestAsyncSeal(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.seal = AsyncSeal(self.mock_adapter)

    async def test_is_sealed_true(self):
        self.mock_adapter.get.return_value = {"sealed": True}
        result = await self.seal.is_sealed()
        self.assertTrue(result)
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/seal-status")

    async def test_is_sealed_false(self):
        self.mock_adapter.get.return_value = {"sealed": False}
        result = await self.seal.is_sealed()
        self.assertFalse(result)
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/seal-status")

    async def test_read_seal_status(self):
        self.mock_adapter.get.return_value = {"sealed": True}
        result = await self.seal.read_seal_status()
        self.assertEqual(result, {"sealed": True})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/seal-status")

    async def test_seal(self):
        self.mock_adapter.put.return_value = Response(204)
        result = await self.seal.seal()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(url="/v1/sys/seal")

    async def test_submit_unseal_key(self):
        self.mock_adapter.put.return_value = VaultxResponse(Response(200, json={"sealed": True}))
        result = await self.seal.submit_unseal_key(key="test_key")
        self.assertEqual(result.value, {"sealed": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/unseal",
            json={"key": "test_key", "migrate": False},
        )

    async def test_submit_unseal_key_reset(self):
        self.mock_adapter.put.return_value = {"sealed": True}
        result = await self.seal.submit_unseal_key(reset=True)
        self.assertEqual(result, {"sealed": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/unseal",
            json={"reset": True, "migrate": False},
        )

    async def test_submit_unseal_keys(self):
        self.mock_adapter.put.side_effect = [
            {"sealed": True},
            {"sealed": False},
        ]
        result = await self.seal.submit_unseal_keys(keys=["key1", "key2"])
        self.assertEqual(result, {"sealed": False})
        self.assertEqual(self.mock_adapter.put.call_count, 2)

    async def test_submit_unseal_keys_no_unseal(self):
        self.mock_adapter.put.return_value = VaultxResponse(Response(200, json={"sealed": True}))
        result = await self.seal.submit_unseal_keys(keys=["key1", "key2"])
        self.assertEqual(result.value, {"sealed": True})
        self.assertEqual(self.mock_adapter.put.call_count, 2)
