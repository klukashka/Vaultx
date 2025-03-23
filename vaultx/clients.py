import abc
import importlib
import os
import ssl
import types
import typing as tp
from typing import Any, Optional, Union

import httpx

from vaultx import _types, adapters, api, exceptions
from vaultx.adapters import VaultxResponse
from vaultx.constants.client import (
    DEFAULT_URL,
    VAULT_CACERT,
    VAULT_CAPATH,
    VAULT_CLIENT_CERT,
    VAULT_CLIENT_KEY,
)
from vaultx.utils import get_token_from_env


try:
    hcl = importlib.import_module("hcl")

    has_hcl_parser = True
except ImportError:
    has_hcl_parser = False


class MetaClient(metaclass=abc.ABCMeta):
    """Vaultx abstract client interface"""

    @abc.abstractmethod
    def __init__(
        self,
        url: Optional[str] = None,
        token: Optional[str] = None,
        cert: Optional[_types.CertTypes] = None,
        verify: Union[ssl.SSLContext, str, bool] = True,
        timeout: int = 30,
        proxy: Optional[str] = None,
        follow_redirects: bool = True,
        client: Optional[Union[httpx.Client, httpx.AsyncClient]] = None,
        adapter: Optional[Union[adapters.Adapter, adapters.AsyncAdapter]] = None,
        namespace: Optional[str] = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError()

    def __getattr__(self, item: object):
        raise AttributeError(f'"{self.__class__.__name__}" has no attribute "{item}"')

    @property
    @abc.abstractmethod
    def adapter(self):
        raise NotImplementedError()

    @adapter.setter
    @abc.abstractmethod
    def adapter(self, adapter):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def url(self) -> str:
        raise NotImplementedError()

    @url.setter
    @abc.abstractmethod
    def url(self, url):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def token(self):
        raise NotImplementedError()

    @token.setter
    @abc.abstractmethod
    def token(self, token):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def client(self):
        raise NotImplementedError()

    @client.setter
    @abc.abstractmethod
    def client(self, client):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def follow_redirects(self) -> bool:
        raise NotImplementedError()

    @follow_redirects.setter
    @abc.abstractmethod
    def follow_redirects(self, follow_redirects) -> None:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def auth(self):
        """Accessor for the Client instance's auth methods."""
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def secrets(self):
        """Accessor for the Client instance's secrets engines."""
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def sys(self):
        """Accessor for the Client instance's system backend methods."""
        raise NotImplementedError()


@exceptions.handle_unknown_exception
class Client(MetaClient):
    """Vaultx synchronous client"""

    def __init__(
        self,
        url: Optional[str] = None,
        token: Optional[str] = None,
        cert: Optional[_types.CertTypes] = None,
        verify: Union[ssl.SSLContext, str, bool] = True,
        timeout: int = 30,
        proxy: Optional[str] = None,
        follow_redirects: bool = True,
        client: Optional[httpx.Client] = None,
        adapter: tp.Type[adapters.Adapter] = adapters.VaultxAdapter,
        namespace: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Create a new vaultx client instance.

        :param url: Base URL for the Vault instance being addressed.
        :param token: Authentication token to include in requests sent to Vault.
        :param cert: Certificates for use in requests sent to the Vault instance. This should be a tuple with the
            certificate and then key.
        :param verify: Either a boolean to indicate whether TLS verification should be performed
            when sending requests to Vault, or a string pointing at the CA bundle to use for verification.
            See https://www.python-httpx.org/advanced/ssl/
        :param timeout: The timeout value for requests sent to Vault.
        :param proxy: Proxies to use when preforming requests.
            See: https://www.python-httpx.org/advanced/proxies/
        :param follow_redirects: Whether to follow redirects when sending requests to Vault.
        :param client: Optional client object to use when performing request.
        :param adapter: Optional class to be used for performing requests.
        :param kwargs: Additional parameters to pass to the adapter constructor.
        :param namespace: Optional Vault Namespace.
        """

        token = token if token else get_token_from_env()
        url = url if url else os.getenv("VAULT_ADDR", DEFAULT_URL)

        if cert is None and VAULT_CLIENT_CERT and VAULT_CLIENT_KEY:
            cert = (
                VAULT_CLIENT_CERT,
                VAULT_CLIENT_KEY,
            )

        # Consider related CA env vars _only if_ no argument is passed in under the
        # `verify` parameter.
        if verify is None:
            # Reference: https://www.vaultproject.io/docs/commands#vault_cacert
            # Note: "[VAULT_CACERT] takes precedence over VAULT_CAPATH." and thus we check for VAULT_CAPATH _first_.
            if VAULT_CAPATH:
                verify = VAULT_CAPATH
            if VAULT_CACERT:
                verify = VAULT_CACERT
            if not verify:
                # default to verifying certificates if the above aren't defined
                verify = True

        self._adapter = adapter(
            base_uri=url,
            token=token,
            cert=cert,
            verify=verify,
            timeout=timeout,
            proxy=proxy,
            follow_redirects=follow_redirects,
            client=client,
            namespace=namespace,
            **kwargs,
        )

        # Instantiate API classes to be exposed as properties on this class starting with auth method classes.
        self._auth = api.AuthMethods(adapter=self._adapter)
        self._secrets = api.SecretsEngines(adapter=self._adapter)
        self._sys = api.SystemBackend(adapter=self._adapter)

    @exceptions.handle_unknown_exception
    def __enter__(self: "Client") -> "Client":
        self._adapter.__enter__()
        return self

    @exceptions.handle_unknown_exception
    def __exit__(
        self,
        exc_type: Optional[type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[types.TracebackType] = None,
    ) -> None:
        self._adapter.__exit__(exc_type, exc_value, traceback)

    @exceptions.handle_unknown_exception
    def close(self) -> None:
        self._adapter.close()

    @property
    def adapter(self) -> adapters.Adapter:
        """Adapter for all client's connections."""
        return self._adapter

    @adapter.setter
    def adapter(self, adapter: adapters.Adapter) -> None:
        self._adapter = adapter
        self._auth.adapter = adapter
        self._secrets.adapter = adapter
        self._sys.adapter = adapter

    @property
    def url(self) -> str:
        return self._adapter.base_uri

    @url.setter
    def url(self, url) -> None:
        self._adapter.base_uri = url

    @property
    def token(self) -> Optional[str]:
        return self._adapter.token

    @token.setter
    def token(self, token) -> None:
        self._adapter.token = token

    @property
    def client(self):
        return self._adapter.client

    @client.setter
    def client(self, client) -> None:
        self._adapter.client = client

    @property
    def follow_redirects(self) -> bool:
        return self._adapter.follow_redirects

    @follow_redirects.setter
    def follow_redirects(self, follow_redirects) -> None:
        self._adapter.follow_redirects = follow_redirects

    @property
    def auth(self) -> api.AuthMethods:
        """
        Accessor for the Client instance's auth methods. Provided via the :py:class:`vaultx.api.AuthMethods` class.
        :return: This Client instance's associated Auth instance.
        """
        return self._auth

    @property
    def secrets(self) -> api.SecretsEngines:
        """
        Accessor for the Client instance's secrets engines.
            Provided via the :py:class:`vaultx.api.SecretsEngines` class.
        :return: This Client instance's associated SecretsEngines instance.
        """
        return self._secrets

    @property
    def sys(self) -> api.SystemBackend:
        """
        Accessor for the Client instance's system backend methods.
        :return: This Client instance's associated SystemBackend instance.
        """
        return self._sys

    @property
    def generate_root_status(self) -> VaultxResponse:
        return self.sys.read_root_generation_progress()

    @property
    def key_status(self) -> Any:
        """
        GET /sys/key-status
        :return: Information about the current encryption key used by Vault.
        """
        response = self.sys.get_encryption_key_status()
        return response.value["data"]

    @property
    def rekey_status(self) -> VaultxResponse:
        return self.sys.read_rekey_progress()

    @property
    def ha_status(self) -> VaultxResponse:
        """
        Read the high availability status and current leader instance of Vault.

        :return: The VaultxResponse returned by read_leader_status()
        """
        return self.sys.read_leader_status()

    @property
    def seal_status(self) -> VaultxResponse:
        """
        Read the seal status of the Vault.
        This is an unauthenticated endpoint.

        Supported methods:
            GET: /sys/seal-status. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        return self.sys.read_seal_status()

    def read(self, path: str, wrap_ttl: Optional[Union[str, int]] = None) -> Optional[VaultxResponse]:
        """
        GET /<path>

        :return: The VaultxResponse of the request
        """
        try:
            return self._adapter.get(f"/v1/{path}", wrap_ttl=wrap_ttl)
        except exceptions.HTTPError as e:
            if e.status_code == 404:
                return None
            raise

    def list(self, path: str):
        """GET /<path>?list=true"""
        try:
            payload = {"list": True}
            return self._adapter.get(f"/v1/{path}", params=payload)
        except exceptions.HTTPError as e:
            if e.status_code == 404:
                return None

    def write(
        self,
        path: str,
        *,
        data: Optional[dict[str, Any]] = None,
        wrap_ttl: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Write data to a path.

        Supported methods:
            POST /<path>

        :param path:
        :param data:
        :param wrap_ttl:
        """
        return self._adapter.post(f"/v1/{path}", json=data, wrap_ttl=wrap_ttl)

    def delete(self, path: str) -> None:
        """
        DELETE /<path>

        :param path:
        :return:
        """
        self._adapter.delete(f"/v1/{path}")

    def get_policy(self, name: str, parse: bool = False) -> Optional[Union[str, dict[Any, Any]]]:
        """
        Retrieve the policy body for the named policy.

        :param name: The name of the policy to retrieve.
        :param parse: Specifies whether to parse the policy body using pyhcl or not.
        :return: The (optionally parsed) policy body for the specified policy.
        """
        policy = None
        try:
            response = self.sys.read_policy(name=name)
            if isinstance(response, dict):
                return response["data"]["rules"]
            raise exceptions.VaultxError('Non-dict response in "get_policy" method')
        except exceptions.HTTPError as e:
            if e.status_code == 404:
                return None

        if parse:
            if not has_hcl_parser:
                raise ImportError("pyhcl is required for policy parsing")
            policy = hcl.loads(policy)

        return policy

    def lookup_token(
        self, token: Optional[str] = None, accessor: bool = False, wrap_ttl: Optional[int] = None
    ) -> VaultxResponse:
        """
        GET /auth/token/lookup/<token>
        GET /auth/token/lookup-accessor/<token-accessor>
        GET /auth/token/lookup-self

        :param token:
        :param accessor:
        :param wrap_ttl:
        """
        token_param = {
            "token": token,
        }
        accessor_param = {
            "accessor": token,
        }
        if token:
            if accessor:
                path = "/v1/auth/token/lookup-accessor"
                return self._adapter.post(path, json=accessor_param, wrap_ttl=wrap_ttl)
            path = "/v1/auth/token/lookup"
            return self._adapter.post(path, json=token_param)
        path = "/v1/auth/token/lookup-self"
        return self._adapter.get(path, wrap_ttl=wrap_ttl)

    def revoke_token(self, token: str, orphan: bool = False, accessor: bool = False) -> None:
        """
        POST /auth/token/revoke
        POST /auth/token/revoke-orphan
        POST /auth/token/revoke-accessor

        :param token:
        :param orphan:
        :param accessor:
        :return:
        :rtype:
        """
        if accessor and orphan:
            msg = "revoke_token does not support 'orphan' and 'accessor' flags together"
            raise exceptions.VaultxError(msg)
        if accessor:
            params = {"accessor": token}
            self._adapter.post("/v1/auth/token/revoke-accessor", json=params)
        elif orphan:
            params = {"token": token}
            self._adapter.post("/v1/auth/token/revoke-orphan", json=params)
        else:
            params = {"token": token}
            self._adapter.post("/v1/auth/token/revoke", json=params)

    def renew_token(self, token, increment=None, wrap_ttl=None):
        """
        POST /auth/token/renew
        POST /auth/token/renew-self

        :param token:
        :param increment:
        :param wrap_ttl:

        For calls expecting to hit the renew-self endpoint please use the "renew_self" method
            on "vaultx_client.auth.token" instead
        """
        params = {"increment": increment, "token": token}

        return self._adapter.post("/v1/auth/token/renew", json=params, wrap_ttl=wrap_ttl)

    def logout(self, revoke_token: bool = False) -> None:
        """
        Clear the token used for authentication, optionally revoking it before doing so.

        :param revoke_token:
        :return:
        """
        if revoke_token:
            self.auth.token.revoke_self()
        self.token = None

    def is_authenticated(self) -> bool:
        """Helper method which returns the authentication status of the client"""
        if not self.token:
            return False

        try:
            self.lookup_token()
            return True
        except exceptions.VaultxError:
            return False

    def auth_cubbyhole(self, token: str) -> VaultxResponse:
        """
        Perform a login request with a wrapped token.
        Stores the unwrapped token in the resulting Vault response for use by the :py:meth:`vaultx.adapters.Adapter`
            instance under the _adapter Client attribute.

        :param token: Wrapped token
        :return: The (JSON decoded) response of the auth request
        """
        self.token = token
        return self.login("/v1/sys/wrapping/unwrap")

    def login(self, url: str, use_token: bool = True, **kwargs: Optional[dict[Any, Any]]) -> VaultxResponse:
        """
        Perform a login request.
        Associated request is typically to a path prefixed with "/v1/auth" and optionally stores the client token sent
            in the resulting Vault response for use by the :py:meth:`vaultx.adapters.Adapter` instance
            under the _adapter Client attribute.
        :param url: Path to send the authentication request to.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the Adapter instance under the _adapter Client attribute.
        :param kwargs: Additional keyword arguments to include in the params sent with the request.
        :return: The response of the auth request.
        """
        return self._adapter.login(url=url, use_token=use_token, **kwargs)


@exceptions.handle_unknown_exception
class AsyncClient(MetaClient):
    """Vaultx asynchronous client"""

    def __init__(
        self,
        url: Optional[str] = None,
        token: Optional[str] = None,
        cert: Optional[_types.CertTypes] = None,
        verify: Union[ssl.SSLContext, str, bool] = True,
        timeout: int = 30,
        proxy: Optional[str] = None,
        follow_redirects: bool = True,
        client: Optional[httpx.AsyncClient] = None,
        adapter: tp.Type[adapters.AsyncAdapter] = adapters.AsyncVaultxAdapter,
        namespace: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Create a new vaultx async client instance.

        :param url: Base URL for the Vault instance being addressed.
        :param token: Authentication token to include in requests sent to Vault.
        :param cert: Certificates for use in requests sent to the Vault instance. This should be a tuple with the
            certificate and then key.
        :param verify: Either a boolean to indicate whether TLS verification should be performed
            when sending requests to Vault, or a string pointing at the CA bundle to use for verification.
            See https://www.python-httpx.org/advanced/ssl/
        :param timeout: The timeout value for requests sent to Vault.
        :param proxy: Proxies to use when preforming requests.
            See: https://www.python-httpx.org/advanced/proxies/
        :param follow_redirects: Whether to follow redirects when sending requests to Vault.
        :param client: Optional async client object to use when performing request.
        :param adapter: Optional class to be used for performing requests.
        :param kwargs: Additional parameters to pass to the adapter constructor.
        :param namespace: Optional Vault Namespace.
        """

        token = token if token else get_token_from_env()
        url = url if url else os.getenv("VAULT_ADDR", DEFAULT_URL)

        if cert is None and VAULT_CLIENT_CERT and VAULT_CLIENT_KEY:
            cert = (
                VAULT_CLIENT_CERT,
                VAULT_CLIENT_KEY,
            )

        # Consider related CA env vars _only if_ no argument is passed in under the `verify` parameter.
        if verify is None:
            # Reference: https://www.vaultproject.io/docs/commands#vault_cacert
            # Note: "[VAULT_CACERT] takes precedence over VAULT_CAPATH." and thus we check for VAULT_CAPATH _first_.
            if VAULT_CAPATH:
                verify = VAULT_CAPATH
            if VAULT_CACERT:
                verify = VAULT_CACERT
            if not verify:
                # default to verifying certificates if the above aren't defined
                verify = True

        self._adapter = adapter(
            base_uri=url,
            token=token,
            cert=cert,
            verify=verify,
            timeout=timeout,
            proxy=proxy,
            follow_redirects=follow_redirects,
            client=client,
            namespace=namespace,
            **kwargs,
        )

        # Instantiate API classes to be exposed as properties on this class starting with auth method classes.
        self._auth = api.AsyncAuthMethods(adapter=self._adapter)
        self._secrets = api.AsyncSecretsEngines(adapter=self._adapter)
        self._sys = api.AsyncSystemBackend(adapter=self._adapter)

    @exceptions.handle_unknown_exception
    async def __aenter__(self: "AsyncClient") -> "AsyncClient":
        await self._adapter.__aenter__()
        return self

    @exceptions.handle_unknown_exception
    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[types.TracebackType] = None,
    ) -> None:
        await self._adapter.__aexit__(exc_type, exc_value, traceback)

    @exceptions.handle_unknown_exception
    async def close(self) -> None:
        await self._adapter.close()

    @property
    def adapter(self) -> adapters.AsyncAdapter:
        """AsyncAdapter for all client's connections."""
        return self._adapter

    @adapter.setter
    def adapter(self, adapter: adapters.AsyncAdapter) -> None:
        self._adapter = adapter
        self._auth.adapter = adapter
        self._secrets.adapter = adapter
        self._sys.adapter = adapter

    @property
    def url(self) -> str:
        return self._adapter.base_uri

    @url.setter
    def url(self, url) -> None:
        self._adapter.base_uri = url

    @property
    def token(self) -> Optional[str]:
        return self._adapter.token

    @token.setter
    def token(self, token) -> None:
        self._adapter.token = token

    @property
    def client(self):
        return self._adapter.client

    @client.setter
    def client(self, client) -> None:
        self._adapter.client = client

    @property
    def follow_redirects(self) -> bool:
        return self._adapter.follow_redirects

    @follow_redirects.setter
    def follow_redirects(self, follow_redirects) -> None:
        self._adapter.follow_redirects = follow_redirects

    @property
    def auth(self) -> api.AsyncAuthMethods:
        """
        Accessor for the AsyncClient instance's auth methods.
            Provided via the :py:class:`vaultx.api.AsyncAuthMethods` class.
        :return: This AsyncClient instance's associated AsyncAuth instance.
        """
        return self._auth

    @property
    def secrets(self) -> api.AsyncSecretsEngines:
        """
        Accessor for the AsyncClient instance's secrets engines.
            Provided via the :py:class:`vaultx.api.AsyncSecretsEngines` class.
        :return: This AsyncClient instance's associated AsyncSecretsEngines instance.
        """
        return self._secrets

    @property
    def sys(self) -> api.AsyncSystemBackend:
        """
        Accessor for the AsyncClient instance's async system backend methods.
        :return: This AsyncClient instance's associated AsyncSystemBackend instance.
        """
        return self._sys

    @property
    async def generate_root_status(self) -> VaultxResponse:
        return await self.sys.read_root_generation_progress()

    @property
    async def key_status(self) -> Any:
        """
        GET /sys/key-status
        :return: Information about the current encryption key used by Vault.
        """
        response = await self.sys.get_encryption_key_status()
        if isinstance(response, dict):
            return response["data"]
        raise exceptions.VaultxError('Non-dict response in "key_status" method')

    @property
    async def rekey_status(self) -> VaultxResponse:
        return await self.sys.read_rekey_progress()

    @property
    async def ha_status(self) -> VaultxResponse:
        """
        Read the high availability status and current leader instance of Vault.

        :return: The VaultxResponse returned by read_leader_status()
        """
        return await self.sys.read_leader_status()

    @property
    async def seal_status(self) -> VaultxResponse:
        """
        Read the seal status of the Vault.
        This is an unauthenticated endpoint.

        Supported methods:
            GET: /sys/seal-status. Produces: 200 application/json

        :return: The VaultxResponse of the request.
        """
        return await self.sys.read_seal_status()

    async def read(self, path: str, wrap_ttl: Optional[Union[str, int]] = None) -> Optional[VaultxResponse]:
        """
        GET /<path>

        :return: The VaultxResponse of the request
        """
        try:
            return await self._adapter.get(f"/v1/{path}", wrap_ttl=wrap_ttl)
        except exceptions.HTTPError as e:
            if e.status_code == 404:
                return None
            raise

    async def list(self, path: str):
        """GET /<path>?list=true"""
        try:
            payload = {"list": True}
            return await self._adapter.get(f"/v1/{path}", params=payload)
        except exceptions.HTTPError as e:
            if e.status_code == 404:
                return None

    async def write(
        self,
        path: str,
        *,
        data: Optional[dict[str, Any]] = None,
        wrap_ttl: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Write data to a path.

        Supported methods:
            POST /<path>

        :param path:
        :param data:
        :param wrap_ttl:
        """
        return await self._adapter.post(f"/v1/{path}", json=data, wrap_ttl=wrap_ttl)

    async def delete(self, path: str) -> None:
        """
        DELETE /<path>

        :param path:
        :return:
        """
        await self._adapter.delete(f"/v1/{path}")

    async def get_policy(self, name: str, parse: bool = False) -> Optional[Union[str, dict[Any, Any]]]:
        """
        Retrieve the policy body for the named policy.

        :param name: The name of the policy to retrieve.
        :param parse: Specifies whether to parse the policy body using pyhcl or not.
        :return: The (optionally parsed) policy body for the specified policy.
        """
        policy = None
        try:
            response = await self.sys.read_policy(name=name)
            if isinstance(response, dict):
                return response["data"]["rules"]
            raise exceptions.VaultxError('Non-dict response in "get_policy" method')
        except exceptions.HTTPError as e:
            if e.status_code == 404:
                return None

        if parse:
            if not has_hcl_parser:
                raise ImportError("pyhcl is required for policy parsing")
            policy = hcl.loads(policy)

        return policy

    async def lookup_token(
        self, token: Optional[str] = None, accessor: bool = False, wrap_ttl: Optional[int] = None
    ) -> VaultxResponse:
        """
        GET /auth/token/lookup/<token>
        GET /auth/token/lookup-accessor/<token-accessor>
        GET /auth/token/lookup-self

        :param token:
        :param accessor:
        :param wrap_ttl:
        """
        token_param = {
            "token": token,
        }
        accessor_param = {
            "accessor": token,
        }
        if token:
            if accessor:
                path = "/v1/auth/token/lookup-accessor"
                return await self._adapter.post(path, json=accessor_param, wrap_ttl=wrap_ttl)
            path = "/v1/auth/token/lookup"
            return await self._adapter.post(path, json=token_param)
        path = "/v1/auth/token/lookup-self"
        return await self._adapter.get(path, wrap_ttl=wrap_ttl)

    async def revoke_token(self, token: str, orphan: bool = False, accessor: bool = False) -> None:
        """
        POST /auth/token/revoke
        POST /auth/token/revoke-orphan
        POST /auth/token/revoke-accessor

        :param token:
        :param orphan:
        :param accessor:
        :return:
        :rtype:
        """
        if accessor and orphan:
            msg = "revoke_token does not support 'orphan' and 'accessor' flags together"
            raise exceptions.VaultxError(msg)
        if accessor:
            params = {"accessor": token}
            await self._adapter.post("/v1/auth/token/revoke-accessor", json=params)
        elif orphan:
            params = {"token": token}
            await self._adapter.post("/v1/auth/token/revoke-orphan", json=params)
        else:
            params = {"token": token}
            await self._adapter.post("/v1/auth/token/revoke", json=params)

    async def renew_token(self, token, increment=None, wrap_ttl=None):
        """
        POST /auth/token/renew
        POST /auth/token/renew-self

        :param token:
        :param increment:
        :param wrap_ttl:

        For calls expecting to hit the renew-self endpoint please use the "renew_self" method
            on "vaultx_client.auth.token" instead
        """
        params = {"increment": increment, "token": token}

        return await self._adapter.post("/v1/auth/token/renew", json=params, wrap_ttl=wrap_ttl)

    async def logout(self, revoke_token: bool = False) -> None:
        """
        Clear the token used for authentication, optionally revoking it before doing so.

        :param revoke_token:
        :return:
        """
        if revoke_token:
            await self.auth.token.revoke_self()
        self.token = None

    async def is_authenticated(self) -> bool:
        """Helper method which returns the authentication status of the client"""
        if not self.token:
            return False

        try:
            await self.lookup_token()
            return True
        except exceptions.VaultxError:
            return False

    async def auth_cubbyhole(self, token: str) -> VaultxResponse:
        """
        Perform a login request with a wrapped token.
        Stores the unwrapped token in the resulting Vault response for use by the
            :py:meth:`vaultx.adapters.AsyncAdapter` instance under the _adapter Client attribute.

        :param token: Wrapped token
        :return: The (JSON decoded) response of the auth request
        """
        self.token = token
        return await self.login("/v1/sys/wrapping/unwrap")

    async def login(self, url: str, use_token: bool = True, **kwargs: Optional[dict[Any, Any]]) -> VaultxResponse:
        """
        Perform a login request.
        Associated request is typically to a path prefixed with "/v1/auth" and optionally stores the client token sent
            in the resulting Vault response for use by the :py:meth:`vaultx.adapters.AsyncAdapter` instance
            under the _adapter AsyncClient attribute.
        :param url: Path to send the authentication request to.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the AsyncAdapter instance under the _adapter AsyncClient attribute.
        :param kwargs: Additional keyword arguments to include in the params sent with the request.
        :return: The response of the auth request.
        """
        return await self._adapter.login(url=url, use_token=use_token, **kwargs)
