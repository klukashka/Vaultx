import unittest
from unittest import mock

from httpx import Response

from vaultx.api.system_backend.leader import Leader


class TestLeader(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.leader = Leader(self.mock_adapter)

    def test_read_leader_status_returns_response(self):
        mock_response = Response(200, json={"ha_enabled": True, "is_self": True})
        self.mock_adapter.get.return_value = mock_response

        result = self.leader.read_leader_status()

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"ha_enabled": True, "is_self": True})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/leader",
        )

    def test_step_down_returns_response(self):
        mock_response = Response(200, json={"message": "Successfully stepped down"})
        self.mock_adapter.put.return_value = mock_response

        result = self.leader.step_down()

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"message": "Successfully stepped down"})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/step-down",
        )
