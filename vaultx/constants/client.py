from os import getenv


DEFAULT_URL = "http://localhost:8200"
VAULT_CACERT = getenv("VAULT_CACERT")
VAULT_CAPATH = getenv("VAULT_CAPATH")
VAULT_CLIENT_CERT = getenv("VAULT_CLIENT_CERT")
VAULT_CLIENT_KEY = getenv("VAULT_CLIENT_KEY")
