from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


DEFAULT_MOUNT_POINT = "rabbitmq"


class RabbitMQ(AsyncVaultApiBase):
    """
    RabbitMQ Secrets Engine (API).
    Reference: https://www.vaultproject.io/api/secret/rabbitmq/index.html
    """

    async def configure(
        self,
        connection_uri: str = "",
        username: str = "",
        password: str = "",
        verify_connection: bool = True,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure shared information for the rabbitmq secrets engine.

        Supported methods:
            POST: /{mount_point}/config/connection. Produces: 204 (empty body)

        :param connection_uri: Specifies the RabbitMQ connection URI.
        :param username: Specifies the RabbitMQ management administrator username.
        :param password: Specifies the RabbitMQ management administrator password.
        :param verify_connection: Specifies whether to verify connection URI, username, and password.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :return: The response of the request.
        """
        params = {
            "connection_uri": connection_uri,
            "verify_connection": verify_connection,
            "username": username,
            "password": password,
        }

        api_path = f"/v1/{mount_point}/config/connection"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def configure_lease(self, ttl: int, max_ttl: int, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint configures the lease settings for generated credentials.

        :param ttl: Specifies the lease ttl provided in seconds.
        :param max_ttl: Specifies the maximum ttl provided in seconds.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config/lease"
        params = {
            "ttl": ttl,
            "max_ttl": max_ttl,
        }
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def create_role(
        self,
        name: str,
        tags: str = "",
        vhosts: str = "",
        vhost_topics: str = "",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint creates or updates the role definition.

        :param name:  Specifies the name of the role to create.
        :param tags:  Specifies a comma-separated RabbitMQ management tags.
        :param vhosts: Specifies a map of virtual hosts to permissions.
        :param vhost_topics: Specifies a map of virtual hosts and exchanges to topic permissions.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        params = {"tags": tags, "vhosts": vhosts, "vhost_topics": vhost_topics}
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint queries the role definition.

        :param name:  Specifies the name of the role to read.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def delete_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint deletes the role definition.
        Even if the role does not exist, this endpoint will still return await a successful response.

        :param name: Specifies the name of the role to delete.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def generate_credentials(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint generates a new set of dynamic credentials based on the named role.

        :param name: Specifies the name of the role to create credentials against.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/creds/{name}"
        return await self._adapter.get(
            url=api_path,
        )
