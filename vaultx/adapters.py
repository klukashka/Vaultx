import abc
import ssl  # pragma: no cover
import types
import typing as tp
from types import CoroutineType
from typing import Any, Optional, Union

import aiohttp
import httpx

from vaultx.constants.client import DEFAULT_URL
from vaultx.utils import replace_double_slashes_to_single, urljoin
from . import _types, exceptions


class AdapterResponse(metaclass=abc.ABCMeta):
    """Abstract base class for Adapter responses."""

    @property
    @abc.abstractmethod
    def raw(self) -> Any:
        """
        The raw response object.
        The specific Adapter determines the type or whether to return anything.
        :return: The raw response object from the request, if applicable.
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def status(self) -> int:
        """
        The HTTP status code of the response.
        :return: An HTTP response code.
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def value(self) -> Any:
        """
        The value of the response.
        The specific Adapter determines the type of the response.
        :return: The value returned by the request.
        """
        raise NotImplementedError()


@exceptions.handle_unknown_exception
class HttpxAdapterResponse(AdapterResponse):
    """An abstract AdapterResponse class for responses based on a httpx.Response."""

    _raw: tp.Final[httpx.Response]
    _value: tp.Final[dict]

    def __init__(self, response: httpx.Response) -> None:
        try:
            value = response.json()
        except ValueError:
            value = {}
        self._value = value
        self._raw = response

    @property
    def raw(self) -> httpx.Response:
        return self._raw

    @property
    def status(self) -> int:
        return self._raw.status_code

    @property
    def value(self) -> dict:
        return self._value


@exceptions.handle_unknown_exception
class VaultxResponse(HttpxAdapterResponse):
    """The specialized AdapterResponse used for the HvacAdapter."""

    def __getattr__(self, __name: str) -> Any:
        if __name == "_value" or __name == "_raw":
            raise AttributeError
        return getattr(self.value, __name)

    def __getitem__(self, __key: object) -> Any:
        try:
            return self.value.__getitem__(__key)
        except KeyError as e:
            raise KeyError(f'Failed to get "{__key}" item from VaultxResponse.') from e

    def __len__(self) -> int:
        return self.value.__len__()

    def __contains__(self, __o: object) -> bool:
        return self.value.__contains__(__o)


