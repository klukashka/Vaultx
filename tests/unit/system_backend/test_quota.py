import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_system_backend.quota import Quota as AsyncQuota
from vaultx.api.system_backend.quota import Quota


class TestQuota(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.quota = Quota(self.mock_adapter)

    def test_read_quota_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "my-quota", "rate": 10}})
        self.mock_adapter.get.return_value = mock_response

        result = self.quota.read_quota(name="my-quota")

        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "my-quota", "rate": 10}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/quotas/rate-limit/my-quota",
        )

    def test_list_quotas_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["quota1", "quota2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.quota.list_quotas()

        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["quota1", "quota2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/sys/quotas/rate-limit",
        )

    def test_create_or_update_quota_with_all_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.quota.create_or_update_quota(
            name="my-quota",
            rate=10,
            path="my-path",
            interval="5s",
            block_interval="10s",
            role="my-role",
            rate_limit_type="rate-limit",
            inheritable=True,
        )

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/quotas/rate-limit/my-quota",
            json={
                "name": "my-quota",
                "rate": 10,
                "path": "my-path",
                "interval": "5s",
                "block_interval": "10s",
                "role": "my-role",
                "type": "rate-limit",
                "inheritable": True,
            },
        )

    def test_create_or_update_quota_with_minimal_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.quota.create_or_update_quota(
            name="my-quota",
            rate=10,
        )

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/quotas/rate-limit/my-quota",
            json={
                "name": "my-quota",
                "rate": 10,
                "interval": "1s",  # Default value
            },
        )

    def test_delete_quota_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.quota.delete_quota(name="my-quota")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/quotas/rate-limit/my-quota",
        )


class TestAsyncQuota(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.quota = AsyncQuota(self.mock_adapter)

    async def test_read_quota_returns_response(self):
        mock_response = Response(200, json={"data": {"name": "my-quota", "rate": 10}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.quota.read_quota(name="my-quota")

        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "my-quota", "rate": 10}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/sys/quotas/rate-limit/my-quota",
        )

    async def test_list_quotas_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["quota1", "quota2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.quota.list_quotas()

        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["quota1", "quota2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/sys/quotas/rate-limit",
        )

    async def test_create_or_update_quota_with_all_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.quota.create_or_update_quota(
            name="my-quota",
            rate=10,
            path="my-path",
            interval="5s",
            block_interval="10s",
            role="my-role",
            rate_limit_type="rate-limit",
            inheritable=True,
        )

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/quotas/rate-limit/my-quota",
            json={
                "name": "my-quota",
                "rate": 10,
                "path": "my-path",
                "interval": "5s",
                "block_interval": "10s",
                "role": "my-role",
                "type": "rate-limit",
                "inheritable": True,
            },
        )

    async def test_create_or_update_quota_with_minimal_parameters_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.quota.create_or_update_quota(
            name="my-quota",
            rate=10,
        )

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/quotas/rate-limit/my-quota",
            json={
                "name": "my-quota",
                "rate": 10,
                "interval": "1s",  # Default value
            },
        )

    async def test_delete_quota_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.quota.delete_quota(name="my-quota")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/quotas/rate-limit/my-quota",
        )
