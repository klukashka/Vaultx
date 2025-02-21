import functools
import http
import sys
import typing as tp
from collections.abc import Mapping
from typing import Optional


if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec


class VaultxError(Exception):
    """
    Raised when an error occurs in the vaultx package.
    You can catch this exception to handle all errors in the package.
    Check the inherited classes for more concrete exceptions.
    """

    def __init__(self, message=None, errors=None, method=None, url=None, text=None, json=None):
        if errors:
            message = ", ".join(errors)

        self.errors = errors
        self.method = method
        self.url = url
        self.text = text
        self.json = json

        super().__init__(message)


class HTTPError(Exception):
    """
    Vaultx exception for handling http errors
    HTTP status codes used throughout the API: https://www.vaultproject.io/api-docs
    """

    def __init__(
        self,
        status_code: int,
        method: Optional[str] = None,
        url: Optional[str] = None,
        detail: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.method = method
        self.url = url

        self.detail = detail
        self.headers = headers

    def __str__(self) -> str:
        return f"{self.status_code}: {self.detail}, method: {self.method}, URL: {self.url}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"


T = tp.TypeVar("T")
P = ParamSpec("P")
R = tp.TypeVar("R")


@tp.overload
def handle_unknown_exception(obj: tp.Type[T]) -> tp.Type[T]: ...


@tp.overload
def handle_unknown_exception(obj: tp.Callable[P, R]) -> tp.Callable[P, R]: ...


def handle_unknown_exception(  # noqa: C901
    obj: tp.Union[tp.Callable[..., tp.Any], type],
) -> tp.Union[tp.Callable[..., tp.Any], type]:
    """
    A decorator that catches all exceptions in the decorated function and raises VaultxError instead.
    Implemented to guarantee that all exceptions in the vaultx package are overridden by VaultxError.

    When applied to a class, all callable attributes (methods, staticmethods and classmethods) will be wrapped.
    """
    if isinstance(obj, type):
        for attr_name, attr in obj.__dict__.items():
            if attr_name != "__call__" and attr_name.startswith("__") and attr_name.endswith("__"):
                continue

            if isinstance(attr, staticmethod):
                decorated_func = handle_unknown_exception(attr.__func__)
                setattr(obj, attr_name, staticmethod(decorated_func))
            elif isinstance(attr, classmethod):
                decorated_func = handle_unknown_exception(attr.__func__)
                setattr(obj, attr_name, classmethod(decorated_func))
            elif isinstance(attr, property):
                new_getter = handle_unknown_exception(attr.fget) if attr.fget is not None else None
                new_setter = handle_unknown_exception(attr.fset) if attr.fset is not None else None
                new_deleter = handle_unknown_exception(attr.fdel) if attr.fdel is not None else None
                setattr(obj, attr_name, property(new_getter, new_setter, new_deleter))
            elif callable(attr):
                decorated = handle_unknown_exception(attr)
                setattr(obj, attr_name, decorated)
        return obj

    @functools.wraps(obj)
    def wrapper(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        try:
            return obj(*args, **kwargs)
        except VaultxError:
            raise
        except Exception as exc:
            raise VaultxError(message=f"An error occurred in {obj.__name__}: {str(exc)}") from exc

    return wrapper
