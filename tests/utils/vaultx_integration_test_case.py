import logging
import re
import shutil
import time
from typing import Any

from tests.utils import create_async_client, create_client, get_config_file_path, is_enterprise
from tests.utils.server_manager import AsyncServerManager, ServerManager
from vaultx import AsyncClient, Client


class VaultxIntegrationTestCase:
    """Base class intended to be used by sync vaultx integration test cases."""

    TEST_APPROLE_PATH: str
    manager: ServerManager
    client: Client
    enable_vault_ha: bool = False
    use_env: bool = False
    server_retry_count: int = 2  # num retries != total tries
    server_retry_delay_seconds: float = 0.1

    @classmethod
    def setUpClass(cls) -> None:
        """Use the ServerManager class to launch a vault server process."""
        config_paths = [get_config_file_path("vault-tls.hcl")]
        if shutil.which("consul") is None and cls.enable_vault_ha:
            logging.warning("Unable to run Vault in HA mode, consul binary not found in path.")
            cls.enable_vault_ha = False
        if is_enterprise():
            # TODO: figure out why this bit isn't working
            logging.warning("Unable to run Vault in HA mode, enterprise Vault version not currently supported.")
            cls.enable_vault_ha = False
        if cls.enable_vault_ha:
            config_paths = [
                get_config_file_path("vault-ha-node1.hcl"),
                get_config_file_path("vault-ha-node2.hcl"),
            ]
        cls.manager = ServerManager(config_paths=config_paths, use_consul=cls.enable_vault_ha, client=Client())
        while True:
            try:
                cls.manager.start()
                cls.manager.initialize()
                cls.manager.unseal()
            except Exception as e:
                cls.manager.stop()
                logging.debug(f"Failure in ServerManager (retries remaining: {cls.server_retry_count})\n{str(e)}")
                if cls.server_retry_count > 0:
                    cls.server_retry_count -= 1
                    time.sleep(cls.server_retry_delay_seconds)
                else:
                    raise
            else:
                break

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the vault server process at the conclusion of a test class."""
        if cls.manager:
            cls.manager.stop()

    def setUp(self) -> None:
        """Set the client attribute to an authenticated vaultx Client instance."""
        self.client = self.manager.client

    def tearDown(self) -> None:
        """
        Ensure the vaultx Client instance's root token is reset after any auth method tests that may have modified it.

        This allows subclass's to include additional tearDown logic to reset the state of the vault server when needed.
        """
        self.client.token = self.manager.root_token

    def prep_policy(self, name: str) -> tuple[str, dict]:
        """Add a common policy used by a subset of integration test cases."""

        text = """
        path "sys" {
            policy = "deny"
        }
            path "secret" {
        policy = "write"
        }
        """
        obj = {"path": {"sys": {"policy": "deny"}, "secret": {"policy": "write"}}}
        self.client.sys.create_or_update_policy(name, text)
        return text, obj

    def get_vault_addr_by_standby_status(self, standby_status: bool = True):  # noqa
        """
        Get an address for a Vault HA node currently in standby.

        :param standby_status: Value of the 'standby' key from the health status response to match.
        :return: Standby Vault address.
        """
        vault_addresses = self.manager.get_active_vault_addresses()
        for vault_address in vault_addresses:
            health_status = create_client(url=vault_address).sys.read_health_status(method="GET")
            if not isinstance(health_status, dict):
                health_status = health_status.json()
            if health_status["standby"] == standby_status:
                return vault_address

    def add_admin_approle_role(self, role_id: str, role_name: str = "test-admin-role", path: str = "approle") -> Any:
        test_admin_policy = {
            "path": {
                "*": {
                    "capabilities": [
                        "sudo",
                        "create",
                        "read",
                        "update",
                        "delete",
                        "list",
                    ],
                },
            },
        }
        test_admin_policy_name = "test-admin-approle-policy"
        self.client.sys.create_or_update_policy(
            name=test_admin_policy_name,
            policy=test_admin_policy,
        )
        self.client.auth.approle.create_or_update_approle(
            role_name=role_name,
            mount_point=path,
            token_policies=[test_admin_policy_name],
        )
        self.client.auth.approle.update_role_id(
            role_name=role_name,
            role_id=role_id,
            mount_point=path,
        )
        secret_id_resp = self.client.auth.approle.generate_secret_id(
            role_name=role_name,
            mount_point=self.TEST_APPROLE_PATH,
        )
        return secret_id_resp["data"]["secret_id"]

    def login_using_admin_approle_role(
        self, role_id: str, role_name: str = "test-admin-role", path: str = "approle"
    ) -> None:
        secret_id = self.add_admin_approle_role(role_id=role_id, role_name=role_name, path=path)

        self.client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id,
            mount_point=path,
        )


class AsyncVaultxIntegrationTestCase:
    """Base class intended to be used by async vaultx integration test cases."""

    TEST_APPROLE_PATH: str
    manager: AsyncServerManager
    client: AsyncClient
    enable_vault_ha: bool = False
    use_env: bool = False
    server_retry_count: int = 2  # num retries != total tries
    server_retry_delay_seconds: float = 0.1

    @classmethod
    def setUpClass(cls):
        config_paths = [get_config_file_path("vault-tls.hcl")]
        if shutil.which("consul") is None and cls.enable_vault_ha:
            logging.warning("Unable to run Vault in HA mode, consul binary not found in path.")
            cls.enable_vault_ha = False
        if is_enterprise():
            # TODO: figure out why this bit isn't working
            logging.warning("Unable to run Vault in HA mode, enterprise Vault version not currently supported.")
            cls.enable_vault_ha = False
        if cls.enable_vault_ha:
            config_paths = [
                get_config_file_path("vault-ha-node1.hcl"),
                get_config_file_path("vault-ha-node2.hcl"),
            ]
        cls.manager = AsyncServerManager(
            config_paths=config_paths,
            use_consul=cls.enable_vault_ha,
            client=Client(),
        )
        while True:
            try:
                cls.manager.start()
                cls.manager.initialize()
                cls.manager.unseal()
            except Exception as e:
                cls.manager.stop()
                logging.debug(f"Failure in ServerManager (retries remaining: {cls.server_retry_count})\n{str(e)}")
                if cls.server_retry_count > 0:
                    cls.server_retry_count -= 1
                    time.sleep(cls.server_retry_delay_seconds)
                else:
                    raise
            else:
                break

    @classmethod
    def tearDownClass(cls):
        if cls.manager:
            cls.manager.stop()

    async def asyncSetUp(self) -> None:
        self.client = await self.manager.make_client()

    async def asyncTearDown(self) -> None:
        """
        Ensure AsyncClient instance's root token is reset after any auth method tests that may have modified it.

        This allows subclass's to include additional tearDown logic to reset the state of the vault server when needed.
        """
        await self.client.close()

    async def prep_policy(self, name: str) -> tuple[str, dict]:
        """Add a common policy used by a subset of integration test cases."""

        text = """
        path "sys" {
            policy = "deny"
        }
            path "secret" {
        policy = "write"
        }
        """
        obj = {"path": {"sys": {"policy": "deny"}, "secret": {"policy": "write"}}}
        await self.client.sys.create_or_update_policy(name, text)
        return text, obj

    async def get_vault_addr_by_standby_status(self, standby_status: bool = True):  # noqa
        """
        Get an address for a Vault HA node currently in standby.

        :param standby_status: Value of the 'standby' key from the health status response to match.
        :return: Standby Vault address.
        """
        vault_addresses = self.manager.get_active_vault_addresses()
        for vault_address in vault_addresses:
            health_status = await (await create_async_client(url=vault_address)).sys.read_health_status(method="GET")
            if not isinstance(health_status, dict):
                health_status = health_status.json()
            if health_status["standby"] == standby_status:
                return vault_address

    async def add_admin_approle_role(
        self, role_id: str, role_name: str = "test-admin-role", path: str = "approle"
    ) -> Any:
        test_admin_policy = {
            "path": {
                "*": {
                    "capabilities": [
                        "sudo",
                        "create",
                        "read",
                        "update",
                        "delete",
                        "list",
                    ],
                },
            },
        }
        test_admin_policy_name = "test-admin-approle-policy"
        await self.client.sys.create_or_update_policy(
            name=test_admin_policy_name,
            policy=test_admin_policy,
        )
        await self.client.auth.approle.create_or_update_approle(
            role_name=role_name,
            mount_point=path,
            token_policies=[test_admin_policy_name],
        )
        await self.client.auth.approle.update_role_id(
            role_name=role_name,
            role_id=role_id,
            mount_point=path,
        )
        secret_id_resp = await self.client.auth.approle.generate_secret_id(
            role_name=role_name,
            mount_point=self.TEST_APPROLE_PATH,
        )
        return secret_id_resp["data"]["secret_id"]

    async def login_using_admin_approle_role(
        self, role_id: str, role_name: str = "test-admin-role", path: str = "approle"
    ) -> None:
        secret_id = await self.add_admin_approle_role(role_id=role_id, role_name=role_name, path=path)

        await self.client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id,
            mount_point=path,
        )


def convert_python_ttl_value_to_expected_vault_response(ttl_value: str) -> int:
    """Convert any acceptable Vault TTL *input* to the expected value that Vault would return.

    Vault accepts TTL values in the form r'^(?P<duration>[0-9]+)(?P<unit>[smh])?$ (number of seconds/minutes/hours).
        However, it returns those values as integers corresponding to seconds when retrieving configuration.
        This method converts the "go duration format" arguments Vault accepts into the number (integer) of seconds
        corresponding to what Vault returns.

    :param ttl_value: A TTL string accepted by vault; number of seconds/minutes/hours
    :return: The provided TTL value in the form returned by the Vault API.
    """
    expected_ttl = 0
    if not isinstance(ttl_value, int) and ttl_value != "":
        regexp_matches = re.findall(r"(?P<duration>[0-9]+)(?P<unit>[smh])", ttl_value)
        if regexp_matches:
            for regexp_match in regexp_matches:
                duration, unit = regexp_match
                if unit == "m":
                    # convert minutes to seconds
                    expected_ttl += int(duration) * 60
                elif unit == "h":
                    # convert hours to seconds
                    expected_ttl += int(duration) * 60 * 60
                else:
                    expected_ttl += int(duration)

    elif ttl_value == "":
        expected_ttl = 0
    return expected_ttl
