import unittest
from unittest import mock

from httpx import Response

from vaultx.api.system_backend.audit import Audit


class TestAudit(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.audit = Audit(self.mock_adapter)

    def test_list_enabled_audit_devices_returns_response(self):
        mock_response = Response(200, json={"data": {"file/": {"type": "file"}}})
        self.mock_adapter.get.return_value = mock_response

        result = self.audit.list_enabled_audit_devices()

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"file/": {"type": "file"}}})
        self.mock_adapter.get.assert_called_once_with("/v1/sys/audit")

    def test_enable_audit_device_with_all_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.audit.enable_audit_device(
            device_type="file",
            description="File audit device",
            options="option1",
            path="file-audit",
            local=True,
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
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
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/audit/file",
            json={"type": "file"},
        )

    def test_disable_audit_device_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.audit.disable_audit_device(path="file-audit")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/audit/file-audit",
        )

    def test_calculate_hash_returns_response(self):
        mock_response = Response(200, json={"hash": "abc123"})
        self.mock_adapter.post.return_value = mock_response

        result = self.audit.calculate_hash(path="file-audit", input_to_hash="test-input")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"hash": "abc123"})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/audit-hash/file-audit",
            json={"input": "test-input"},
        )
