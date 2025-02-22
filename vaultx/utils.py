import os
from typing import Optional


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
