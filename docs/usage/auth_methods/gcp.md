# GCP

>**Note**: Every method under the Client class's gcp.auth attribute includes a mount_point parameter that can be used to address the GCP auth method under a custom mount path. E.g., If enabling the GCP auth method using Vault’s CLI commands via vault auth enable -path=my-gcp gcp”, the mount_point parameter in vaultx.api.auth.Gcp() methods would be set to “my-gcp”.

## Enabling the Auth Method

`vaultx.api.SystemBackend.enable_auth_method()`

```python3
import vaultx
client = vaultx.Client()

gcp_auth_path = 'company-gcp'
description = 'Auth method for use by team members in our company'

if f"{gcp_auth_path}/" not in vault_client.sys.list_auth_methods()['data']:
    print(f'Enabling the gcp auth backend at mount_point: {gcp_auth_path}')
    client.sys.enable_auth_method(
        method_type='gcp',
        description=description,
        path=gcp_auth_path,
    )
```

## Configure

`vaultx.api.auth.Gcp.configure()`

```python3
import vaultx
client = vaultx.Client()

client.auth.gcp.configure(
    credentials='some signed JSON web token for the Vault server...'
)
```

## Read Config

`vaultx.api.auth.Gcp.read_config()`

```python3
import vaultx
client = vaultx.Client()

read_config = client.auth.gcp.read_config()
print('The configured project_id is: {id}'.format(id=read_config['project_id'))
```

## Delete Config

`vaultx.api.auth.Gcp.delete_config()`

```python3
import vaultx
client = vaultx.Client()

client.auth.gcp.delete_config()
```

## Create Role

`vaultx.api.auth.Gcp.create_role()`

```python3
import vaultx
client = vaultx.Client()

client.auth.gcp.create_role(
        name='some-gcp-role-name',
        role_type='iam',
        project_id='some-gcp-project-id',
        bound_service_accounts=['*'],
)
```

## Edit Service Accounts On IAM Role

`vaultx.api.auth.Gcp.edit_service_accounts_on_iam_role()`

```python3
import vaultx
client = vaultx.Client()

client.gcp.edit_service_accounts_on_iam_role(
            name='some-gcp-role-name',
    add=['vaultx@appspot.gserviceaccount.com'],
)

client.gcp.edit_service_accounts_on_iam_role(
            name='some-gcp-role-name',
    remove=['disallowed-service-account@appspot.gserviceaccount.com'],
)
```

## Edit Labels On GCE Role

`vaultx.api.auth.Gcp.edit_labels_on_gce_role()`

```python3
import vaultx
client = vaultx.Client()

client.gcp.edit_labels_on_gce_role(
            name='some-gcp-role-name',
    add=['some-key:some-value'],
)

client.gcp.edit_labels_on_gce_role(
            name='some-gcp-role-name',
    remove=['some-bad-key:some-bad-value'],
)
```

## Read A Role

`vaultx.api.auth.Gcp.read_role()`

```python3
import vaultx
client = vaultx.Client()

read_role_response = client.gcp.read_role(
    name=role_name,
)

print('Policies for role "{name}": {policies}'.format(
    name='my-role',
    policies=','.join(read_role_response['policies']),
))
```

## List Roles

`vaultx.api.auth.Gcp.list_roles()`
```python3
import vaultx
client = vaultx.Client()

roles = client.auth.gcp.list_roles()
print('The following GCP auth roles are configured: {roles}'.format(
    roles=','.join(roles['keys']),
))
```

## Delete A Role

`vaultx.api.auth.Gcp.delete_role()`

```python3
import vaultx
client = vaultx.Client()

client.gcp.delete_role(
)
```

## Login

`vaultx.api.auth.Gcp.login()`

```python3
import vaultx
client = vaultx.Client()

client.gcp.login(
    role=role_name,
    jwt='some signed JSON web token...',
)
print(client.is_authenticated)
```

## Example with google-api-python-client Usage

```python3
import time

import googleapiclient.discovery # pip install google-api-python-client
from google.oauth2 import service_account # pip install google-auth
import vaultx # pip install vaultx

# First load some previously generated GCP service account key
path_to_sa_json = 'some-service-account-path.json'
credentials = service_account.Credentials.from_service_account_file(path_to_sa_json)
with open(path_to_sa_json, 'r') as f:
    creds = json.load(f)
    project = creds['project_id']
    service_account = creds['client_email']

# Generate a payload for subsequent "signJwt()" call
# Reference: https://google-auth.readthedocs.io/en/latest/reference/google.auth.jwt.html#google.auth.jwt.Credentials
now = int(time.time())
expires = now + 900  # 15 mins in seconds, can't be longer.
payload = {
    'iat': now,
    'exp': expires,
    'sub': service_account,
    'aud': 'vault/my-role'
}
body = {'payload': json.dumps(payload)}
name = f'projects/{project}/serviceAccounts/{service_account}'

# Perform the GCP API call
iam = googleapiclient.discovery.build('iam', 'v1', credentials=credentials)
request = iam.projects().serviceAccounts().signJwt(name=name, body=body)
resp = request.execute()
jwt = resp['signedJwt']

# Perform vaultx call to configured GCP auth method
client.auth.gcp.login(
    role='my-role',
    jwt=jwt,
)
```
