# Azure

>>**Note**: Every method under the Azure class includes a mount_point parameter that can be used to address the Azure secret engine under a custom mount path. E.g., If enabling the Azure secret engine using Vault’s CLI commands via vault secrets enable -path=my-azure azure”, the mount_point parameter in vaultx.api.secrets_engines.Azure() methods would need to be set to “my-azure”.

## Configure

`vaultx.api.secrets_engines.Azure.configure()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.azure.configure(
    subscription_id='my-subscription-id',
    tenant_id='my-tenant-id',
)
```

## Read Config

`vaultx.api.secrets_engines.Azure.read_config()`

```python3
import vaultx
client = vaultx.Client()

azure_secret_config = client.secrets.azure.read_config()
print('The Azure secret engine is configured with a subscription ID of {id}'.format(
    id=azure_secret_config['subscription_id'],
))
```

## Delete Config

`vaultx.api.secrets_engines.Azure.delete_config()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.azure.delete_config()
```

## Create Or Update A Role

`vaultx.api.secrets_engines.Azure.create_or_update_role()`

```python3
import vaultx
client = vaultx.Client()


azure_roles = [
    {
        'role_name': "Contributor",
        'scope': "/subscriptions/95e675fa-307a-455e-8cdf-0a66aeaa35ae",
    },
]
client.secrets.azure.create_or_update_role(
    name='my-azure-secret-role',
    azure_roles=azure_roles,
)
```

## List Roles

`vaultx.api.secrets_engines.Azure.list_roles()`

```python3
import vaultx
client = vaultx.Client()

azure_secret_engine_roles = client.secrets.azure.list_roles()
print(f'The following Azure secret roles are configured: {",".join(roles['keys'])}')
```

## Generate Credentials

`vaultx.api.secrets_engines.Azure.generate_credentials()`

```python3
import vaultx
from azure.common.credentials import ServicePrincipalCredentials

client = vaultx.Client()
azure_creds = client.secrets.azure.secret.generate_credentials(
    name='some-azure-role-name',
)
azure_spc = ServicePrincipalCredentials(
    client_id=azure_creds['client_id'],
    secret=azure_creds['client_secret'],
    tenant=TENANT_ID,
)
```
