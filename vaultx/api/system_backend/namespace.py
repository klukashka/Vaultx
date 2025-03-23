from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase


class Namespace(VaultApiBase):
    def create_namespace(self, path: str) -> VaultxResponse:
        """
        Create a namespace at the given path.

        Supported methods:
            POST: /sys/namespaces/{path}. Produces: 200 application/json

        :return: The response of the request.
        """
        api_path = f"/v1/sys/namespaces/{path}"
        return self._adapter.post(
            url=api_path,
        )

    def list_namespaces(self) -> VaultxResponse:
        """
        Lists all the namespaces.

        Supported methods:
            LIST: /sys/namespaces. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        api_path = "/v1/sys/namespaces/"
        return self._adapter.list(
            url=api_path,
        )

    def delete_namespace(self, path: str) -> VaultxResponse:
        """
        Delete a namespaces. You cannot delete a namespace with existing child namespaces.

        Supported methods:
            DELETE: /sys/namespaces. Produces: 204 (empty body)

        :return: The response of the request.
        """
        api_path = f"/v1/sys/namespaces/{path}"
        return self._adapter.delete(
            url=api_path,
        )
