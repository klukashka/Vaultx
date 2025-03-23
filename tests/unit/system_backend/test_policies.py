import unittest
from unittest import mock

import pytest
from httpx import Response

from vaultx.api.async_system_backend.policies import Policies as AsyncPolicies
from vaultx.api.system_backend.policies import Policies


class TestPolicies(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.policies = Policies(self.mock_adapter)

    def test_list_acl_policies(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["policy1", "policy2"]}}
        result = self.policies.list_acl_policies()
        self.assertEqual(result, {"data": {"keys": ["policy1", "policy2"]}})
        self.mock_adapter.list.assert_called_once()

    def test_read_acl_policy(self):
        self.mock_adapter.get.return_value = {"data": {"name": "test_policy"}}
        result = self.policies.read_acl_policy(name="test_policy")
        self.assertEqual(result, {"data": {"name": "test_policy"}})
        self.mock_adapter.get.assert_called_once()

    def test_create_or_update_acl_policy(self):
        self.mock_adapter.put.return_value = Response(204)
        result = self.policies.create_or_update_acl_policy(
            name="test_policy",
            policy={"key": "value"},
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once()

    def test_delete_acl_policy(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.policies.delete_acl_policy(name="test_policy")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_list_rgp_policies(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["policy1", "policy2"]}}
        result = self.policies.list_rgp_policies()
        self.assertEqual(result, {"data": {"keys": ["policy1", "policy2"]}})
        self.mock_adapter.list.assert_called_once()

    def test_read_rgp_policy(self):
        self.mock_adapter.get.return_value = {"data": {"name": "test_policy"}}
        result = self.policies.read_rgp_policy(name="test_policy")
        self.assertEqual(result, {"data": {"name": "test_policy"}})
        self.mock_adapter.get.assert_called_once()

    def test_create_or_update_rgp_policy(self):
        self.mock_adapter.put.return_value = Response(204)
        result = self.policies.create_or_update_rgp_policy(
            name="test_policy",
            policy="test_policy",
            enforcement_level="advisory",
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once()

    def test_delete_rgp_policy(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.policies.delete_rgp_policy(name="test_policy")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_list_egp_policies(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["policy1", "policy2"]}}
        result = self.policies.list_egp_policies()
        self.assertEqual(result, {"data": {"keys": ["policy1", "policy2"]}})
        self.mock_adapter.list.assert_called_once()

    def test_read_egp_policy(self):
        self.mock_adapter.get.return_value = {"data": {"name": "test_policy"}}
        result = self.policies.read_egp_policy(name="test_policy")
        self.assertEqual(result, {"data": {"name": "test_policy"}})
        self.mock_adapter.get.assert_called_once()

    def test_create_or_update_egp_policy(self):
        self.mock_adapter.put.return_value = Response(204)
        result = self.policies.create_or_update_egp_policy(
            name="test_policy",
            policy="test_policy",
            enforcement_level="advisory",
            paths=["path1", "path2"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once()

    def test_delete_egp_policy(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.policies.delete_egp_policy(name="test_policy")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()


@pytest.mark.asyncio
class TestAsyncPolicies:
    def setup_method(self):
        self.mock_adapter = mock.AsyncMock()
        self.policies = AsyncPolicies(self.mock_adapter)

    async def test_list_acl_policies(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["policy1", "policy2"]}}
        result = await self.policies.list_acl_policies()
        assert result == {"data": {"keys": ["policy1", "policy2"]}}
        self.mock_adapter.list.assert_called_once()

    async def test_read_acl_policy(self):
        self.mock_adapter.get.return_value = {"data": {"name": "test_policy"}}
        result = await self.policies.read_acl_policy(name="test_policy")
        assert result == {"data": {"name": "test_policy"}}
        self.mock_adapter.get.assert_called_once()

    async def test_create_or_update_acl_policy(self):
        self.mock_adapter.put.return_value = Response(204)
        result = await self.policies.create_or_update_acl_policy(name="test_policy", policy={"key": "value"})
        assert result.status_code == 204
        self.mock_adapter.put.assert_called_once()

    async def test_delete_acl_policy(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.policies.delete_acl_policy(name="test_policy")
        assert result.status_code == 204
        self.mock_adapter.delete.assert_called_once()

    async def test_list_rgp_policies(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["policy1", "policy2"]}}
        result = await self.policies.list_rgp_policies()
        assert result == {"data": {"keys": ["policy1", "policy2"]}}
        self.mock_adapter.list.assert_called_once()

    async def test_read_rgp_policy(self):
        self.mock_adapter.get.return_value = {"data": {"name": "test_policy"}}
        result = await self.policies.read_rgp_policy(name="test_policy")
        assert result == {"data": {"name": "test_policy"}}
        self.mock_adapter.get.assert_called_once()

    async def test_create_or_update_rgp_policy(self):
        self.mock_adapter.put.return_value = Response(204)
        result = await self.policies.create_or_update_rgp_policy(
            name="test_policy", policy="test_policy", enforcement_level="advisory"
        )
        assert result.status_code == 204
        self.mock_adapter.put.assert_called_once()

    async def test_delete_rgp_policy(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.policies.delete_rgp_policy(name="test_policy")
        assert result.status_code == 204
        self.mock_adapter.delete.assert_called_once()

    async def test_list_egp_policies(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["policy1", "policy2"]}}
        result = await self.policies.list_egp_policies()
        assert result == {"data": {"keys": ["policy1", "policy2"]}}
        self.mock_adapter.list.assert_called_once()

    async def test_read_egp_policy(self):
        self.mock_adapter.get.return_value = {"data": {"name": "test_policy"}}
        result = await self.policies.read_egp_policy(name="test_policy")
        assert result == {"data": {"name": "test_policy"}}
        self.mock_adapter.get.assert_called_once()

    async def test_create_or_update_egp_policy(self):
        self.mock_adapter.put.return_value = Response(204)
        result = await self.policies.create_or_update_egp_policy(
            name="test_policy",
            policy="test_policy",
            enforcement_level="advisory",
            paths=["path1", "path2"],
        )
        assert result.status_code == 204
        self.mock_adapter.put.assert_called_once()

    async def test_delete_egp_policy(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.policies.delete_egp_policy(name="test_policy")
        assert result.status_code == 204
        self.mock_adapter.delete.assert_called_once()
