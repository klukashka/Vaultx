from unittest import TestCase

import httpx
import pytest
import respx
from parameterized import parameterized  # type: ignore

from vaultx import Client


class TestClientWriteData:
    test_url = "https://vault.example.com"
    test_path = "whatever/fake"
    response = {"a": 1, "b": "two"}

    @pytest.fixture(autouse=True)
    def write_mock(self):
        with respx.mock:
            yield respx.request(
                method="POST",
                url=f"{self.test_url}/v1/{self.test_path}",
            ).mock(return_value=httpx.Response(status_code=200, json=self.response))

    @pytest.fixture
    def client(self) -> Client:
        return Client(url=self.test_url)

    @pytest.mark.parametrize("wrap_ttl", [None, "3m"])
    def test_write_data(self, client: Client, wrap_ttl: str):
        response = client.write(self.test_path, data={"data": "cool"}, wrap_ttl=wrap_ttl)
        assert response == self.response


class TestSystemBackendMethods(TestCase):
    """Unit tests providing coverage for Vault system backend-related methods in the vaultx Client class."""

    @parameterized.expand(
        [
            ("pki lease ID", "pki/issue/my-role/12c7e036-b59e-5e79-3370-03826fc6f34b"),
        ]
    )
    def test_read_lease(self, test_label, test_lease_id):
        test_path = "http://localhost:8200/v1/sys/leases/lookup"
        client = Client()
        mock_response = {
            "issue_time": "2018-07-15T08:35:34.775859245-05:00",
            "renewable": False,
            "id": test_lease_id,
            "ttl": 259199,
            "expire_time": "2018-07-18T08:35:34.00004241-05:00",
            "last_renewal": None,
        }
        with respx.mock:
            respx.request(
                method="PUT",
                url=test_path,
            ).mock(return_value=httpx.Response(status_code=200, json=mock_response))
            response = client.sys.read_lease(
                lease_id=test_lease_id,
            )
            self.assertEqual(
                first=mock_response,
                second=response,
            )
