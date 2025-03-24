# AWS

## IAM Authentication

`vaultx.api.auth_methods.Aws.iam_login()`

## Static Access Key Strings

Various examples of authenticating with static access key strings:

```python3
import vaultx

client = vaultx.Client()

client.auth.aws.iam_login('MY_AWS_ACCESS_KEY_ID', 'MY_AWS_SECRET_ACCESS_KEY')
client.auth.aws.iam_login('MY_AWS_ACCESS_KEY_ID', 'MY_AWS_SECRET_ACCESS_KEY', 'MY_AWS_SESSION_TOKEN')
client.auth.aws.iam_login('MY_AWS_ACCESS_KEY_ID', 'MY_AWS_SECRET_ACCESS_KEY', role='MY_ROLE')
```

## Boto3 Session

Retrieving credentials from a boto3 Session object:

```python3
import boto3
import vaultx

session = boto3.Session()
credentials = session.get_credentials()

client = vaultx.Client()
client.auth.aws.iam_login(credentials.access_key, credentials.secret_key, credentials.token)
```

##  Lambda and/or EC2 Instance

```python3
import os
import vaultx


def infer_credentials_from_iam_role(iam_role):
    on_lambda = 'AWS_LAMBDA_FUNCTION_NAME' in os.environ
    if on_lambda:
        return os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], os.environ['AWS_SESSION_TOKEN']
    else:
        security_credentials = load_aws_ec2_role_iam_credentials(iam_role)
        return security_credentials['AccessKeyId'], security_credentials['SecretAccessKey']


access_key_id, secret_access_key, session_token = infer_credentials_from_iam_role('some-role')

client = vaultx.Client()
client.auth.aws.iam_login(access_key_id, secret_access_key, session_token)
```

## Caveats For Non-Default AWS Regions

I.e., calling vaultx.api.auth_methods.Aws.iam_login() with a region argument other than its default of “us-east-1”. For additional background / context on this matter, see the comments at vaultx#251 and/or vault-ruby#161.

The following code snippets are for authenticating hosts in the us-west-1 region:

>**Note**: In order to authenticate to various regions, the AWS auth method configuration needs to be set up with an “endpoint URL” corresponding to the region in question. E.g.: “https://sts.us-west-1.amazonaws.com” in the case of this example. Vault defaults to an endpoint of “https://sts.amazonaws.com” if not configured with a different endpoint URL.

```python3
import boto3
import os
import vaultx

VAULT_ADDR = os.environ["VAULT_ADDR"]
VAULT_HEADER_VALUE = os.environ["VAULT_HEADER_VALUE"]

client = vaultx.Client(url=VAULT_ADDR)

# One-time setup of the credentials / configuration for the Vault server to use.
# Note the explicit region subdomain bit included in the endpoint argument.
client.auth.aws.configure(
    access_key='SOME_ACCESS_KEY_FOR_VAULTS_USE',
    secret_key='SOME_ACCESS_KEY_FOR_VAULTS_USE',
    endpoint='https://sts.us-west-1.amazonaws.com',
)

session = boto3.Session()
creds = session.get_credentials().get_frozen_credentials()
client.auth.aws.iam_login((
    access_key=creds.access_key,
    secret_key=creds.secret_key,
    session_token=creds.token,
    header_value=VAULT_HEADER_VALUE,
    role='some-role,
    use_token=True,
    region='us-west-1',
)
```

---

## EC2 Authentication

`vaultx.api.auth_methods.Aws.ec2_login()`

## EC2 Metadata Service

Authentication using EC2 instance role credentials and the EC2 metadata service

