import unittest
from unittest import mock

from httpx import Response

from vaultx.adapters import VaultxResponse
from vaultx.api.async_system_backend.audit import Audit as AsyncAudit
from vaultx.api.system_backend.audit import Audit


class TestAudit(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.audit = Audit(self.mock_adapter)

    def test_list_enabled_audit_devices_returns_response(self):
        mock_response = Response(200, json={"data": {"file/": {"type": "file"}}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)

        result = self.audit.list_enabled_audit_devices()

        self.assertEqual(result.status, 200)
        self.assertEqual(result.value, {"data": {"file/": {"type": "file"}}})
        self.mock_adapter.get.assert_called_once_with("/v1/sys/audit")

    def test_enable_audit_device_with_all_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = VaultxResponse(mock_response)

        result = self.audit.enable_audit_device(
            device_type="file",
            description="File audit device",
            options="option1",
            path="file-audit",
            local=True,
        )
        self.assertEqual(result.status, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/audit/file-audit",
            json={
                "type": "file",
                "description": "File audit device",
                "options": "option1",
                "local": True,
            },
        )

    def test_enable_audit_device_with_minimal_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.audit.enable_audit_device(device_type="file")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/audit/file",
            json={"type": "file"},
        )

    def test_disable_audit_device_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = VaultxResponse(mock_response)

        result = self.audit.disable_audit_device(path="file-audit")
        self.assertEqual(result.status, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/audit/file-audit",
        )

    def test_calculate_hash_returns_response(self):
        mock_response = Response(200, json={"hash": "abc123"})
        self.mock_adapter.post.return_value = VaultxResponse(mock_response)

        result = self.audit.calculate_hash(path="file-audit", input_to_hash="test-input")
        self.assertEqual(result.status, 200)
        self.assertEqual(result.value, {"hash": "abc123"})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/audit-hash/file-audit",
            json={"input": "test-input"},
        )


class TestAsyncAudit(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.audit = AsyncAudit(self.mock_adapter)

    async def test_list_enabled_audit_devices_returns_response(self):
        mock_response = Response(200, json={"data": {"file/": {"type": "file"}}})
        self.mock_adapter.get.return_value = VaultxResponse(mock_response)

        result = await self.audit.list_enabled_audit_devices()

        self.assertEqual(result.status, 200)
        self.assertEqual(result.value, {"data": {"file/": {"type": "file"}}})
        self.mock_adapter.get.assert_called_once_with("/v1/sys/audit")

    async def test_enable_audit_device_with_all_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = VaultxResponse(mock_response)

        result = await self.audit.enable_audit_device(
            device_type="file",
            description="File audit device",
            options="option1",
            path="file-audit",
            local=True,
        )
        self.assertEqual(result.status, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/audit/file-audit",
            json={
                "type": "file",
                "description": "File audit device",
                "options": "option1",
                "local": True,
            },
        )

    async def test_enable_audit_device_with_minimal_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.audit.enable_audit_device(device_type="file")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/audit/file",
            json={"type": "file"},
        )

    async def test_disable_audit_device_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = VaultxResponse(mock_response)

        result = await self.audit.disable_audit_device(path="file-audit")
        self.assertEqual(result.status, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/audit/file-audit",
        )

    async def test_calculate_hash_returns_response(self):
        mock_response = Response(200, json={"hash": "abc123"})
        self.mock_adapter.post.return_value = VaultxResponse(mock_response)

        result = await self.audit.calculate_hash(path="file-audit", input_to_hash="test-input")
        self.assertEqual(result.status, 200)
        self.assertEqual(result.value, {"hash": "abc123"})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/audit-hash/file-audit",
            json={"input": "test-input"},
        )
