# LDAP

## Configure LDAP Secrets Engine

`vaultx.api.secrets_engines.LDAP.configure()`

Configure the LDAP secrets engine to either manage service accounts or service account libraries.

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

# Not all these settings may apply to your setup, refer to Vault
# documentation for context of what to use here

config_response = client.secrets.ldap.configure(
    binddn='username@domain.fqdn',  # A UPN or DN can be used for this value, Vault resolves the user to a DN silently
    bindpass='***********',
    url='ldaps://domain.fqdn',
    userdn='cn=Users,dn=domain,dn=fqdn',
    upndomain='domain.fqdn',
    userattr="cn",
    schema="openldap"
)
print(config_response)
```

## Read Config

`vaultx.api.secrets_engines.LDAP.read_config()`

Return the LDAP Secret Engine configuration.

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

config_response = client.secrets.ldap.read_config()
print(config_response)
```

## Rotate Root

`vaultx.api.secrets_engines.LDAP.rotate_root()`

Rotate the password for the `binddn` entry used to manage LDAP. This generated password will only be known to Vault and will not be retrievable once rotated.

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

rotate_response = client.secrets.ldap.rotate_root()
print(rotate_response)
```

## Create or Update Static Role

`vaultx.api.secrets_engines.LDAP.create_or_update_static_role()`

Create or update a role which allows the retrieval and rotation of an LDAP account. Retrieve and rotate the actual credential via `generate_static_credentials()`.

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

role_response = client.secrets.ldap.create_or_update_static_role(
    name='vaultx-role',
    username='sql-service-account',
    dn='cn=sql-service-account,dc=petshop,dc=com',
    rotation_period="60s"
)
print(role_response)
```

## Read Static Role

`vaultx.api.secrets_engines.LDAP.read_static_role()`

Retrieve the role configuration which allows the retrieval and rotation of an LDAP account. Retrieve and rotate the actual credential via `generate_static_credentials()`.

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

role_response = client.secrets.ldap.read_static_role(name='vaultx-role')
print(role_response)
```

## List Static Roles

`vaultx.api.secrets_engines.LDAP.list_static_roles()`

List all configured roles which allow the retrieval and rotation of an LDAP account. Retrieve and rotate the actual credential via `generate_static_credentials()`.

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

all_static_roles = client.secrets.ldap.list_static_roles()
print(all_static_roles)
```

## Delete Static Role

`vaultx.api.secrets_engines.LDAP.delete_static_role()`

Remove the role configuration which allows the retrieval and rotation of an LDAP account.

**Note**: Passwords are not rotated upon deletion of a static role. The password should be manually rotated prior to deleting the role or revoking access to the static role.

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

deletion_response = client.secrets.ldap.delete_static_role(name='vaultx-role')
print(deletion_response)
```

## Generate Static Credentials

`vaultx.api.secrets_engines.LDAP.generate_static_credentials()`

Retrieve a service account password from LDAP. Return the previous password (if known). Vault shall rotate the password before returning it if it has breached its configured TTL.

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

gen_creds_response = client.secrets.ldap.generate_static_credentials(
    name='vaultx-role',
)
print('Retrieved Service Account Password: {access} (Current) / {secret} (Old)'.format(
    access=gen_creds_response['data']['current_password'],
    secret=gen_creds_response['data']['old_password'],
))
```

## Rotate Static Credentials

`vaultx.api.secrets_engines.LDAP.rotate_static_credentials()`

Manually rotate the password of an existing role.

```python3
import vaultx
client = vaultx.Client()

# Authenticate to Vault using client.auth.x

rotate_response = client.secrets.ldap.rotate_static_credentials(name='vaultx-role')
print(rotate_response)
```
