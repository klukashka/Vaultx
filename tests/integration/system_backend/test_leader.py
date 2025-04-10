from unittest import TestCase
from unittest.async_case import IsolatedAsyncioTestCase

from tests.utils.vaultx_integration_test_case import AsyncVaultxIntegrationTestCase, VaultxIntegrationTestCase


class TestLeader(VaultxIntegrationTestCase, TestCase):
    def test_read_health_status(self):
        self.assertIn(
            member="ha_enabled",
            container=self.client.sys.read_leader_status(),
        )


class TestAsyncLeader(AsyncVaultxIntegrationTestCase, IsolatedAsyncioTestCase):
    async def test_read_health_status(self):
        self.assertIn(
            member="ha_enabled",
            container=(await self.client.sys.read_leader_status()),
        )
