# LDAP

>**Note**: Every method under the Client class's ldap attribute includes a mount_point parameter that can be used to address the LDAP auth method under a custom mount path. E.g., If enabling the LDAP auth method using Vault’s CLI commands via vault auth enable -path=my-ldap ldap”, the mount_point parameter in vaultx.api.auth_methods.Ldap() methods would be set to “my-ldap”.

## Enabling the LDAP Auth Method

`vaultx.api.SystemBackend.enable_auth_method()`

```python3
import vaultx
client = vaultx.Client()

ldap_auth_path = 'company-ldap'
description = "Auth method for use by team members in our company's LDAP organization"

if f'{ldap_auth_path}/' not in client.sys.list_auth_methods()['data']:
    print(f'Enabling the ldap auth backend at mount_point: {ldap_auth_path}')
    client.sys.enable_auth_method(
        method_type='ldap',
        description=description,
        path=ldap_auth_path,
    )
```

## Configure LDAP Auth Method Settings

`vaultx.api.auth_methods.Ldap.configure()`

```python3
import vaultx
client = vaultx.Client()

client.auth.ldap.configure(
    user_dn='dc=users,dc=vaultx,dc=network',
    group_dn='ou=groups,dc=vaultx,dc=network',
    url='ldaps://ldap.vaultx.network:12345',
    bind_dn='cn=admin,dc=vaultx,dc=network',
    bind_pass='ourverygoodadminpassword',
    user_attr='uid',
    group_attr='cn',
)
```

## Reading the LDAP Auth Method Configuration

`vaultx.api.auth_methods.Ldap.read_configuration()`

```python3
import vaultx
client = vaultx.Client()

ldap_configuration = client.auth.ldap.read_configuration()
print(f'The LDAP auth method is configured with a LDAP server URL of: {ldap_configuration['data']['url']}')
```

## Create or Update an LDAP Group Mapping

`vaultx.api.auth_methods.Ldap.create_or_update_group()`

```python3
import vaultx
client = vaultx.Client()

client.auth.ldap.create_or_update_group(
    name='some-dudes',
    policies=['policy-for-some-dudes'],
)
```

## List LDAP Group Mappings

`vaultx.api.auth_methods.Ldap.list_groups()`

```python3
import vaultx
client = vaultx.Client()

ldap_groups = client.auth.ldap.list_groups()
print(f'The following groups are configured in the LDAP auth method: {",".join(ldap_groups['data']['keys'])}')
```

## Read LDAP Group Mapping

`vaultx.api.auth_methods.Ldap.read_group()`

```python3
import vaultx
client = vaultx.Client()

some_dudes_ldap_group = client.auth.ldap.read_group(
    name='somedudes',
)
print('The "somedudes" group in the LDAP auth method are mapped to the following policies: {policies}'.format(
    policies=','.join(some_dudes_ldap_group['data']['policies'])
))
```

## Deleting a LDAP Group Mapping

`vaultx.api.auth_methods.Ldap.delete_group()`

```python3
import vaultx
client = vaultx.Client()

client.auth.ldap.delete_group(
    name='some-group',
)
```

## Creating or Updating a LDAP User Mapping

`vaultx.api.auth_methods.Ldap.create_or_update_user()`

```
import vaultx
client = vaultx.Client()

client.auth.ldap.create_or_update_user(
    username='somedude',
    policies=['policy-for-some-dudes'],
)
```

## Listing LDAP User Mappings

`vaultx.api.auth_methods.Ldap.list_users()`

```python3
import vaultx
client = vaultx.Client()

ldap_users = client.auth.ldap.list_users()
print('The following users are configured in the LDAP auth method: {users}'.format(
    users=','.join(ldap_users['data']['keys'])
)
```

## Reading a LDAP User Mapping

`vaultx.api.auth_methods.Ldap.read_user()`

```python3
import vaultx
client = vaultx.Client()

some_dude_ldap_user = client.auth.ldap.read_user(
    username='somedude'
)
print('The "somedude" user in the LDAP auth method is mapped to the following policies: {policies}'.format(
    policies=','.join(some_dude_ldap_user['data']['policies'])
)
```

## Deleting a Configured User Mapping

`vaultx.api.auth_methods.Ldap.delete_user()`

```python3
import vaultx
client = vaultx.Client()

client.auth.ldap.delete_user(
    username='somedude',
)
```

## Authentication / Login

`vaultx.api.auth_methods.Ldap.login_with_user()`

For an LDAP backend mounted under a non-default (ldap) path. E.g., via Vault CLI with vault auth enable -path=prod-ldap ldap

```python3
from getpass import getpass

import vaultx

service_account_username = 'someuser'
password_prompt = 'Please enter your password for the LDAP authentication backend: '
service_account_password = getpass(prompt=password_prompt)

client = vaultx.Client()

# Here the mount_point parameter corresponds to the path provided when enabling the backend
client.auth.ldap.login(
    username=service_account_username,
    password=service_account_password,
    mount_point='prod-ldap'
)
print(client.is_authenticated())  # => True
```