```python3
import logging.handlers
import os

import vaultx
import httpx


logger = logging.getLogger(__name__)

VAULT_URL = os.getenv('VAULT_ADDR', 'https://127.0.0.1:8200')
VAULT_CERTS = ('/etc/vault.d/ssl/bundle.crt', '/etc/vault.d/ssl/vault.key')
TOKEN_NONCE_PATH = os.getenv('WP_VAULT_TOKEN_NONCE_PATH', '/root/.vault-token-meta-nonce')
EC2_METADATA_URL_BASE = 'http://169.254.169.254'


def load_aws_ec2_pkcs7_string(metadata_url_base: str = EC2_METADATA_URL_BASE) -> str:
    """
    Requests an ec2 instance's pkcs7-encoded identity document from the EC2 metadata service.
    :param metadata_url_base: IP address for the EC2 metadata service.
    :return: string, pkcs7-encoded identity document from the EC2 metadata service
    """
    metadata_pkcs7_url = f'{metadata_url_base}/latest/dynamic/instance-identity/pkcs7'
    logger.debug(f"load_aws_ec2_pkcs7_string connecting to {metadata_pkcs7_url}")

    response = httpx.get(url=metadata_pkcs7_url)
    response.raise_for_status()

    pcks7 = response.text.replace('\n', '')

    return pcks7


def load_aws_ec2_nonce_from_disk(token_nonce_path: str = TOKEN_NONCE_PATH) -> bytes:
    """
    Helper method to load a previously stored "token_meta_nonce" returned in the
    initial authorization AWS EC2 request from the current instance to our Vault service.
    :param token_nonce_path: string, the full filesystem path to a file containing the instance's
        token meta nonce.
    :return: string, a previously stored "token_meta_nonce"
    """
    logger.debug(f"Attempting to load vault token meta nonce from path: {token_nonce_path}")
    try:
        with open(token_nonce_path, 'rb') as nonce_file:
            nonce = nonce_file.readline()
    except IOError:
        logger.warning(f"Unable to load vault token meta nonce at path: {token_nonce_path}")
        nonce = None

    logger.debug(f"Nonce loaded: {nonce}")
    return nonce


def write_aws_ec2_nonce_to_disk(token_meta_nonce: str, token_nonce_path: str = TOKEN_NONCE_PATH) -> None:
    """
    Helper method to store the current "token_meta_nonce" returned from authorization AWS EC2 request
    from the current instance to our Vault service.
    :return: string, a previously stored "token_meta_nonce"
    :param token_meta_nonce: string, the actual nonce
    :param token_nonce_path: string, the full filesystem path to a file containing the instance's
        token meta nonce.
    :return: None
    """
    logger.debug(f'Writing nonce "{token_meta_nonce}" to file "{token_nonce_path}".')
    with open(token_nonce_path, 'w') as nonce_file:
        nonce_file.write(token_meta_nonce)


def auth_ec2(vault_client, pkcs7=None, nonce=None, role=None, mount_point='aws', store_nonce=True):
    """
    Helper method to authenticate to vault using the "auth_ec2" backend.
    :param vault_client: vaultx.Client
    :param pkcs7: pkcs7-encoded identity document from the EC2 metadata service
    :param nonce: string, the nonce returned from the initial AWS EC2 auth request (if applicable)
    :param role: string, the role/policy to request. Defaults to the current instance's AMI ID if not provided.
    :param mount_point: string, the path underwhich the AWS EC2 auth backend is provided
    :param store_nonce: bool, if True, store the nonce received in the auth_ec2 response on disk for later use.
        Especially useful for automated secure introduction.
    :param kwargs: dict, remaining arguments blindly passed through by this lookup module class
    :return: None
    """
    if pkcs7 is None:
        logger.debug('No pkcs7 argument provided to auth_ec2 backend.')
        logger.debug('Attempting to retrieve information from EC2 metadata service.')
        pkcs7 = load_aws_ec2_pkcs7_string()

    if nonce is None:
        logger.debug('No nonce argument provided to auth_ec2 backend.')
        logger.debug('Attempting to retrieve information from disk.')
        nonce = load_aws_ec2_nonce_from_disk()

    auth_ec2_resp = vault_client.auth.aws.ec2_login(
        pkcs7=pkcs7,
        nonce=nonce,
        role=role,
        use_token=False,
        mount_point=mount_point
    )

    if store_nonce and 'metadata' in auth_ec2_resp.get('auth', dict()):
        token_meta_nonce = auth_ec2_resp['auth']['metadata'].get('nonce')
        if token_meta_nonce is not None:
            logger.debug(f'token_meta_nonce received back from auth_ec2 call: {token_meta_nonce}')
            write_aws_ec2_nonce_to_disk(token_meta_nonce)
        else:
            logger.warning('No token meta nonce returned in auth response.')

    return auth_ec2_resp


def get_vault_client(vault_url=VAULT_URL, certs=VAULT_CERTS, verify_certs=True, ec2_role=None):
    """
    Instantiates a vaultx / vault client.
    :param vault_url: string, protocol + address + port for the vault service
    :param certs: tuple, Optional tuple of self-signed certs to use for verification with vaultx's requests
    :param verify_certs: bool, if True use the provided certs tuple for verification with vaultx's requests.
        If False, don't verify SSL with vaultx's requests (typically used with local development).
    :param ec2_role: str, Name of the Vault AWS auth backend role to use when retrieving a token (if applicable)
    :return: vaultx.Client
    """
    logger.debug('Retrieving a vault (vaultx) client...')
    if verify_certs:
        # We use a self-signed certificate for the vault service itself, so we need to include our
        # local ca bundle here for the underlying httpx module.
        os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'
        vault_client = vaultx.Client(
            url=vault_url,
            cert=certs,
        )
    else:
        vault_client = vaultx.Client(
            url=vault_url,
            verify=False,
        )

    vault_client.token = load_vault_token(vault_client, ec2_role=ec2_role)

    if not vault_client.is_authenticated():
        raise vaultx.exceptions.VaultxError('Unable to authenticate to the Vault service')

    return vault_client


authenticated_vault_client = get_vault_client()
```
