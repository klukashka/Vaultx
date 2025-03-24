# Okta

>**Note**: Every method under the Client class's okta attribute includes a mount_point parameter that can be used to address the Okta auth method under a custom mount path. E.g., If enabling the Okta auth method using Vault’s CLI commands via vault secret enable -path=my-okta okta”, the mount_point parameter in Source reference: vaultx.api.auth_methods.Okta() methods would be set to “my-okta”.

## Enabling the Auth Method

`vaultx.v1.client.sys.enable_secrets_engine()`

```python3
import vaultx
client = vaultx.Client()

okta_path = 'company-okta'
description = 'Auth method for use by team members in our company'

if f"{okta_path}" not in client.sys.list_auth_methods()['data']:
    print(f'Enabling the okta secret backend at mount_point: {okta_secret_path}')
    client.sys.enable_auth_method(
        method_type='okta',
        description=description,
        path=okta_secret_path,
    )
```

## Configure

`vaultx.api.auth_methods.Okta.configure()`

```python3
import vaultx
client = vaultx.Client()

client.auth.okta.configure(
    org_name='vaultx-project'
)
```

## Read Config

`vaultx.api.auth_methods.Okta.read_config()`

```python3
import vaultx
client = vaultx.Client()

okta_config = client.auth.okta.read_config()
print('The Okta auth method at path /okta has a configured organization name of: {name}'.format(
    name=okta_config['data']['org_name'],
))
```

## List Users

`vaultx.api.auth_methods.Okta.list_users()`

```python3
import vaultx
client = vaultx.Client()

users = client.auth.okta.list_users()
print(f'The following Okta users are registered: {",".join(users['data']['keys'])}')
```

## Register User

`vaultx.api.auth_methods.Okta.register_user()`

```python3
import vaultx
client = vaultx.Client()

client.auth.okta.register_user(
    username='vaultx-person',
    policies=['vaultx-admin'],
)
```

## Read User

`vaultx.api.auth_methods.Okta.read_user()`

```python3
import vaultx
client = vaultx.Client()

read_user = client.auth.okta.read_user(
    username='vaultx-person',
)
print('Okta user "{name}" has the following attached policies: {policies}'.format(
    name='vaultx-person',
    policies=', '.join(read_user['data']['policies']),
))
```

## Delete User

`vaultx.api.auth_methods.Okta.delete_user()`

```python3
import vaultx
client = vaultx.Client()

client.auth.okta.delete_user(
    username='vaultx-person'
)
```

## List Groups

`vaultx.api.auth_methods.Okta.list_groups()`

```python3
import vaultx
client = vaultx.Client()

groups = client.auth.okta.list_groups()
print('The following Okta groups are registered: {groups}'.format(
    groups=','.join(groups['data']['keys']),
))
```

## Register Group

`vaultx.api.auth_methods.Okta.register_group()`

```python3
import vaultx
client = vaultx.Client()

client.auth.okta.register_group(
    name='vaultx-group',
    policies=['vaultx-group-members'],
)
```

## Read Group

`vaultx.api.auth_methods.Okta.read_group()`

```python3
import vaultx
client = vaultx.Client()

read_group = client.auth.okta.read_group(
    name='vaultx-group',
)
print('Okta group "{name}" has the following attached policies: {policies}'.format(
    name='vaultx-group',
    policies=', '.join(read_group['data']['policies']),
))
```

## Delete Group

`vaultx.api.auth_methods.Okta.delete_group()`

```python3
import vaultx
client = vaultx.Client()

client.auth.okta.delete_group(
    name='vaultx-group',
)
```

## Login

`vaultx.api.auth_methods.Okta.login()`

```python3
from getpass import getpass

import vaultx
client = vaultx.Client()


password_prompt = 'Please enter your password for the Okta authentication backend: '
okta_password = getpass(prompt=password_prompt)

client.auth.okta.login(
    username='vaultx-person',
    password=okta_password,
)
```
