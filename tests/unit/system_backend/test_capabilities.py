import unittest
from unittest import IsolatedAsyncioTestCase, mock

from vaultx.api.async_system_backend.capabilities import Capabilities as AsyncCapabilities
from vaultx.api.system_backend.capabilities import Capabilities


class TestCapabilities(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.capabilities = Capabilities(self.mock_adapter)

    def test_get_capabilities_with_token(self):
        # Test getting capabilities with a token
        self.mock_adapter.post.return_value = {"data": {"capabilities": ["read"]}}
        result = self.capabilities.get_capabilities(
            paths=["secret/data/test"],
            token="test_token",
        )
        self.assertEqual(result, {"data": {"capabilities": ["read"]}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/capabilities",
            json={"paths": ["secret/data/test"], "token": "test_token"},
        )

    def test_get_capabilities_with_accessor(self):
        self.mock_adapter.post.return_value = {"data": {"capabilities": ["read"]}}
        result = self.capabilities.get_capabilities(
            paths=["secret/data/test"],
            accessor="test_accessor",
        )
        self.assertEqual(result, {"data": {"capabilities": ["read"]}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/capabilities-accessor",
            json={"paths": ["secret/data/test"], "accessor": "test_accessor"},
        )

    def test_get_capabilities_self(self):
        self.mock_adapter.post.return_value = {"data": {"capabilities": ["read"]}}
        result = self.capabilities.get_capabilities(
            paths=["secret/data/test"],
        )
        self.assertEqual(result, {"data": {"capabilities": ["read"]}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/capabilities-self",
            json={"paths": ["secret/data/test"]},
        )

    def test_get_capabilities_with_token_and_accessor(self):
        with self.assertRaises(ValueError) as context:
            self.capabilities.get_capabilities(
                paths=["secret/data/test"],
                token="test_token",
                accessor="test_accessor",
            )
        self.assertEqual(
            str(context.exception),
            "You can specify either token or accessor, not both.",
        )


class TestAsyncCapabilities(IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.capabilities = AsyncCapabilities(self.mock_adapter)

    async def test_get_capabilities_with_token(self):
        self.mock_adapter.post.return_value = {"data": {"capabilities": ["read"]}}
        result = await self.capabilities.get_capabilities(
            paths=["secret/data/test"],
            token="test_token",
        )
        self.assertEqual(result, {"data": {"capabilities": ["read"]}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/capabilities",
            json={"paths": ["secret/data/test"], "token": "test_token"},
        )

    async def test_get_capabilities_with_accessor(self):
        self.mock_adapter.post.return_value = {"data": {"capabilities": ["read"]}}
        result = await self.capabilities.get_capabilities(
            paths=["secret/data/test"],
            accessor="test_accessor",
        )
        self.assertEqual(result, {"data": {"capabilities": ["read"]}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/capabilities-accessor",
            json={"paths": ["secret/data/test"], "accessor": "test_accessor"},
        )

    async def test_get_capabilities_self(self):
        self.mock_adapter.post.return_value = {"data": {"capabilities": ["read"]}}
        result = await self.capabilities.get_capabilities(
            paths=["secret/data/test"],
        )
        self.assertEqual(result, {"data": {"capabilities": ["read"]}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/capabilities-self",
            json={"paths": ["secret/data/test"]},
        )

    async def test_get_capabilities_with_token_and_accessor(self):
        with self.assertRaises(ValueError) as context:
            await self.capabilities.get_capabilities(
                paths=["secret/data/test"],
                token="test_token",
                accessor="test_accessor",
            )
        self.assertEqual(
            str(context.exception),
            "You can specify either token or accessor, not both.",
        )
