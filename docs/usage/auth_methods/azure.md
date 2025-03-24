# Azure

>**Note**: Every method under the Client class's azure attribute includes a mount_point parameter that can be used to address the Azure auth method under a custom mount path. E.g., If enabling the Azure auth method using Vault’s CLI commands via vault auth enable -path=my-azure azure”, the mount_point parameter in vaultx.api.auth_methods.Azure() methods would be set to “my-azure”.

## Enabling the Auth Method

`vaultx.api.SystemBackend.enable_auth_method()`

```python3
import vaultx
client = vaultx.Client()

azure_auth_path = 'company-azure'
description = 'Auth method for use by team members in our company'

if f"{azure_auth_path}/" not in client.sys.list_auth_methods()['data']:
    print(f'Enabling the azure auth backend at mount_point: {azure_auth_path}'
    client.sys.enable_auth_method(
        method_type='azure',
        description=description,
        path=azure_auth_path,
    )
```

## Configure

`vaultx.api.auth_methods.Azure.configure()`

```python3
import os
import vaultx
client = vaultx.Client()

client.auth.azure.configure(
    tenant_id='my-tenant-id', 
    resource='my-resource',
    client_id=os.environ.get('AZURE_CLIENT_ID'),
    client_secret=os.environ.get('AZURE_CLIENT_SECRET'),
)
```

## Read Config

```python3
vaultx.api.auth_methods.Azure.read_config()

import vaultx
client = vaultx.Client()

read_config = client.auth.azure.read_config()
print(f'The configured tenant_id is: {read_config['tenant_id']}')
```

## Delete Config

`vaultx.api.auth_methods.Azure.delete_config()`

```python3
import vaultx
client = vaultx.Client()

client.auth.azure.delete_config()
```

## Create a Role

`vaultx.api.auth_methods.Azure.create_role()`

```python3
import vaultx
client = vaultx.Client()

client.auth.azure.create_role(
    name='my-role',
    policies=policies,
    bound_service_principal_ids=bound_service_principal_ids,
)
```

## Read A Role

`vaultx.api.auth_methods.Azure.read_role()`

```python3
import vaultx
client = vaultx.Client()

role_name = 'my-role'
read_role_response = client.auth.azure.read_role(
    name=role_name,
)
print('Policies for role "{name}": {policies}'.format(
    name='my-role',
    policies=','.join(read_role_response['policies']),
))
```

## List Roles

`vaultx.api.auth_methods.Azure.list_roles()`

```python3
import vaultx
client = vaultx.Client()

roles = client.auth.azure.list_roles()
print('The following Azure auth roles are configured: {roles}'.format(
    roles=','.join(roles['keys']),
))
```

## Delete A Role

`vaultx.api.auth_methods.Azure.delete_role()`

```python3
import vaultx
client = vaultx.Client()

client.auth.azure.delete_role(
    name='my-role',
)
```

## Login

`vaultx.api.auth_methods.Azure.login()`

```python3
import vaultx
client = vaultx.Client()

client.auth.azure.login(
    role=role_name,
    jwt='Some MST JWT...',
)
```
