import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.rabbitmq import RabbitMQ as AsyncRabbitMQ
from vaultx.api.secrets_engines.rabbitmq import RabbitMQ


class TestRabbitMQ(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.rabbitmq = RabbitMQ(self.mock_adapter)

    def test_configure(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.rabbitmq.configure(
            connection_uri="amqp://localhost:5672",
            username="admin",
            password="password",
            verify_connection=True,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/rabbitmq/config/connection",
            json={
                "connection_uri": "amqp://localhost:5672",
                "username": "admin",
                "password": "password",
                "verify_connection": True,
            },
        )

    def test_configure_lease(self):
        mock_response = Response(200, json={"data": {"ttl": 3600, "max_ttl": 7200}})
        self.mock_adapter.post.return_value = mock_response

        result = self.rabbitmq.configure_lease(ttl=3600, max_ttl=7200)
        self.assertEqual(result.json(), {"data": {"ttl": 3600, "max_ttl": 7200}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/rabbitmq/config/lease",
            json={"ttl": 3600, "max_ttl": 7200},
        )

    def test_create_role(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.rabbitmq.create_role(
            name="test-role",
            tags="administrator",
            vhosts="vhost1",
            vhost_topics="topic1",
        )
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/rabbitmq/roles/test-role",
            json={"tags": "administrator", "vhosts": "vhost1", "vhost_topics": "topic1"},
        )

    def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.rabbitmq.read_role(name="test-role")
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/rabbitmq/roles/test-role",
        )

    def test_delete_role(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.rabbitmq.delete_role(name="test-role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/rabbitmq/roles/test-role",
        )

    def test_generate_credentials(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.rabbitmq.generate_credentials(name="test-role")
        self.assertEqual(result.json(), {"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/rabbitmq/creds/test-role",
        )


class TestAsyncRabbitMQ(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.rabbitmq = AsyncRabbitMQ(self.mock_adapter)

    async def test_configure_async(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.rabbitmq.configure(
            connection_uri="amqp://localhost:5672",
            username="admin",
            password="password",
            verify_connection=True,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/rabbitmq/config/connection",
            json={
                "connection_uri": "amqp://localhost:5672",
                "username": "admin",
                "password": "password",
                "verify_connection": True,
            },
        )

    async def test_configure_lease_async(self):
        mock_response = Response(200, json={"data": {"ttl": 3600, "max_ttl": 7200}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.rabbitmq.configure_lease(ttl=3600, max_ttl=7200)
        self.assertEqual(result.json(), {"data": {"ttl": 3600, "max_ttl": 7200}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/rabbitmq/config/lease",
            json={"ttl": 3600, "max_ttl": 7200},
        )

    async def test_create_role_async(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.rabbitmq.create_role(
            name="test-role",
            tags="administrator",
            vhosts="vhost1",
            vhost_topics="topic1",
        )
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/rabbitmq/roles/test-role",
            json={"tags": "administrator", "vhosts": "vhost1", "vhost_topics": "topic1"},
        )

    async def test_read_role_async(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.rabbitmq.read_role(name="test-role")
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/rabbitmq/roles/test-role",
        )

    async def test_delete_role_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.rabbitmq.delete_role(name="test-role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/rabbitmq/roles/test-role",
        )

    async def test_generate_credentials_async(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.rabbitmq.generate_credentials(name="test-role")
        self.assertEqual(result.json(), {"data": {"username": "test-user", "password": "test-password"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/rabbitmq/creds/test-role",
        )
