import json
from unittest import IsolatedAsyncioTestCase, TestCase

import httpx
import respx

from vaultx import AsyncClient, Client
from vaultx.exceptions import VaultxError


class TestAuthMethods(TestCase):
    """Tests for methods related to Vault sys/auth routes."""

    def test_tune_auth_backend(self):
        client = Client()
        expected_status_code = 204
        test_mount_point = "approle-test"
        test_description = "this is a test description"
        expected_response = httpx.Response(status_code=expected_status_code)
        with respx.mock:
            route = respx.request(
                method="POST",
                url=f"http://localhost:8200/v1/sys/auth/{test_mount_point}/tune",
            ).mock(return_value=expected_response)
            actual_response = client.sys.tune_auth_method(
                path=test_mount_point,
                description=test_description,
            )
            actual_request_params = json.loads(route.calls.last.request.content)

        if isinstance(actual_response, httpx.Response) and isinstance(actual_request_params, dict):
            self.assertEqual(
                first=expected_status_code,
                second=actual_response.status_code,
            )

            # Ensure we sent through an optional tune parameter as expected
            self.assertEqual(
                first=test_description,
                second=actual_request_params["description"],
            )
        else:
            raise VaultxError("Unexpected response types")

    def test_get_auth_backend_tuning(self):
        client = Client()
        expected_status_code = 200
        test_mount_point = "approle-test"
        mock_response = {
            "max_lease_ttl": 12345678,
            "lease_id": "",
            "force_no_cache": False,
            "warnings": None,
            "data": {
                "force_no_cache": False,
                "default_lease_ttl": 2764800,
                "max_lease_ttl": 12345678,
            },
            "wrap_info": None,
            "auth": None,
            "lease_duration": 0,
            "request_id": "673f2336-3235-b988-2194-c68261a02bfe",
            "default_lease_ttl": 2764800,
            "renewable": False,
        }
        expected_response = httpx.Response(
            status_code=expected_status_code,
            json=mock_response,
        )
        with respx.mock:
            respx.request(
                method="GET",
                url=f"http://localhost:8200/v1/sys/auth/{test_mount_point}/tune",
            ).mock(
                return_value=expected_response,
            )
            actual_response = client.sys.read_auth_method_tuning(
                path=test_mount_point,
            )
        self.assertEqual(
            first=mock_response,
            second=actual_response,
        )


class TestAsyncAuthMethods(IsolatedAsyncioTestCase):
    """Tests for methods related to Vault sys/auth routes."""

    async def test_tune_auth_backend(self):
        client = AsyncClient(client=httpx.AsyncClient())
        expected_status_code = 204
        test_mount_point = "approle-test"
        test_description = "this is a test description"
        expected_response = httpx.Response(status_code=expected_status_code)
        async with respx.mock:
            route = respx.request(
                method="POST",
                url=f"http://localhost:8200/v1/sys/auth/{test_mount_point}/tune",
            ).mock(return_value=expected_response)
            actual_response = await client.sys.tune_auth_method(
                path=test_mount_point,
                description=test_description,
            )
            actual_request_params = json.loads(route.calls.last.request.content)

        if isinstance(actual_response, httpx.Response) and isinstance(actual_request_params, dict):
            self.assertEqual(
                first=expected_status_code,
                second=actual_response.status_code,
            )

            # Ensure we sent through an optional tune parameter as expected
            self.assertEqual(
                first=test_description,
                second=actual_request_params["description"],
            )
        else:
            raise VaultxError("Unexpected response types")

    async def test_get_auth_backend_tuning(self):
        client = AsyncClient(client=httpx.AsyncClient())
        expected_status_code = 200
        test_mount_point = "approle-test"
        mock_response = {
            "max_lease_ttl": 12345678,
            "lease_id": "",
            "force_no_cache": False,
            "warnings": None,
            "data": {
                "force_no_cache": False,
                "default_lease_ttl": 2764800,
                "max_lease_ttl": 12345678,
            },
            "wrap_info": None,
            "auth": None,
            "lease_duration": 0,
            "request_id": "673f2336-3235-b988-2194-c68261a02bfe",
            "default_lease_ttl": 2764800,
            "renewable": False,
        }
        expected_response = httpx.Response(
            status_code=expected_status_code,
            json=mock_response,
        )
        async with respx.mock:
            respx.request(
                method="GET",
                url=f"http://localhost:8200/v1/sys/auth/{test_mount_point}/tune",
            ).mock(
                return_value=expected_response,
            )
            actual_response = await client.sys.read_auth_method_tuning(
                path=test_mount_point,
            )
        self.assertEqual(
            first=mock_response,
            second=actual_response,
        )
