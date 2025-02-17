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
