from typing import Any, Optional

from vaultx import exceptions
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase
from vaultx.exceptions import VaultxError


DEFAULT_MOUNT_POINT = "secret"


class KvV2(AsyncVaultApiBase):
    """
    KV Secrets Engine - Version 2 (API).

    Reference: https://www.vaultproject.io/api/secret/kv/kv-v2.html
    """

    async def configure(
        self,
        max_versions: int = 10,
        cas_required: Optional[bool] = None,
        delete_version_after: str = "0s",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure backend level settings that are applied to every key in the key-value store.

        Supported methods:
            POST: /{mount_point}/config. Produces: 204 (empty body)


        :param max_versions: The number of versions to keep per key. This value applies to all keys, but a key's
            metadata setting can overwrite this value. Once a key has more than the configured allowed versions the
            oldest version will be permanently deleted. Defaults to 10.
        :param cas_required: If true all keys will require the cas parameter to be set on all write requests.
        :param mount_point: The "path" the secret engine was mounted on.
        :param delete_version_after: Specifies the length of time before a version is deleted.
            Defaults to "0s" (i.e., disabled).
        :return: The response of the request.
        """
        params = {
            "max_versions": max_versions,
            "delete_version_after": delete_version_after,
        }
        if cas_required is not None:
            params["cas_required"] = cas_required
        api_path = f"/v1/{mount_point}/config"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_configuration(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the KV Version 2 configuration.

        Supported methods:
            GET: /auth/{mount_point}/config. Produces: 200 application/json


        :param mount_point: The "path" the secret engine was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config"
        return await self._adapter.get(url=api_path)

    async def read_secret(
        self, path: str, mount_point: str = DEFAULT_MOUNT_POINT, raise_on_deleted_version: bool = False
    ) -> Optional[VaultxResponse]:
        """
        Retrieve the secret at the specified location.

        Equivalent to calling read_secret_version with version=None.

        Supported methods:
            GET: /{mount_point}/data/{path}. Produces: 200 application/json


        :param path: Specifies the path of the secret to read. This is specified as part of the URL.
        :param mount_point: The "path" the secret engine was mounted on.
        :param raise_on_deleted_version: Changes the behavior when the requested version is deleted.
            If True an exception will be raised.
            If False, nothing is returned.
        :return: The VaultxResponse of the request.
        """
        return await self.read_secret_version(
            path=path,
            mount_point=mount_point,
            raise_on_deleted_version=raise_on_deleted_version,
        )

    async def read_secret_version(
        self,
        path: str,
        version: Optional[int] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        raise_on_deleted_version: bool = False,
    ) -> Optional[VaultxResponse]:
        """
        Retrieve the secret at the specified location, with the specified version.

        Supported methods:
            GET: /{mount_point}/data/{path}. Produces: 200 application/json


        :param path: Specifies the path of the secret to read. This is specified as part of the URL.
        :param version: Specifies the version to return. If not set the latest version is returned.
        :type version: int
        :param mount_point: The "path" the secret engine was mounted on.
        :param raise_on_deleted_version: Changes the behavior when the requested version is deleted.
            If True an exception will be raised.
            If False, nothing is returned.
        :return: The VaultxResponse of the request.
        """

        params = {}
        if version is not None:
            params["version"] = version
        api_path = f"/v1/{mount_point}/data/{path}"
        try:
            return await self._adapter.get(
                url=api_path,
                params=params,
            )
        except exceptions.HTTPError:
            if not raise_on_deleted_version:
                return None
            raise

    async def create_or_update_secret(
        self, path: str, secret, cas: Optional[int] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Create a new version of a secret at the specified location.

        If the value does not yet exist, the calling token must have an ACL policy granting the capability of creating.
        If the value already exists, the calling token must have an ACL policy granting the update capability.

        Supported methods:
            POST: /{mount_point}/data/{path}. Produces: 200 application/json

        :param path: Path
        :param cas: Set the "cas" value to use a Check-And-Set operation.
            None: writing will be allowed.
            0: writing will only be allowed if the key doesn't exist.
            Non-zero: writing will only be allowed if the key's current version matches the version
            specified in the cas parameter.
        :param secret: The contents of the "secret" dict will be stored and returned on read.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The VaultxResponse of the request.
        """
        params = {"options": {}, "data": secret}

        if cas is not None:
            params["options"]["cas"] = cas

        api_path = f"/v1/{mount_point}/data/{path}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def patch(self, path: str, secret: dict[Any, Any], mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Set or update data in the KV store without overwriting.

        :param path: Path
        :param secret: The contents of the "secret" dict will be stored and returned on read.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The VaultxResponse of the create_or_update_secret request.
        """
        # First, do a read.
        try:
            current_secret_version = await self.read_secret_version(
                path=path,
                mount_point=mount_point,
            )
            if current_secret_version is None:
                raise VaultxError(f"Failed to read secret version from {path}")
            if current_secret_version.status == 404:
                raise exceptions.HTTPError(
                    status_code=404,
                    method="GET",
                    detail=f'No value found at "{path}"; patch only works on existing data.',
                )
        except Exception as e:
            raise VaultxError from e

        # Update existing secret dict.
        patched_secret = current_secret_version["data"]["data"]
        patched_secret.update(secret)

        # Write back updated secret.
        return await self.create_or_update_secret(
            path=path,
            cas=current_secret_version["data"]["metadata"]["version"],
            secret=patched_secret,
            mount_point=mount_point,
        )

    async def delete_latest_version_of_secret(
        self, path: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Issue a soft delete of the secret's latest version at the specified location.

        This marks the version as deleted and will stop it from being returned from reads, but the underlying data will
        not be removed. Deletion can be undone using the undelete path.

        Supported methods:
            DELETE: /{mount_point}/data/{path}. Produces: 204 (empty body)

        :param path: Specifies the path of the secret to delete. This is specified as part of the URL.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/data/{path}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def delete_secret_versions(
        self, path: str, versions: list[int], mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Issue a soft delete of the specified versions of the secret.

        This marks the versions as deleted and will stop them from being returned from reads,
        but the underlying data will not be removed. Deletion can be undone using the
        undelete path.

        Supported methods:
            POST: /{mount_point}/delete/{path}. Produces: 204 (empty body)

        :param path: Specifies the path of the secret to delete. This is specified as part of the URL.
        :param versions: The versions to be deleted. The versioned data will not be deleted, but it will no longer be
            returned in normal get requests.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The response of the request.
        """
        if not isinstance(versions, list) or len(versions) == 0:
            error_msg = f"Error in parameter validation: argument to 'versions' \
                must be a list containing one or more integers, '{versions}' provided."
            raise exceptions.VaultxError(message=error_msg)
        params = {"versions": versions}
        api_path = f"/v1/{mount_point}/delete/{path}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def undelete_secret_versions(
        self, path: str, versions: list[int], mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Undelete the data for the provided version and path in the key-value store.

        This restores the data, allowing it to be returned on get requests.

        Supported methods:
            POST: /{mount_point}/undelete/{path}. Produces: 204 (empty body)

        :param path: Specifies the path of the secret to undelete. This is specified as part of the URL.
        :param versions: The versions to undelete. The versions will be restored and their data will be returned on
            normal get requests.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The response of the request.
        """
        if not isinstance(versions, list) or len(versions) == 0:
            error_msg = f"Error in parameter validation: argument to 'versions' \
                must be a list containing one or more integers, '{versions}' provided."
            raise exceptions.VaultxError(message=error_msg)
        params = {"versions": versions}
        api_path = f"/v1/{mount_point}/undelete/{path}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def destroy_secret_versions(
        self, path: str, versions: list[int], mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Permanently remove the specified version data and numbers for the provided path from the key-value store.

        Supported methods:
            POST: /{mount_point}/destroy/{path}. Produces: 204 (empty body)

        :param path: Specifies the path of the secret to destroy. This is specified as part of the URL.
        :param versions: The versions to destroy. Their data will be permanently deleted.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The response of the request.
        """
        if not isinstance(versions, list) or len(versions) == 0:
            error_msg = f"Error in parameter validation: argument to 'versions' \
                must be a list containing one or more integers, '{versions}' provided."
            raise exceptions.VaultxError(message=error_msg)
        params = {"versions": versions}
        api_path = f"/v1/{mount_point}/destroy/{path}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def list_secrets(self, path: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Return a list of key names at the specified location.

        Folders are suffixed with /. The input must be a folder; list on a file will not return a value. Note that no
        policy-based filtering is performed on keys; do not encode sensitive information in key names. The values
        themselves are not accessible via this command.

        Supported methods:
            LIST: /{mount_point}/metadata/{path}. Produces: 200 application/json

        :param path: Specifies the path of the secrets to list. This is specified as part of the URL.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/metadata/{path}"
        return await self._adapter.list(
            url=api_path,
        )

    async def read_secret_metadata(self, path: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Retrieve the metadata and versions for the secret at the specified path.

        Supported methods:
            GET: /{mount_point}/metadata/{path}. Produces: 200 application/json

        :param path: Specifies the path of the secret to read. This is specified as part of the URL.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/metadata/{path}"
        return await self._adapter.get(
            url=api_path,
        )

    async def update_metadata(
        self,
        path: str,
        max_versions: Optional[int] = None,
        cas_required: Optional[bool] = None,
        delete_version_after: str = "0s",
        mount_point: str = DEFAULT_MOUNT_POINT,
        custom_metadata: Optional[dict[Any, Any]] = None,
    ):
        """
        Update the max_versions of cas_required setting on an existing path.

        Supported methods:
            POST: /{mount_point}/metadata/{path}. Produces: 204 (empty body)

        :param path: Path
        :param max_versions: The number of versions to keep per key. If not set, the backend's configured max version is
            used. Once a key has more than the configured allowed versions the oldest version will be permanently
            deleted.
        :param cas_required: If true the key will require the cas parameter to be set on all write requests. If false,
            the backend's configuration will be used.
        :param delete_version_after: Specifies the length of time before a version is deleted.
            Defaults to "0s" (i.e., disabled).
        :param mount_point: The "path" the secret engine was mounted on.
        :param custom_metadata: A dictionary of key/value metadata to describe the secret.
            Requires Vault 1.9.0 or greater.
        :return: The response of the request.
        """
        params: dict[Any, Any] = {"delete_version_after": delete_version_after}
        if max_versions:
            params["max_versions"] = max_versions
        if cas_required:
            if not isinstance(cas_required, bool):
                error_msg = f"Error in parameter validation: \
                    bool expected for cas_required parameter, {type(cas_required)} received"
                raise exceptions.VaultxError(message=error_msg)
            params["cas_required"] = cas_required
        if custom_metadata:
            if not isinstance(custom_metadata, dict):
                error_msg = f"Error in parameter validation: \
                    dict expected for custom_metadata param, {type(custom_metadata)} received"
                raise exceptions.VaultxError(error_msg)
            params["custom_metadata"] = custom_metadata
        api_path = f"/v1/{mount_point}/metadata/{path}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def delete_metadata_and_all_versions(
        self, path: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Delete (permanently) the key metadata and all version data for the specified key.
        All version history will be removed.

        Supported methods:
            DELETE: /{mount_point}/metadata/{path}. Produces: 204 (empty body)

        :param path: Specifies the path of the secret to delete. This is specified as part of the URL.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/metadata/{path}"
        return await self._adapter.delete(
            url=api_path,
        )
