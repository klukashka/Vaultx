import abc
import ssl  # pragma: no cover
import types
import typing as tp
from types import CoroutineType
from typing import Any, Optional, Union

import aiohttp
import httpx
from httpx import Response

from vaultx.constants.client import DEFAULT_URL
from vaultx.utils import replace_double_slashes_to_single, urljoin
from . import _types, exceptions
from .exceptions import VaultxError


class MetaAdapter(metaclass=abc.ABCMeta):
    """Abstract adapter class"""

    @classmethod
    @abc.abstractmethod
    def from_adapter(
        cls: tp.Type["MetaAdapter"],
        adapter: object,
    ) -> "MetaAdapter":
        """
        Creates a new adapter based on an existing Adapter instance.
        This can be used to create a new type of adapter that inherits the properties of an existing one.

        :param adapter: The existing Adapter instance.
        """

        raise NotImplementedError()


class Adapter(MetaAdapter):
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

    @classmethod
    @exceptions.handle_unknown_exception
    def from_adapter(
        cls: tp.Type["Adapter"],
        adapter: object,
    ) -> "Adapter":
        if isinstance(adapter, Adapter):
            return cls(
                base_uri=adapter.base_uri,
                token=adapter.token,
                follow_redirects=adapter.follow_redirects,
                client=adapter.client,
                namespace=adapter.namespace,
                ignore_exceptions=adapter.ignore_exceptions,
                strict_http=adapter.strict_http,
                request_header=adapter.request_header,
                **adapter._kwargs,
            )
        raise exceptions.VaultxError(
            '"from_adapter" method of Adapter class should receive Adapter instance as a parameter'
        )

    @exceptions.handle_unknown_exception
    def close(self):
        """Close the Client's underlying TCP connections."""
        self.client.close()

    @exceptions.handle_unknown_exception
    def get(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform a GET request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("GET", url, **kwargs)

    @exceptions.handle_unknown_exception
    def post(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform a POST request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("POST", url, **kwargs)

    @exceptions.handle_unknown_exception
    def put(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform a PUT request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("PUT", url, **kwargs)

    @exceptions.handle_unknown_exception
    def delete(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform a DELETE request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("DELETE", url, **kwargs)

    @exceptions.handle_unknown_exception
    def list(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform a LIST request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("LIST", url, **kwargs)

    @exceptions.handle_unknown_exception
    def head(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform a HEAD request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return self.request("HEAD", url, **kwargs)

    @exceptions.handle_unknown_exception
    def login(self, url: str, use_token: bool = True, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
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
    def get_login_token(self, response: Union[dict[str, Any], Response]) -> str:
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
    ) -> Union[dict[str, Any], Response]:
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
class RawAdapter(Adapter):
    """
    The RawAdapter adapter class.
    This adapter adds Vault-specific headers as required and optionally raises exceptions on errors,
    but always returns Response objects for requests.
    """

    def get_login_token(self, response: Union[dict[str, Any], Response]) -> str:
        """
        Extract the client token from a login response.

        :param response: The response object returned by the login method.
        """
        if isinstance(response, Response):
            response_json = response.json()
            return response_json["auth"]["client_token"]
        return response["auth"]["client_token"]

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        raise_exception: Optional[bool] = True,
        **kwargs: Optional[Any],
    ) -> Union[dict[str, Any], Response]:
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

        return response


@exceptions.handle_unknown_exception
class JsonAdapter(RawAdapter):
    """
    The JsonAdapter adapter class.
    This adapter works just like the RawAdapter adapter except that HTTP 200 responses are returned as JSON dicts.
    All non-200 responses are returned as Response objects.
    """

    def get_login_token(self, response: Union[dict[str, Any], Response]) -> str:
        """
        Extracts the client token from a login response.

        :param response: The response object returned by the login method.
        """
        if isinstance(response, Response):
            response_json = response.json()
            return response_json["auth"]["client_token"]
        return response["auth"]["client_token"]

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        raise_exception: Optional[bool] = True,
        **kwargs: Optional[Any],
    ) -> Union[dict[str, Any], Response]:
        """
        Main method for routing HTTP requests to the configured Vault base_uri.

        :param method: HTTP method to use with the request. E.g., GET, POST, etc.
        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param headers: Additional headers to include with the request.
        :param raise_exception: If True, raise an exception.
        :param kwargs: Keyword arguments to pass to RawAdapter.request.
        """
        response = super().request(method=method, url=url, headers=headers, raise_exception=raise_exception, **kwargs)
        if isinstance(response, Response):
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError:
                    pass

            return response
        raise VaultxError("Unexpected dict return from RawAdapter's request method inside JsonAdapter's request method")


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


class AsyncAdapter(MetaAdapter):
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

    @classmethod
    @exceptions.handle_unknown_exception
    def from_adapter(
        cls: tp.Type["AsyncAdapter"],
        adapter: object,
    ) -> "AsyncAdapter":
        if isinstance(adapter, AsyncAdapter):
            return cls(
                base_uri=adapter.base_uri,
                token=adapter.token,
                follow_redirects=adapter.follow_redirects,
                client=adapter.client,
                namespace=adapter.namespace,
                ignore_exceptions=adapter.ignore_exceptions,
                strict_http=adapter.strict_http,
                request_header=adapter.request_header,
                **adapter._kwargs,
            )
        raise exceptions.VaultxError(
            '"from_adapter" method of AsyncAdapter class should receive AsyncAdapter instance as a parameter'
        )

    @exceptions.handle_unknown_exception
    async def close(self):
        """Close the AsyncClient's underlying TCP connections."""
        await self.client.aclose()

    @exceptions.handle_unknown_exception
    async def get(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform an async GET request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("GET", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def post(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform an async POST request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("POST", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def put(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform an async PUT request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("PUT", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def delete(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform an async DELETE request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("DELETE", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def list(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform an async LIST request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("LIST", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def head(self, url: str, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
        """
        Perform an async HEAD request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """
        return await self.request("HEAD", url, **kwargs)

    @exceptions.handle_unknown_exception
    async def login(self, url: str, use_token: bool = True, **kwargs: Optional[Any]) -> Union[dict[str, Any], Response]:
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
    async def get_login_token(self, response: Union[dict[str, Any], Response]) -> str:
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
    ) -> Union[dict[str, Any], Response]:
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
class AsyncRawAdapter(AsyncAdapter):
    """The AsyncRawAdapter adapter class. Mostly similar to the sync version."""

    async def get_login_token(self, response: Union[dict[str, Any], Response]) -> str:
        """
        Extract the client token from a login response.

        :param response: The response object returned by the login method.
        """
        if isinstance(response, Response):
            response_json = response.json()
            return response_json["auth"]["client_token"]
        return response["auth"]["client_token"]

    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        raise_exception: Optional[bool] = True,
        **kwargs: Optional[Any],
    ) -> Union[dict[str, Any], Response]:
        """Main method for routing HTTP requests to the configured Vault base_uri.

        :param method: HTTP method to use with the request. E.g., GET, POST, etc.
        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param headers: Additional headers to include with the request.
        :param raise_exception: If True, raise an exception.
        :param kwargs: Additional keyword arguments to include in the requests call.
        """

        # url = replace_double_slashes_to_single(url)
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

        return response


@exceptions.handle_unknown_exception
class AsyncJsonAdapter(AsyncRawAdapter):
    """The AsyncJsonAdapter adapter class. Mostly similar to the sync version"""

    async def get_login_token(self, response: Union[dict[str, Any], Response]) -> str:
        """
        Extract the client token from a login response.

        :param response: The response object returned by the login method.
        """
        if isinstance(response, Response):
            response_json = response.json()
            return response_json["auth"]["client_token"]
        return response["auth"]["client_token"]

    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        raise_exception: Optional[bool] = True,
        **kwargs: Optional[Any],
    ) -> Union[dict[str, Any], Response]:
        """
        Main method for routing HTTP requests to the configured Vault base_uri.

        :param method: HTTP method to use with the request. E.g., GET, POST, etc.
        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :param headers: Additional headers to include with the request.
        :param raise_exception: If True, raise an exception.
        :param kwargs: Keyword arguments to pass to AsyncRawAdapter.request.
        """
        response = await super().request(
            method=method, url=url, headers=headers, raise_exception=raise_exception, **kwargs
        )
        if isinstance(response, Response):
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError:
                    pass

            return response
        raise VaultxError(
            "Unexpected dict return from AsyncRawAdapter's request method inside AsyncJsonAdapter's request method"
        )
