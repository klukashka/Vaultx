from unittest import IsolatedAsyncioTestCase, TestCase

from vaultx import AsyncClient, Client
from vaultx.adapters import AsyncJsonAdapter, JsonAdapter


class TestClient(TestCase):
    """Unit tests providing coverage for client related methods."""

    def test_setting_adapter_on_client_sets_adapter_of_endpoint_classes(self):
        client = Client()
        old_adapter = client.adapter

        client.adapter = JsonAdapter()

        self.assertIsNot(client.adapter, old_adapter)
        self.assertSetEqual(
            {client.adapter},
            {client.secrets.adapter, client.sys.adapter, client.auth.adapter},
        )


class TestAsyncClient(IsolatedAsyncioTestCase):
    """Unit tests providing coverage for async_client related methods."""

    async def test_setting_adapter_on_client_sets_adapter_of_endpoint_classes(self):
        client = AsyncClient()
        old_adapter = client.adapter

        client.adapter = AsyncJsonAdapter()

        self.assertIsNot(client.adapter, old_adapter)
        self.assertSetEqual(
            {client.adapter},
            {client.secrets.adapter, client.sys.adapter, client.auth.adapter},
        )
