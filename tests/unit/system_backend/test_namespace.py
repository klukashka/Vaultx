import unittest
from unittest import mock

from httpx import Response

from vaultx.api.system_backend import Namespace


class TestNamespace(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.namespace = Namespace(self.mock_adapter)

    def test_create_namespace_returns_response(self):
        mock_response = Response(200, json={"data": {"path": "my-namespace"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.namespace.create_namespace(path="my-namespace")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"path": "my-namespace"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/sys/namespaces/my-namespace",
        )

    def test_list_namespaces_returns_response(self):
        mock_response = Response(200, json={"data": {"keys": ["ns1/", "ns2/"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.namespace.list_namespaces()

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json(), {"data": {"keys": ["ns1/", "ns2/"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/sys/namespaces/",
        )

    def test_delete_namespace_returns_response(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.namespace.delete_namespace(path="my-namespace")

        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/sys/namespaces/my-namespace",
        )
