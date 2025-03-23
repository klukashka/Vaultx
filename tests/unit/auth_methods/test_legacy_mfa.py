import unittest
from unittest import mock

from httpx import Response

from vaultx import exceptions
from vaultx.adapters import VaultxResponse
from vaultx.api.async_auth_methods.legacy_mfa import LegacyMfa as AsyncLegacyMfa
from vaultx.api.auth_methods.legacy_mfa import LegacyMfa


class TestLegacyMfa(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.legacy_mfa = LegacyMfa(self.mock_adapter)
        self.mount_point = "test_mount"

    def test_configure(self):
        # Test successful configuration with default MFA type
        self.mock_adapter.post.return_value = Response(204)
        result = self.legacy_mfa.configure(mount_point=self.mount_point)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/auth/{self.mount_point}/mfa_config",
            json={"type": "duo"},
        )

        # Test with force=True and unsupported MFA type
        self.mock_adapter.post.return_value = Response(204)
        result = self.legacy_mfa.configure(mount_point=self.mount_point, mfa_type="unsupported", force=True)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url=f"/v1/auth/{self.mount_point}/mfa_config",
            json={"type": "unsupported"},
        )

        # Test with unsupported MFA type and force=False (should raise an error)
        with self.assertRaises(exceptions.VaultxError) as context:
            self.legacy_mfa.configure(mount_point=self.mount_point, mfa_type="unsupported", force=False)
        self.assertIn('Unsupported mfa_type argument provided "unsupported"', str(context.exception))

    def test_read_configuration(self):
        # Test successful read configuration
        mock_response = Response(200, json={"data": {"type": "duo"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.legacy_mfa.read_configuration(mount_point=self.mount_point)
        self.assertEqual(result.value, {"data": {"type": "duo"}})
        self.mock_adapter.get.assert_called_once_with(url=f"/v1/auth/{self.mount_point}/mfa_config")

    def test_configure_duo_access(self):
        # Test successful Duo access configuration
        self.mock_adapter.post.return_value = Response(204)
        result = self.legacy_mfa.configure_duo_access(
            mount_point=self.mount_point,
            host="api-1234.duosecurity.com",
            integration_key="test_ikey",
            secret_key="test_skey",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/auth/{self.mount_point}/duo/access",
            json={
                "host": "api-1234.duosecurity.com",
                "ikey": "test_ikey",
                "skey": "test_skey",
            },
        )

    def test_configure_duo_behavior(self):
        # Test successful Duo behavior configuration with all parameters
        self.mock_adapter.post.return_value = Response(204)
        result = self.legacy_mfa.configure_duo_behavior(
            mount_point=self.mount_point,
            push_info="key1=value1&key2=value2",
            user_agent="test_user_agent",
            username_format="%s",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/auth/{self.mount_point}/duo/config",
            json={
                "push_info": "key1=value1&key2=value2",
                "user_agent": "test_user_agent",
                "username_format": "%s",
            },
        )

        # Test with only required parameters
        self.mock_adapter.post.return_value = Response(204)
        result = self.legacy_mfa.configure_duo_behavior(
            mount_point=self.mount_point,
            username_format="%s",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url=f"/v1/auth/{self.mount_point}/duo/config",
            json={"username_format": "%s"},
        )

    def test_read_duo_behavior_configuration(self):
        # Test successful read of Duo behavior configuration
        mock_response = Response(200, json={"data": {"username_format": "%s"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = self.legacy_mfa.read_duo_behavior_configuration(mount_point=self.mount_point)
        self.assertEqual(result.value, {"data": {"username_format": "%s"}})
        self.mock_adapter.get.assert_called_once_with(url=f"/v1/auth/{self.mount_point}/duo/config")


class TestAsyncLegacyMfa(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.legacy_mfa = AsyncLegacyMfa(self.mock_adapter)
        self.mount_point = "test_mount"

    async def test_configure(self):
        # Test successful configuration with default MFA type
        self.mock_adapter.post.return_value = Response(204)
        result = await self.legacy_mfa.configure(mount_point=self.mount_point)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/auth/{self.mount_point}/mfa_config",
            json={"type": "duo"},
        )

        # Test with force=True and unsupported MFA type
        self.mock_adapter.post.return_value = Response(204)
        result = await self.legacy_mfa.configure(mount_point=self.mount_point, mfa_type="unsupported", force=True)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url=f"/v1/auth/{self.mount_point}/mfa_config",
            json={"type": "unsupported"},
        )

        # Test with unsupported MFA type and force=False (should raise an error)
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.legacy_mfa.configure(mount_point=self.mount_point, mfa_type="unsupported", force=False)
        self.assertIn('Unsupported mfa_type argument provided "unsupported"', str(context.exception))

    async def test_read_configuration(self):
        # Test successful read configuration
        mock_response = Response(200, json={"data": {"type": "duo"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.legacy_mfa.read_configuration(mount_point=self.mount_point)
        self.assertEqual(result.value, {"data": {"type": "duo"}})
        self.mock_adapter.get.assert_called_once_with(url=f"/v1/auth/{self.mount_point}/mfa_config")

    async def test_configure_duo_access(self):
        # Test successful Duo access configuration
        self.mock_adapter.post.return_value = Response(204)
        result = await self.legacy_mfa.configure_duo_access(
            mount_point=self.mount_point,
            host="api-1234.duosecurity.com",
            integration_key="test_ikey",
            secret_key="test_skey",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/auth/{self.mount_point}/duo/access",
            json={
                "host": "api-1234.duosecurity.com",
                "ikey": "test_ikey",
                "skey": "test_skey",
            },
        )

    async def test_configure_duo_behavior(self):
        # Test successful Duo behavior configuration with all parameters
        self.mock_adapter.post.return_value = Response(204)
        result = await self.legacy_mfa.configure_duo_behavior(
            mount_point=self.mount_point,
            push_info="key1=value1&key2=value2",
            user_agent="test_user_agent",
            username_format="%s",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/auth/{self.mount_point}/duo/config",
            json={
                "push_info": "key1=value1&key2=value2",
                "user_agent": "test_user_agent",
                "username_format": "%s",
            },
        )

        # Test with only required parameters
        self.mock_adapter.post.return_value = Response(204)
        result = await self.legacy_mfa.configure_duo_behavior(
            mount_point=self.mount_point,
            username_format="%s",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url=f"/v1/auth/{self.mount_point}/duo/config",
            json={"username_format": "%s"},
        )

    async def test_read_duo_behavior_configuration(self):
        # Test successful read of Duo behavior configuration
        mock_response = Response(200, json={"data": {"username_format": "%s"}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)
        result = await self.legacy_mfa.read_duo_behavior_configuration(mount_point=self.mount_point)
        self.assertEqual(result.value, {"data": {"username_format": "%s"}})
        self.mock_adapter.get.assert_called_once_with(url=f"/v1/auth/{self.mount_point}/duo/config")
