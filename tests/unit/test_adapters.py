from unittest import TestCase

import httpx
import pytest
import respx
from parameterized import parameterized

from vaultx import adapters
from vaultx.constants.client import DEFAULT_URL


class TestAdapters:
    CONSTRUCTOR_ARGS = (
        "base_uri",
        "token",
        "cert",
        "verify",
        "timeout",
        "proxy",
        "follow_redirects",
        "client",
        "namespace",
        "ignore_exceptions",
        "strict_http",
        "request_header",
    )

    INTERNAL_KWARGS = (
        "cert",
        "verify",
        "timeout",
        "proxy",
    )

    @pytest.mark.parametrize(
        "conargs",
        [
            {arg: arg.capitalize() for arg in CONSTRUCTOR_ARGS},
            {arg: arg.upper() for arg in CONSTRUCTOR_ARGS},
        ],
    )
    def test_from_adapter(self, conargs):
        # set client to None so that the adapter will create its own internally
        conargs["client"] = None
        conargs["proxy"] = None
        conargs["cert"] = None
        conargs["verify"] = None
        expected = conargs.copy()
        for internal_kwarg in self.INTERNAL_KWARGS:
            expected.setdefault("_kwargs", {})[internal_kwarg] = expected.pop(internal_kwarg)

        # let's start with a JsonAdapter, and make a RawAdapter out of it
        json_adapter = adapters.JsonAdapter(**conargs)

        # reset the expected client to be the one created by the JsonAdapter
        expected["client"] = json_adapter.client

        raw_adapter = adapters.RawAdapter.from_adapter(json_adapter)

        for property_key, value in expected.items():
            assert getattr(raw_adapter, property_key) == value


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
        adapter = adapters.RawAdapter(base_uri=url)
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
            response.status_code,
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
            adapter = adapters.RawAdapter()
            response = adapter.list(
                url=test_path,
            )
        self.assertEqual(
            first=expected_status_code,
            second=response.status_code,
        )
        self.assertEqual(first=mock_response, second=response.json())
