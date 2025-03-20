from unittest import IsolatedAsyncioTestCase, TestCase

import httpx
import respx
from parameterized import parameterized  # type: ignore

from vaultx import adapters
from vaultx.constants.client import DEFAULT_URL


class TestRequest(TestCase):
    """Unit tests providing coverage for requests-related methods in the vaultx Client class."""

    @parameterized.expand(
        [
            ("standard Vault address", "https://localhost:8200", None, None),
            ("Vault address with route", "https://example.com/vault", None, None),
            ("regression test", "https://localhost:8200", "keyring/http://some.url/sub/entry", None),
            (
                "redirect with location header",
                "https://localhost:8200",
                "secret/some-secret",
                "https://another-place.com/secret/some-secret",
            ),
        ]
    )
    def test_get(self, name, url, path, redirect_url):
        path = path.replace("//", "/") if path else "v1/sys/health"
        mock_url = f"{url}/{path}"
        expected_status_code = 200
        adapter = adapters.VaultxAdapter(base_uri=url)
        response_headers = {}
        response_status_code = 200
        if redirect_url is not None:
            response_headers["Location"] = redirect_url
            response_status_code = 301
        expected_response = httpx.Response(response_status_code, json={"name": "baz"}, headers=response_headers)
        with respx.mock:
            respx.request(
                method="GET",
                url=mock_url,
            ).mock(return_value=expected_response)
            if redirect_url is not None:
                respx.request(
                    method="GET",
                    url=redirect_url,
                )

            response = adapter.get(url=path)

        self.assertEqual(
            expected_status_code,
            response.status,
        )

    @parameterized.expand(
        [
            ("kv secret lookup", "v1/secret/some-secret"),
        ]
    )
    def test_list(self, name, test_path):
        mock_response = {
            "auth": None,
            "data": {"keys": ["things1", "things2"]},
            "lease_duration": 0,
            "lease_id": "",
            "renewable": False,
            "request_id": "ba933afe-84d4-410f-161b-592a5c016009",
            "warnings": None,
            "wrap_info": None,
        }
        expected_status_code = 200
        mock_url = f"{DEFAULT_URL}/{test_path}"
        with respx.mock:
            resp_json = httpx.Response(status_code=expected_status_code, json=mock_response)
            respx.request(method="LIST", url=mock_url).mock(return_value=resp_json)
            adapter = adapters.VaultxAdapter()
            response = adapter.list(
                url=test_path,
            )

        self.assertEqual(
            first=expected_status_code,
            second=response.status,
        )
        self.assertEqual(first=mock_response, second=response.value)


class TestAsyncRequest(IsolatedAsyncioTestCase):
    """Unit tests providing coverage for requests-related methods in the vaultx Client class."""

    @parameterized.expand(
        [
            ("standard Vault address", "https://localhost:8200", None, None),
            ("Vault address with route", "https://example.com/vault", None, None),
            ("regression test", "https://localhost:8200", "keyring/http://some.url/sub/entry", None),
            (
                "redirect with location header",
                "https://localhost:8200",
                "secret/some-secret",
                "https://another-place.com/secret/some-secret",
            ),
        ]
    )
    async def test_get(self, name, url, path, redirect_url):
        path = path.replace("//", "/") if path else "v1/sys/health"
        mock_url = f"{url}/{path}"
        expected_status_code = 200
        adapter = adapters.AsyncVaultxAdapter(base_uri=url, client=httpx.AsyncClient())
        response_headers = {}
        response_status_code = 200
        if redirect_url is not None:
            response_headers["Location"] = redirect_url
            response_status_code = 301
        expected_response = httpx.Response(response_status_code, json={"name": "baz"}, headers=response_headers)
        async with respx.mock:
            respx.request(
                method="GET",
                url=mock_url,
            ).mock(return_value=expected_response)
            if redirect_url is not None:
                respx.request(
                    method="GET",
                    url=redirect_url,
                )

            response = await adapter.get(url=path)

        self.assertEqual(
            expected_status_code,
            response.status,
        )

    @parameterized.expand(
        [
            ("kv secret lookup", "v1/secret/some-secret"),
        ]
    )
    async def test_list(self, name, test_path):
        mock_response = {
            "auth": None,
            "data": {"keys": ["things1", "things2"]},
            "lease_duration": 0,
            "lease_id": "",
            "renewable": False,
            "request_id": "ba933afe-84d4-410f-161b-592a5c016009",
            "warnings": None,
            "wrap_info": None,
        }
        expected_status_code = 200
        mock_url = f"{DEFAULT_URL}/{test_path}"
        async with respx.mock:
            resp_json = httpx.Response(status_code=expected_status_code, json=mock_response)
            respx.request(method="LIST", url=mock_url).mock(return_value=resp_json)
            adapter = adapters.AsyncVaultxAdapter(client=httpx.AsyncClient())
            response = await adapter.list(
                url=test_path,
            )

        self.assertEqual(
            first=expected_status_code,
            second=response.status,
        )
        self.assertEqual(first=mock_response, second=response.value)
