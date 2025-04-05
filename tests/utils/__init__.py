import base64
import json
import logging
import operator
import os
import re
import socket
import ssl
import subprocess
import typing as tp
from contextlib import suppress
from shutil import which
from typing import Optional, Union
from unittest import SkipTest, mock

import httpx
from aiohttp import ClientSession, TCPConnector
from packaging.version import Version

from vaultx import AsyncClient, Client
from vaultx.adapters import AiohttpTransport


logger = logging.getLogger(__name__)

VERSION_REGEX = re.compile(r"Vault v([0-9.]+)")
LATEST_VAULT_VERSION = "1.1.3"


def get_vault_version_string() -> str:
    if not which("vault"):
        raise SkipTest("Vault executable not found")
    command = ["vault", "-version"]
    process = subprocess.Popen(**get_popen_kwargs(args=command, stdout=subprocess.PIPE))
    output, _ = process.communicate()
    return output.strip().split()[1].lstrip("v")


def get_installed_vault_version() -> str:
    version_string = get_vault_version_string()
    # replace any '-beta1' type substrings with a StrictVersion parsable version. E.g., 1.0.0-beta1 => 1.0.0b1
    version = version_string.replace("-", "").replace("beta", "b")
    return version.replace("+ent", "")


def is_enterprise() -> bool:
    version_string = get_vault_version_string()
    return re.search(r"\+ent$", version_string) is not None


def if_vault_version(supported_version, comparison=operator.lt) -> bool:
    current_version = get_installed_vault_version()
    return comparison(Version(current_version), Version(supported_version))


def vault_version_lt(supported_version) -> bool:
    return if_vault_version(supported_version, comparison=operator.lt)


def vault_version_ge(supported_version) -> bool:
    return if_vault_version(supported_version, comparison=operator.ge)


def vault_version_eq(supported_version) -> bool:
    return if_vault_version(supported_version, comparison=operator.eq)


def get_generate_root_otp() -> str:
    """
    Get an appropriate OTP for the current Vault version under test.

    :return: OTP to use in generate root operations
    """
    if vault_version_ge("1.10.0"):
        test_otp = "BMjzW3wAsEzINXCM05Wbas3u9zSl"
    elif vault_version_ge("1.0.0"):
        test_otp = "ygs0vL8GIxu0AjRVEmJ5jLCVq8"
    else:
        test_otp = "RSMGkAqBH5WnVLrDTbZ+UQ=="
    return test_otp


def create_client(url: str, use_env: bool = False, **kwargs) -> Client:
    """
    Small helper to instantiate a :py:class:`vaultx.Client` class with the appropriate parameters for the test env.

    :param url: Vault address to configure the client with.
    :param use_env: configure vault using environment variable
    :param kwargs: Dictionary of additional keyword arguments to pass through to the Client instance being created.
    :return: Instantiated :py:class:`vaultx.Client` class.
    """

    client_cert_path = get_config_file_path("client-cert.pem")
    client_key_path = get_config_file_path("client-key.pem")
    server_cert_path = get_config_file_path("server-cert.pem")
    if use_env:
        with (
            mock.patch("vaultx.VAULT_CAPATH", server_cert_path),
            mock.patch("vaultx.VAULT_CLIENT_CERT", client_cert_path),
            mock.patch("vaultx.VAULT_CLIENT_KEY", client_key_path),
        ):
            client = Client(
                url=url,
                **kwargs,
            )
    else:
        # Make sure self-signed certificates for testing will be accepted

        verify_param = ssl.create_default_context(cafile=server_cert_path)
        verify_param.load_cert_chain(client_cert_path, client_key_path)  # do this instead of adding cert param

        transport = httpx.HTTPTransport(
            retries=3,
            verify=verify_param,
        )

        mounts = {"http://": transport, "https://": transport}
        httpx_client = httpx.Client(
            mounts=mounts,
            verify=verify_param,
        )

        client = Client(
            url=url,
            verify=verify_param,
            client=httpx_client,
            **kwargs,
        )
    return client


