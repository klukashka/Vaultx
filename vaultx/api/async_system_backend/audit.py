from typing import Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


class Audit(AsyncVaultApiBase):
    async def list_enabled_audit_devices(self) -> VaultxResponse:
        """
        List enabled audit devices.

        It does not list all available audit devices.
        This endpoint requires sudo capability in addition to any path-specific capabilities.

        Supported methods:
            GET: /sys/audit. Produces: 200 application/json

        :return: VaultxResponse of the request.
        """
        return await self._adapter.get("/v1/sys/audit")

    async def enable_audit_device(
        self,
        device_type: str,
        description: Optional[str] = None,
        options: Optional[str] = None,
        path: Optional[str] = None,
        local: Optional[bool] = None,
    ) -> VaultxResponse:
        """
        Enable a new audit device at the supplied path.
        The path can be a single word name or a more complex, nested path.

        Supported methods:
            PUT: /sys/audit/{path}. Produces: 204 (empty body)

        :param device_type: Specifies the type of the audit device.
        :param description: Human-friendly description of the audit device.
        :param options: Configuration options to pass to the audit device itself. This is
            dependent on the audit device type.
        :param path: Specifies the path in which to enable the audit device. This is part of
            the request URL.
        :param local: Specifies if the audit device is a local only.
        :return: The response of the request.
        """

        if path is None:
            path = device_type

        params = {
            "type": device_type,
        }
        params.update(
            utils.remove_nones(
                {
                    "description": description,
                    "options": options,
                    "local": local,
                }
            )
        )

        api_path = f"/v1/sys/audit/{path}"
        return await self._adapter.post(url=api_path, json=params)

    async def disable_audit_device(self, path: str) -> VaultxResponse:
        """
        Disable the audit device at the given path.

        Supported methods:
            DELETE: /sys/audit/{path}. Produces: 204 (empty body)

        :param path: The path of the audit device to delete. This is part of the request URL.
        :return: The response of the request.
        """
        api_path = f"/v1/sys/audit/{path}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def calculate_hash(self, path: str, input_to_hash: str) -> VaultxResponse:
        """
        Hash the given input data with the specified audit device's hash function and salt.
        This endpoint can be used to discover whether a given plaintext string (the input parameter) appears in the
        audit log in obfuscated form.

        Supported methods:
            POST: /sys/audit-hash/{path}. Produces: 204 (empty body)

        :param path: The path of the audit device to generate hashes for. This is part of the request URL.
        :param input_to_hash: The input string to hash.
        :return: The VaultxResponse of the request.
        """
        params = {
            "input": input_to_hash,
        }

        api_path = f"/v1/sys/audit-hash/{path}"
        return await self._adapter.post(url=api_path, json=params)
