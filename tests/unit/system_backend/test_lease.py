import unittest
from unittest import mock

from httpx import Response

from vaultx.api.system_backend.lease import Lease


class TestLease(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.lease = Lease(self.mock_adapter)

    def test_read_lease_returns_response(self):
        mock_response = Response(200, json={"data": {"lease_id": "my-lease", "renewable": True}})
        self.mock_adapter.put.return_value = mock_response

        result = self.lease.read_lease(lease_id="my-lease")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"lease_id": "my-lease", "renewable": True}})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/leases/lookup",
            json={"lease_id": "my-lease"},
        )

    def test_list_leases_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["lease1", "lease2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.lease.list_leases(prefix="my-prefix")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"keys": ["lease1", "lease2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/sys/leases/lookup/my-prefix",
        )

    def test_renew_lease_with_increment_returns_response(self):
        mock_response = Response(200, json={"data": {"lease_id": "my-lease", "lease_duration": 3600}})
        self.mock_adapter.put.return_value = mock_response

        result = self.lease.renew_lease(lease_id="my-lease", increment=3600)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"lease_id": "my-lease", "lease_duration": 3600}})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/leases/renew",
            json={"lease_id": "my-lease", "increment": 3600},
        )

    def test_renew_lease_without_increment_returns_response(self):
        mock_response = Response(200, json={"data": {"lease_id": "my-lease", "lease_duration": 3600}})
        self.mock_adapter.put.return_value = mock_response

        result = self.lease.renew_lease(lease_id="my-lease")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"lease_id": "my-lease", "lease_duration": 3600}})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/leases/renew",
            json={"lease_id": "my-lease", "increment": None},
        )

    def test_revoke_lease_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.put.return_value = mock_response

        result = self.lease.revoke_lease(lease_id="my-lease")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/leases/revoke",
            json={"lease_id": "my-lease"},
        )

    def test_revoke_prefix_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.put.return_value = mock_response

        result = self.lease.revoke_prefix(prefix="my-prefix")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/leases/revoke-prefix/my-prefix",
            json={"prefix": "my-prefix"},
        )

    def test_revoke_force_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.put.return_value = mock_response

        result = self.lease.revoke_force(prefix="my-prefix")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/leases/revoke-force/my-prefix",
            json={"prefix": "my-prefix"},
        )
