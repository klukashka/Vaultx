# Active Directory

## Configure AD Secrets Engine

Configure the AD secrets engine to either manage service accounts or service account libraries.

`vaultx.api.secrets_engines.ActiveDirectory.configure()`

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

# Not all these settings may apply to your setup, refer to Vault
# documentation for context of what to use here

config_response = client.secrets.ActiveDirectory.configure(
    binddn='username@domain.fqdn', # An upn or DN can be used for this value, Vault resolves the user to a dn silently
    bindpass='***********',
    url='ldaps://domain.fqdn',
    userdn='CN=Users,DN=domain,DN=fqdn',
    upndomain='domain.fqdn',
    ttl=60,
    max_ttl=120
)
print(config_response)
```

## Read Config

Return the AD Secret Engine configuration.

`vaultx.api.secrets_engines.ActiveDirectory.read_config()`

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

config_response = client.secrets.ActiveDirectory.read_config()
```

## Create or Update Role

Create or Update a role which allows the retrieval and rotation of an AD account. Retrieve and rotate the actual credential via generate_credentials().

`vaultx.api.secrets_engines.ActiveDirectory.create_or_update_role()`

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

role_response = client.secrets.ActiveDirectory.create_or_update_role(
    name='sql-service-account',
    service_account_name='svc-sqldb-petshop@domain.fqdn',
    ttl=60)
```
## Read Role

Retrieve the role configuration which allows the retrieval and rotation of an AD account. Retrieve and rotate the actual credential via generate_credentials().

`vaultx.api.secrets_engines.ActiveDirectory.read_role()`

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

role_response = client.secrets.ActiveDirectory.read_role(name='sql-service-account')
```

## List Roles

List all configured roles which allows the retrieval and rotation of an AD account. Retrieve and rotate the actual credential via generate_credentials().

`vaultx.api.secrets_engines.ActiveDirectory.list_roles()`

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

all_roles = client.secrets.ActiveDirectory.list_roles()
```

## Delete Role

Remove the role configuration which allows the retrieval and rotation of an AD account.

The account is retained in Active Directory, but the password will be whatever Vault had rotated it to last. To regain control, the password will need to be reset via Active Directory.

`vaultx.api.secrets_engines.ActiveDirectory.delete_role()`

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

deletion_response = client.secrets.ActiveDirectory.delete_role(name='sql-service-account')
```

## Generate Credentials

Retrieve a service account password from AD. Return the previous password (if known). Vault shall rotate the password before returning it, if it has breached its configured ttl.

`vaultx.api.secrets_engines.ActiveDirectory.generate_credentials()`

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

gen_creds_response = client.secrets.ActiveDirectory.generate_credentials(
    name='vaultx-role',
)

access = gen_creds_response['data']['current_password']
secret = gen_creds_response['data']['old_password']

print(f'Retrieved Service Account Password: {access} (Current) / {secret} (Old)')
```
