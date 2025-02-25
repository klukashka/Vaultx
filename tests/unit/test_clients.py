from unittest import TestCase

from vaultx import Client
from vaultx.adapters import JsonAdapter


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
