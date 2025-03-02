import unittest
from unittest import mock

from httpx import Response

from vaultx.api.system_backend.health import Health
from vaultx.exceptions import VaultxError


class TestHealth(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.health = Health(self.mock_adapter)

    def test_read_health_status_head(self):
        self.mock_adapter.head.return_value = Response(200)
        result = self.health.read_health_status(method="HEAD")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
        self.mock_adapter.head.assert_called_once_with(
            url="/v1/sys/health",
            raise_exception=False,
        )

    def test_read_health_status_get(self):
        self.mock_adapter.get.return_value = {"initialized": True}
        result = self.health.read_health_status(method="GET")
        self.assertEqual(result, {"initialized": True})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/health",
            params={},
            raise_exception=False,
        )

    def test_read_health_status_get_with_params(self):
        self.mock_adapter.get.return_value = {"initialized": True}
        result = self.health.read_health_status(
            standby_ok=True,
            active_code=200,
            standby_code=200,
            dr_secondary_code=200,
            performance_standby_code=200,
            sealed_code=200,
            uninit_code=200,
            method="GET",
        )
        self.assertEqual(result, {"initialized": True})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/health",
            params={
                "standbyok": True,
                "activecode": 200,
                "standbycode": 200,
                "drsecondarycode": 200,
                "performancestandbycode": 200,
                "sealedcode": 200,
                "uninitcode": 200,
            },
            raise_exception=False,
        )

    def test_read_health_status_invalid_method(self):
        with self.assertRaises(VaultxError) as context:
            self.health.read_health_status(method="POST")
        self.assertEqual(
            str(context.exception),
            '"method" parameter provided invalid value; HEAD or GET allowed, "POST" provided',
        )
