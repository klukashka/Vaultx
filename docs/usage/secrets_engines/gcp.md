# GCP

## Configure

`vaultx.api.secrets_engines.Gcp.configure(credentials=None, ttl=None, max_ttl=None, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')


credentials = test_utils.load_config_file('example.jwt.json')
configure_response = client.secrets.gcp.configure(
    credentials=credentials,
    max_ttl=3600,
)
print(configure_response)
```

## Rotate Root Credentials

`vaultx.api.secrets_engines.Gcp.rotate_root_credentials(mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

rotate_response = client.secrets.gcp.rotate_root_credentials()
```

## Read Config


`vaultx.api.secrets_engines.Gcp.read_config(mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

read_config_response = client.secrets.gcp.read_config()
print('Max TTL for GCP secrets engine set to: {max_ttl}'.format(max_ttl=read_config_response['data']['max_ttl']))
```


## Create Or Update Roleset

`vaultx.api.secrets_engines.Gcp.create_or_update_roleset(name, project, bindings, secret_type=None, token_scopes=None, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')


bindings = """
    resource "//cloudresourcemanager.googleapis.com/project/some-gcp-project-id" {
      roles = [
        "roles/viewer"
      ],
    }
"""
token_scopes = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/bigquery',
]

roleset_response = client.secrets.gcp.create_or_update_roleset(
    name='vaultx-doctest',
    project='some-gcp-project-id',
    bindings=bindings,
    token_scopes=token_scopes,
)
```

## Rotate Roleset Account

`vaultx.api.secrets_engines.Gcp.rotate_roleset_account(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

rotate_response = client.secrets.gcp.rotate_roleset_account(name='vaultx-doctest')
```

## Rotate Roleset Account Key

`vaultx.api.secrets_engines.Gcp.rotate_roleset_account_key(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

rotate_response = client.secrets.gcp.rotate_roleset_account_key(name='vaultx-doctest')
```

## Read Roleset

`vaultx.api.secrets_engines.Gcp.read_roleset(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

read_response = client.secrets.gcp.read_roleset(name='vaultx-doctest')
```

## List Rolesets

`vaultx.api.secrets_engines.Gcp.list_rolesets(mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

list_response = client.secrets.gcp.list_rolesets()
```

## Delete Roleset

`vaultx.api.secrets_engines.Gcp.delete_roleset(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

delete_response = client.secrets.gcp.delete_roleset(name='vaultx-doctest')
```

## Generate Oauth2 Access Token

`vaultx.api.secrets_engines.Gcp.generate_oauth2_access_token(roleset, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

token_response = client.secrets.gcp.generate_oauth2_access_token(roleset='vaultx-doctest')
```

## Generate Service Account Key

`vaultx.api.secrets_engines.Gcp.generate_service_account_key(roleset, key_algorithm='KEY_ALG_RSA_2048', key_type='TYPE_GOOGLE_CREDENTIALS_FILE', method='POST', mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

key_response = client.secrets.gcp.generate_service_account_key(roleset='vaultx-doctest')
```

## Create Or Update Static Account

`vaultx.api.secrets_engines.Gcp.create_or_update_static_account(name, service_account_email, bindings=None, secret_type=None, token_scopes=None, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

create_response = client.secrets.gcp.create_or_update_static_account(
  name="vaultx-doctest",
  service_account_email="vaultx-doctest@some-gcp-project-id.iam.gserviceaccount.com",
  secret_type="access_token",
  token_scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
```

## Rotate Static Account Key

`vaultx.api.secrets_engines.Gcp.rotate_static_account_key(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

rotate_response = client.secrets.gcp.rotate_static_account_key(name="vaultx-doctest")
```

## Read Static Account

`vaultx.api.secrets_engines.Gcp.read_static_account(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

read_response = client.secrets.gcp.read_static_account(name="vaultx-doctest")
```

## List Static Accounts

`vaultx.api.secrets_engines.Gcp.list_static_accounts(mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

list_response = client.secrets.gcp.list_static_accounts()
```

## Delete Static Account

`vaultx.api.secrets_engines.Gcp.delete_static_account(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

delete_response = client.secrets.gcp.delete_static_account(name="vaultx-doctest")
```

## Generate Static Account OAuth2 Access Token

`vaultx.api.secrets_engines.Gcp.generate_static_account_oauth2_access_token(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

token_response = client.secrets.gcp.generate_static_account_oauth2_access_token(
  name="vaultx-doctest",
)
```

## Generate Static Account Service Account Key

`vaultx.api.secrets_engines.Gcp.generate_static_account_service_account_key(name, key_algorithm='KEY_ALG_RSA_2048', key_type='TYPE_GOOGLE_CREDENTIALS_FILE', method='POST', mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

key_response = client.secrets.gcp.generate_static_account_service_account_key(
  name="vaultx-doctest",
)
```

## Create Or Update Impersonated Account

`vaultx.api.secrets_engines.Gcp.create_or_update_impersonated_account(name, service_account_email, token_scopes=None, ttl=None, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

create_response = client.secrets.gcp.create_or_update_impersonated_account(
  name="vaultx-doctest",
  service_account_email="vaultx-doctest@some-gcp-project-id.iam.gserviceaccount.com",
  token_scopes=["https://www.googleapis.com/auth/cloud-platform"],
  ttl='4h'
)
```

## Read Impersonated Account

`vaultx.api.secrets_engines.Gcp.read_impersonated_account(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

read_response = client.secrets.gcp.read_impersonated_account(name="vaultx-doctest")
```

## List Impersonated Accounts

`vaultx.api.secrets_engines.Gcp.list_impersonated_accounts(mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

list_response = client.secrets.gcp.list_impersonated_accounts()
```

## Delete Impersonated Account

`vaultx.api.secrets_engines.Gcp.delete_impersonated_account(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

delete_response = client.secrets.gcp.delete_impersonated_account(name="vaultx-doctest")
```

## Generate Impersonated Account OAuth2 Access Token

`vaultx.api.secrets_engines.Gcp.generate_impersonated_account_oauth2_access_token(name, mount_point='gcp')`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

token_response = client.secrets.gcp.generate_impersonated_account_oauth2_access_token(
  name="vaultx-doctest",
)
```