async def create_async_client(url: str, use_env: bool = False, **kwargs) -> AsyncClient:
    """
    Small helper to instantiate a :py:class:`vaultx.AsyncClient` class with the appropriate parameters for the test env.

    :param url: Vault address to configure the client with.
    :param use_env: configure vault using environment variable
    :param kwargs: Dictionary of additional keyword arguments to pass through to the AsyncClient instance being created.
    :return: Instantiated :py:class:`vaultx.AsyncClient` class.
    """

    client_cert_path = get_config_file_path("client-cert.pem")
    client_key_path = get_config_file_path("client-key.pem")
    server_cert_path = get_config_file_path("server-cert.pem")
    if use_env:
        with (
            mock.patch("vaultx.VAULT_CAPATH", server_cert_path),
            mock.patch("vaultx.VAULT_CLIENT_CERT", client_cert_path),
            mock.patch("vaultx.VAULT_CLIENT_KEY", client_key_path),
        ):
            client = AsyncClient(
                url=url,
                **kwargs,
            )
    else:
        # Make sure self-signed certificates for testing will be accepted

        verify_param = ssl.create_default_context(cafile=server_cert_path)
        verify_param.load_cert_chain(client_cert_path, client_key_path)  # do this instead of adding cert param

        aiohttp_session = ClientSession(connector=TCPConnector(ssl=verify_param))

        transport = AiohttpTransport(session=aiohttp_session)

        mounts = {"http://": transport, "https://": transport}
        httpx_client = httpx.AsyncClient(
            mounts=mounts,
            verify=verify_param,
        )

        client = AsyncClient(
            url=url,
            verify=verify_param,
            client=httpx_client,
            **kwargs,
        )
    return client


class PortGetter:
    _entered: bool = False
    _sockets: list[socket.socket] = []

    def __init__(self, default_address: str = "localhost") -> None:
        self._default_addr = default_address

    class PortGetterProtocol(tp.Protocol):
        def __call__(
            self,
            *,
            address: Optional[str] = None,
            port: Optional[int] = None,
            proto: socket.SocketKind = socket.SOCK_STREAM,
        ) -> tuple[str, int]:
            raise NotImplementedError()

    def get_port(
        self,
        *,
        address: Optional[str] = None,
        port: Optional[int] = None,
        proto: socket.SocketKind = socket.SOCK_STREAM,
    ) -> tuple[str, int]:
        if not self._entered:
            raise RuntimeError("Enter the context manager before calling get_port.")

        if address is None:
            address = self._default_addr

        s = socket.socket(socket.AF_INET, type=proto)

        if port is not None:
            try:
                s.bind((address, port))
            except OSError:
                s.bind((address, 0))
        else:
            s.bind((address, 0))

        self._sockets.append(s)
        return s.getsockname()

    def __enter__(self):
        if self._entered:
            raise RuntimeError(
                "This context manager can only be entered once at a time. Exit first or use a new instance."
            )
        self._entered = True
        self._sockets.clear()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        for sock in self._sockets:
            with suppress(Exception):
                sock.close()
        self._sockets.clear()
        self._entered = False


def get_free_port() -> int:
    # TODO: deprecated: remove in favor of port getter class once LDAP mock is refactored
    """
    Small helper method used to discover an open port to use by mock API HTTP servers.

    :return: An available port number.
    """
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    address, port = s.getsockname()
    s.close()
    return port


def load_config_file(filename: str) -> str:
    """
    Load test config file data for use by various test cases.

    :param filename: Name of the test data file.
    :return: Test data contents
    """
    test_data_path = get_config_file_path(filename)
    with open(test_data_path) as f:
        return f.read()


def get_config_file_path(*components: str) -> str:
    """
    Get the path to a config file under the "tests/config_files" directory.

    I.e., the directory containing self-signed certificates, configuration files, etc. that are used for various tests.

    :param components: One or more path components, the last of which is usually the name of the test data file.
    :return: The absolute path to the test data directory.
    """
    # Use __file__ to derive a path relative to this module's location which points to the tests data directory.
    relative_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config_files")
    return os.path.join(os.path.abspath(relative_path), *components)


def decode_generated_root_token(encoded_token: str, otp: str, url: str) -> str:
    """
    Decode a newly generated root token via Vault CLI.

    :param encoded_token: The token to decode.
    :param otp: OTP code to use when decoding the token.
    :param url:
    :return: The decoded root token.
    """
    command = ["vault"]
    if vault_version_ge("0.9.6"):
        # before Vault ~0.9.6, the generate-root command was the first positional argument
        # afterwards, it was moved under the "operator" category
        command.append("operator")

    command.extend(
        [
            "generate-root",
            "-address",
            url,
            "-tls-skip-verify",
            "-decode",
            encoded_token,
            "-otp",
            otp,
        ]
    )
    process = subprocess.Popen(**get_popen_kwargs(args=command, stdout=subprocess.PIPE, stderr=subprocess.PIPE))

    stdout, stderr = process.communicate()
    logging.debug('decode_generated_root_token stdout: "%s"' % str(stdout))
    if stderr != "":
        logging.error("decode_generated_root_token stderr: %s" % stderr)

    try:
        # On the off chance VAULT_FORMAT=json or such is set in the test environment:
        new_token = json.loads(stdout)["token"]
    except ValueError:
        new_token = stdout.replace("Root token:", "")
    return new_token.strip()


