import unittest
from unittest import mock

from httpx import Response

from vaultx.api.system_backend.policy import Policy


class TestPolicy(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.policy = Policy(self.mock_adapter)

    def test_list_policies_returns_response(self):
        mock_response = Response(200, json={"data": {"policies": ["default", "admin"]}})
        self.mock_adapter.get.return_value = mock_response

        result = self.policy.list_policies()

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"policies": ["default", "admin"]}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/policy",
        )

    def test_read_policy_returns_response(self):
        mock_response = Response(
            200, json={"data": {"name": "admin", "rules": "path '/*' { capabilities = ['create', 'read'] }"}}
        )
        self.mock_adapter.get.return_value = mock_response

        result = self.policy.read_policy(name="admin")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(
                result.json(), {"data": {"name": "admin", "rules": "path '/*' { capabilities = ['create', 'read'] }"}}
            )
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/policy/admin",
        )

    def test_create_or_update_policy_with_string_policy_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.put.return_value = mock_response

        policy = 'path "/*" { capabilities = ["create", "read"] }'
        result = self.policy.create_or_update_policy(name="admin", policy=policy)

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/policy/admin",
            json={"policy": 'path "/*" { capabilities = ["create", "read"] }'},
        )

    def test_delete_policy_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.policy.delete_policy(name="admin")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/policy/admin",
        )
