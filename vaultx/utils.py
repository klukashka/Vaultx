import os
from typing import Any, Optional

from vaultx import exceptions


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
    Join given arguments into url. Trailing and leading slashes are stripped for each argument.
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
    Remove None values from optional arguments in a parameter dictionary.

    :param params: The dictionary of parameters to be filtered.
    :return: A filtered copy of the parameter dictionary.
    """

    return {key: value for key, value in params.items() if value is not None}


def validate_list_of_strings_param(param_name: str, param_arg: Optional[list[str]]) -> None:
    """
    Validate that an argument is a list of strings.
    Returns nothing if valid, raises ParamValidationException if invalid.

    :param param_name: The name of the parameter being validated. Used in any resulting exception messages.
    :param param_arg: The argument to validate.
    """
    if param_arg is None:
        param_arg = []
    if isinstance(param_arg, str):
        param_arg = param_arg.split(",")
    if not isinstance(param_arg, list) or not all(isinstance(p, str) for p in param_arg):
        raise exceptions.VaultxError(
            f'unsupported {param_name} argument provided "{param_arg}" ({type(param_arg)}), required type: List[str]'
        )


def list_to_comma_delimited(list_param) -> str:
    """
    Convert a list of strings into a comma-delimited list / string.

    :param list_param: A list of strings.
    :type list_param: list
    :return: Comma-delimited string.
    """
    if list_param is None:
        list_param = []
    return ",".join(list_param)