def get_popen_kwargs(**popen_kwargs) -> dict:
    """
    Helper method to add `encoding='utf-8'` to subprocess.Popen.

    :param popen_kwargs: List of keyword arguments to mutate on condition
    :return: Conditionally, updated list of keyword arguments
    """
    popen_kwargs["encoding"] = "utf-8"
    return popen_kwargs


def base64ify(bytes_or_str: Union[bytes, str]) -> str:
    """
    Helper method to perform base64 encoding

    :param bytes_or_str:
    :return:
    """

    input_bytes = bytes_or_str.encode("utf8") if isinstance(bytes_or_str, str) else bytes_or_str

    output_bytes = base64.urlsafe_b64encode(input_bytes)
    return output_bytes.decode("ascii")


def configure_pki(
    client: Client, common_name: str = "vaultx.com", role_name: str = "my-role", mount_point: str = "pki"
) -> None:
    """
    Helper function to configure a pki backend for integration tests that need to work with lease IDs.

    :param client: Authenticated vaultx Client instance.
    :param common_name: Common name to configure in the pki backend
    :param role_name: Name of the test role to configure.
    :param mount_point: The path the pki backend is mounted under.
    :return: Nothing.
    """
    if f"{mount_point}/" in client.sys.list_mounted_secrets_engines():
        client.sys.disable_secrets_engine(mount_point)

    client.sys.enable_secrets_engine(backend_type="pki", path=mount_point)

    client.write(
        path=f"{mount_point}/root/generate/internal",
        data={
            "common_name": common_name,
            "ttl": "8760h",
        },
    )
    client.write(
        path=f"{mount_point}/config/urls",
        data={
            "issuing_certificates": "http://127.0.0.1:8200/v1/pki/ca",
            "crl_distribution_points": "http://127.0.0.1:8200/v1/pki/crl",
        },
    )
    client.write(
        path=f"{mount_point}/roles/{role_name}",
        data={
            "allowed_domains": common_name,
            "allow_subdomains": True,
            "generate_lease": True,
            "max_ttl": "72h",
        },
    )


async def async_configure_pki(
    client: AsyncClient, common_name: str = "vaultx.com", role_name: str = "my-role", mount_point: str = "pki"
) -> None:
    """
    Helper function to configure a pki backend for integration tests that need to work with lease IDs.

    :param client: Authenticated vaultx Client instance.
    :param common_name: Common name to configure in the pki backend
    :param role_name: Name of the test role to configure.
    :param mount_point: The path the pki backend is mounted under.
    :return: Nothing.
    """
    if f"{mount_point}/" in await client.sys.list_mounted_secrets_engines():
        await client.sys.disable_secrets_engine(mount_point)

    await client.sys.enable_secrets_engine(backend_type="pki", path=mount_point)

    await client.write(
        path=f"{mount_point}/root/generate/internal",
        data={
            "common_name": common_name,
            "ttl": "8760h",
        },
    )
    await client.write(
        path=f"{mount_point}/config/urls",
        data={
            "issuing_certificates": "http://127.0.0.1:8200/v1/pki/ca",
            "crl_distribution_points": "http://127.0.0.1:8200/v1/pki/crl",
        },
    )
    await client.write(
        path=f"{mount_point}/roles/{role_name}",
        data={
            "allowed_domains": common_name,
            "allow_subdomains": True,
            "generate_lease": True,
            "max_ttl": "72h",
        },
    )


def disable_pki(client: Client, mount_point: str = "pki") -> None:
    """
    Disable a previously configured pki backend.

    :param client: Authenticated vaultx Client instance.
    :param mount_point: The path the pki backend is mounted under.
    """
    client.sys.disable_secrets_engine(mount_point)


async def async_disable_pki(client: AsyncClient, mount_point: str = "pki") -> None:
    """
    Disable a previously configured pki backend.

    :param client: Authenticated vaultx AsyncClient instance.
    :param mount_point: The path the pki backend is mounted under.
    """
    await client.sys.disable_secrets_engine(mount_point)