class Adapter:
    """Abstract synchronous adapter class"""

    def __init__(
        self,
        base_uri: str = DEFAULT_URL,
        token: Optional[str] = None,
        cert: Optional[_types.CertTypes] = None,
        verify: Union[ssl.SSLContext, str, bool] = True,
        timeout: int = 30,
        proxy: Optional[str] = None,
        follow_redirects: bool = True,
        client: Optional[httpx.Client] = None,
        namespace: Optional[str] = None,
        ignore_exceptions: bool = False,
        strict_http: bool = False,
        request_header: bool = True,
    ) -> None:
        """
        Create a new request adapter instance.

        :param base_uri: Base URL for the Vault instance being addressed.
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
        :param namespace: Optional Vault Namespace.
        :param ignore_exceptions: If True, _always_ return the response object for a given request.
            I.e., don't raise an exception based on response status code, etc.
        :param strict_http: If True, use only standard HTTP verbs in request with additional params,
            otherwise process as is
        :param request_header: If true, add the X-Vault-Request header to all requests
            to protect against SSRF vulnerabilities.
        """

        if not client:
            client = httpx.Client(cert=cert, verify=verify, proxy=proxy)

        self.base_uri = base_uri
        self.token = token
        self.namespace = namespace
        self.client = client
        self.follow_redirects = follow_redirects
        self.ignore_exceptions = ignore_exceptions
        self.strict_http = strict_http
        self.request_header = request_header

        self._kwargs: dict[str, Any] = {
            "cert": cert,
            "verify": verify,
            "timeout": timeout,
            "proxy": proxy,
        }

    def __enter__(self: "Adapter") -> "Adapter":
        self.client.__enter__()
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[types.TracebackType] = None,
    ) -> None:
        self.client.__exit__(exc_type, exc_value, traceback)

    @exceptions.handle_unknown_exception
    def close(self):
        """Close the Client's underlying TCP connections."""
        self.client.close()

    @exceptions.handle_unknown_exception
    def get(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform a GET request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("GET", url, **kwargs)

    @exceptions.handle_unknown_exception
    def post(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform a POST request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("POST", url, **kwargs)

    @exceptions.handle_unknown_exception
    def put(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform a PUT request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("PUT", url, **kwargs)

    @exceptions.handle_unknown_exception
    def delete(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform a DELETE request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("DELETE", url, **kwargs)

    @exceptions.handle_unknown_exception
    def list(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform a LIST request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("LIST", url, **kwargs)

    @exceptions.handle_unknown_exception
    def head(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform a HEAD request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("HEAD", url, **kwargs)

    @exceptions.handle_unknown_exception
    def login(self, url: str, use_token: bool = True, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform a login request.

        Associated request is typically to a path prefixed with "/v1/auth" and optionally stores the client token sent
            in the resulting Vault response for use by the :py:meth:`vaultx.adapters.Adapter` instance
            under the _adapter Client attribute.

        :param url: Path to send the authentication request to.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.Adapter` instance under the _adapter Client attribute.
        :param kwargs: Additional keyword arguments to include in the params sent with the request.
        """
        response = self.post(url, **kwargs)

        if use_token:
            self.token = self.get_login_token(response)

        return response

    @abc.abstractmethod
    def get_login_token(self, response: VaultxResponse) -> str:
        """
        Extract the client token from a login response.

        :param response: The response object returned by the login method.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        raise_exception: Optional[bool] = True,
        **kwargs: Optional[Any],
    ) -> VaultxResponse:
        """
        Main method for routing HTTP requests to the configured Vault base_uri.
        Intended to be implemented by subclasses.

        :param method: HTTP method to use with the request. E.g., GET, POST, etc.
        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param headers: Additional headers to include with the request.
        :type headers: dict
        :param kwargs: Additional keyword arguments to include in the requests call.
        :param raise_exception: If True, raise an exception.
        """
        raise NotImplementedError()


@exceptions.handle_unknown_exception
class VaultxAdapter(Adapter):
    """
    The VaultxAdapter adapter class.
    This adapter adds Vault-specific headers as required and optionally raises exceptions on errors,
    but always returns VaultxResponse objects for requests.
    """

    def get_login_token(self, response: VaultxResponse) -> str:
        """
        Extract the client token from a login response.

        :param response: The response object returned by the login method.
        """
        return response.value["auth"]["client_token"]

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        raise_exception: Optional[bool] = True,
        **kwargs: Optional[Any],
    ) -> VaultxResponse:
        """
        Main method for routing HTTP requests to the configured Vault base_uri.

        :param method: HTTP method to use with the request. E.g., GET, POST, etc.
        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param headers: Additional headers to include with the request.
        :param raise_exception: If True, raise an exception.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """

        url = replace_double_slashes_to_single(url)
        url = urljoin(self.base_uri, url)

        if not headers:
            headers = {}

        if self.request_header:
            headers["X-Vault-Request"] = "true"

        if self.token:
            headers["X-Vault-Token"] = self.token

        if self.namespace:
            headers["X-Vault-Namespace"] = self.namespace

        wrap_ttl = kwargs.pop("wrap_ttl", None)
        if wrap_ttl:
            headers["X-Vault-Wrap-TTL"] = str(wrap_ttl)

        _kwargs: dict[str, Any] = {"timeout": self._kwargs.get("timeout")}
        _kwargs.update(kwargs)

        if self.strict_http and method.lower() in ("list",):
            # Entry point for standard HTTP substitution
            params = _kwargs.get("params", {})
            if method.lower() == "list":
                method = "get"
                params.update({"list": "true"})
            _kwargs["params"] = params

        response = self.client.request(
            method=method, url=url, headers=headers, follow_redirects=self.follow_redirects, **_kwargs
        )

        if not response.is_success and (raise_exception and not self.ignore_exceptions):
            raise exceptions.HTTPError(status_code=response.status_code, method=method, url=url)

        return VaultxResponse(response)


@exceptions.handle_unknown_exception
class AiohttpTransport(httpx.AsyncBaseTransport):
    """Class for providing httpx requests with aiohttp transport"""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self._session = session or aiohttp.ClientSession()
        self._closed = False

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        if self._closed:
            raise RuntimeError("Transport is closed")

        aiohttp_headers = dict(request.headers)

        # Prepare request parameters
        method = request.method
        url = str(request.url)
        content = request.content

        async with self._session.request(
            method=method,
            url=url,
            headers=aiohttp_headers,
            data=content,
            allow_redirects=False,
        ) as aiohttp_response:
            content = await aiohttp_response.read()
            headers: list = [(k.lower(), v) for k, v in aiohttp_response.headers.items()]
            return httpx.Response(
                status_code=aiohttp_response.status, headers=headers, content=content, request=request
            )

    async def aclose(self):
        if not self._closed:
            self._closed = True
            await self._session.close()


class AsyncAdapter:
    """Abstract asynchronous adapter class"""

    def __init__(
        self,
        base_uri: str = DEFAULT_URL,
        token: Optional[str] = None,
        cert: Optional[_types.CertTypes] = None,
        verify: Union[ssl.SSLContext, str, bool] = True,
        timeout: int = 30,
        proxy: Optional[str] = None,
        follow_redirects: bool = True,
        client: Optional[httpx.AsyncClient] = None,
        namespace: Optional[str] = None,
        ignore_exceptions: bool = False,
        strict_http: bool = False,
        request_header: bool = True,
    ) -> None:
        """
        Create a new async request adapter instance.

        :param base_uri: Base URL for the Vault instance being addressed.
        :param token: Authentication token to include in requests sent to Vault.
        :param cert: Certificates for use in requests sent to the Vault instance. This should be a tuple with the
            certificate and then key.
        :type cert: tuple
        :param verify: Either a boolean to indicate whether TLS verification should be performed
            when sending requests to Vault, or a string pointing at the CA bundle to use for verification.
            See https://www.python-httpx.org/advanced/ssl/
        :param timeout: The timeout value for requests sent to Vault.
        :param proxy: Proxy to use when performing requests.
            See: https://www.python-httpx.org/advanced/proxies/
        :param follow_redirects: Whether to follow redirects when sending requests to Vault.
        :param client: Optional client object to use when performing request.
        :param namespace: Optional Vault Namespace.
        :param ignore_exceptions: If True, always return the response object for a given request.
            I.e., don't raise an exception based on response status code, etc.
        :param strict_http: If True, use only standard HTTP verbs in request with additional params,
            otherwise process as is
        :param request_header: If true, add the X-Vault-Request header to all requests
            to protect against SSRF vulnerabilities.
        """

        if not client:
            client = httpx.AsyncClient(cert=cert, verify=verify, proxy=proxy, transport=AiohttpTransport())
            # client = httpx.AsyncClient(cert=cert, verify=verify, proxy=proxy)

        self.base_uri = base_uri
        self.token = token
        self.namespace = namespace
        self.client = client
        self.follow_redirects = follow_redirects
        self.ignore_exceptions = ignore_exceptions
        self.strict_http = strict_http
        self.request_header = request_header

        self._kwargs: dict[str, Any] = {
            "cert": cert,
            "verify": verify,
            "timeout": timeout,
            "proxy": proxy,
        }

    @exceptions.handle_unknown_exception
    async def __aenter__(self: "AsyncAdapter") -> "AsyncAdapter":
        await self.client.__aenter__()
        return self

    @exceptions.handle_unknown_exception
    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[types.TracebackType] = None,
    ) -> None:
        await self.client.__aexit__(exc_type, exc_value, traceback)

    @exceptions.handle_unknown_exception
    async def close(self):
        """Close the AsyncClient's underlying TCP connections."""
        await self.client.aclose()

    @exceptions.handle_unknown_exception
    async def get(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform an async GET request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("GET", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def post(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform an async POST request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("POST", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def put(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform an async PUT request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("PUT", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def delete(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform an async DELETE request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("DELETE", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def list(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform an async LIST request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("LIST", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def head(self, url: str, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform an async HEAD request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("HEAD", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def login(self, url: str, use_token: bool = True, **kwargs: Optional[Any]) -> VaultxResponse:
        """
        Perform an async login request.

        Associated request is typically sent to a path prefixed with "/v1/auth"
            and optionally stores the client token sent in the resulting Vault response
            for use by the :py:meth:`vaultx.adapters.AsyncAdapter` instance under the _adapter Client attribute.

        :param url: Path to send the authentication request to.
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.AsyncAdapter` instance under the _adapter Client attribute.
        :param kwargs: Additional keyword arguments to include in the params sent with the request.
        """
        response = await self.post(url, **kwargs)

        if use_token:
            self.token = await self.get_login_token(response)

        return response

    @abc.abstractmethod
    async def get_login_token(self, response: VaultxResponse) -> str:
        """
        Extract the async_client token from a login response.

        :param response: The response object returned by the login method.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        raise_exception: Optional[bool] = True,
        **kwargs: Optional[Any],
    ) -> VaultxResponse:
        """
        Main method for routing HTTP requests to the configured Vault base_uri.
        Intended to be implemented by subclasses.

        :param method: HTTP method to use with the request. E.g., GET, POST, etc.
        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param headers: Additional headers to include with the request.
        :param kwargs: Additional keyword arguments to include in the requests call.
        :param raise_exception: If True, raise an exception.
        """
        raise NotImplementedError()


@exceptions.handle_unknown_exception
class AsyncVaultxAdapter(AsyncAdapter):
    """The AsyncVaultxAdapter adapter class. Mostly similar to the sync version."""

    async def get_login_token(self, response: VaultxResponse) -> str:
        """
        Extract the client token from a login response.

        :param response: The response object returned by the login method.
        """
        return response.value["auth"]["client_token"]

    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        raise_exception: Optional[bool] = True,
        **kwargs: Optional[Any],
    ) -> VaultxResponse:
        """Main method for routing HTTP requests to the configured Vault base_uri.

        :param method: HTTP method to use with the request. E.g., GET, POST, etc.
        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param headers: Additional headers to include with the request.
        :param raise_exception: If True, raise an exception.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """

        url = replace_double_slashes_to_single(url)
        url = urljoin(self.base_uri, url)

        if not headers:
            headers = {}

        if self.request_header:
            headers["X-Vault-Request"] = "true"

        if self.token and not isinstance(self.token, CoroutineType):
            headers["X-Vault-Token"] = self.token

        if self.namespace:
            headers["X-Vault-Namespace"] = self.namespace

        wrap_ttl = kwargs.pop("wrap_ttl", None)
        if wrap_ttl:
            headers["X-Vault-Wrap-TTL"] = str(wrap_ttl)

        _kwargs: dict[str, Any] = {"timeout": self._kwargs.get("timeout")}
        _kwargs.update(kwargs)

        if self.strict_http and method.lower() in ("list",):
            # Entry point for standard HTTP substitution
            params = _kwargs.get("params", {})
            if method.lower() == "list":
                method = "get"
                params.update({"list": "true"})
            _kwargs["params"] = params

        response = await self.client.request(
            method=method, url=url, headers=headers, follow_redirects=self.follow_redirects, **_kwargs
        )

        if not response.is_success and (raise_exception and not self.ignore_exceptions):
            raise exceptions.HTTPError(status_code=response.status_code, method=method, url=url)

        return VaultxResponse(response)
