import unittest
from unittest import mock
from unittest.mock import AsyncMock

import pytest
from httpx import Response

from vaultx.api.async_system_backend.policy import Policy as AsyncPolicy
from vaultx.api.system_backend.policy import Policy


class TestPolicy(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.policy = Policy(self.mock_adapter)

    def test_list_policies_returns_response(self):
        mock_response = Response(200, json={"data": {"policies": ["default", "admin"]}})
        self.mock_adapter.get.return_value = mock_response

        result = self.policy.list_policies()

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

        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/policy/admin",
            json={"policy": 'path "/*" { capabilities = ["create", "read"] }'},
        )

    def test_delete_policy_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.policy.delete_policy(name="admin")

        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/policy/admin",
        )


@pytest.fixture
async def mock_async_adapter():
    return AsyncMock()


@pytest.fixture
async def async_policy(mock_async_adapter):
    return AsyncPolicy(mock_async_adapter)


@pytest.mark.asyncio
async def test_list_policies_returns_response(async_policy, mock_async_adapter):
    mock_response = Response(200, json={"data": {"policies": ["default", "admin"]}})
    mock_async_adapter.get.return_value = mock_response

    result = await async_policy.list_policies()

    assert result.status_code == 200
    assert result.json() == {"data": {"policies": ["default", "admin"]}}
    mock_async_adapter.get.assert_called_once_with(url="/v1/sys/policy")


@pytest.mark.asyncio
async def test_read_policy_returns_response(async_policy, mock_async_adapter):
    mock_response = Response(
        200, json={"data": {"name": "admin", "rules": "path '/*' { capabilities = ['create', 'read'] }"}}
    )
    mock_async_adapter.get.return_value = mock_response

    result = await async_policy.read_policy(name="admin")

    assert result.status_code == 200
    assert result.json() == {"data": {"name": "admin", "rules": "path '/*' { capabilities = ['create', 'read'] }"}}
    mock_async_adapter.get.assert_called_once_with(url="/v1/sys/policy/admin")


@pytest.mark.asyncio
async def test_create_or_update_policy_with_string_policy_returns_response(async_policy, mock_async_adapter):
    mock_response = Response(204)
    mock_async_adapter.put.return_value = mock_response

    policy_data = 'path "/*" { capabilities = ["create", "read"] }'
    result = await async_policy.create_or_update_policy(name="admin", policy=policy_data)

    assert result.status_code == 204
    mock_async_adapter.put.assert_called_once_with(
        url="/v1/sys/policy/admin", json={"policy": 'path "/*" { capabilities = ["create", "read"] }'}
    )


@pytest.mark.asyncio
async def test_delete_policy_returns_response(async_policy, mock_async_adapter):
    mock_response = Response(204)
    mock_async_adapter.delete.return_value = mock_response

    result = await async_policy.delete_policy(name="admin")

    assert result.status_code == 204
    mock_async_adapter.delete.assert_called_once_with(url="/v1/sys/policy/admin")
