import os
from typing import Any, Optional

from vaultx import exceptions
import warnings


def get_token_from_env() -> Optional[str]:
    """
    Get the token from env var, VAULT_TOKEN. If not set, attempt to get the token from, ~/.vault-token
    """
    token = os.getenv("VAULT_TOKEN")
    if not token:
        token_file_path = os.path.expanduser("~/.vault-token")
        if os.path.exists(token_file_path):
            with open(token_file_path) as f_in:
                token = f_in.read().strip()
    return token


def urljoin(*args: str) -> str:
    """
    Joins given arguments into url. Trailing and leading slashes are stripped for each argument.
    :param args: Multiple parts of a URL to be combined into one string.
    :return: Full URL combining all provided arguments
    """

    return "/".join(str(x).strip("/") for x in args)


def replace_double_slashes_to_single(url: str) -> str:
    """
    Vault CLI treats a double forward slash ('//') as a single forward slash for a given path.
    To avoid issues with the requests module's redirection logic, we perform the same translation here.
    :param url: URL as a string
    :return: Modified URL
    """

    while "//" in url:
        url = url.replace("//", "/")
    return url


def remove_nones(params: dict[Any, Any]) -> dict[Any, Any]:
    """
    Removes None values from optional arguments in a parameter dictionary.

    :param params: The dictionary of parameters to be filtered.
    :return: A filtered copy of the parameter dictionary.
    """

    return {key: value for key, value in params.items() if value is not None}


def validate_list_of_strings_param(param_name, param_argument):
    """Validate that an argument is a list of strings.
    Returns nothing if valid, raises ParamValidationException if invalid.

    :param param_name: The name of the parameter being validated. Used in any resulting exception messages.
    :type param_name: str | unicode
    :param param_argument: The argument to validate.
    :type param_argument: list
    """
    if param_argument is None:
        param_argument = []
    if isinstance(param_argument, str):
        param_argument = param_argument.split(",")
    if not isinstance(param_argument, list) or not all(isinstance(p, str) for p in param_argument):
        error_msg = 'unsupported {param} argument provided "{arg}" ({arg_type}), required type: List[str]'
        raise exceptions.VaultxError(
            error_msg.format(
                param=param_name,
                arg=param_argument,
                arg_type=type(param_argument),
            )
        )


def list_to_comma_delimited(list_param):
    """Convert a list of strings into a comma-delimited list / string.

    :param list_param: A list of strings.
    :type list_param: list
    :return: Comma-delimited string.
    :rtype: str
    """
    if list_param is None:
        list_param = []
    return ",".join(list_param)


def _smart_pop(
    dict: dict,
    member: str,
    default: Any = object(),
    *,
    posvalue: Any = object(),
    method: str = "write",
    replacement_method: str = "write_data",
):
    try:
        value = dict.pop(member)
    except KeyError:
        if posvalue is not object():
            return posvalue
        if default is not object():
            return default
        raise TypeError(f"{method}() missing one required positional argument: '{member}'")
    else:
        if posvalue is not object():
            raise TypeError(f"{method}() got multiple values for argument '{member}'")

        warnings.warn(
            (
                f"{method}() argument '{member}' was supplied as a keyword argument and will not be written as data."
                f" To write this data with a '{member}' key, use the {replacement_method}() method."
                f" To continue using {method}() and suppress this warning, supply this argument positionally."
                f" For more information see: https://github.com/hvac/hvac/issues/1034"
            ),
            DeprecationWarning,
            stacklevel=3,
        )
        return value
