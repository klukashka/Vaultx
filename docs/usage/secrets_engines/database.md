# Database

>>**Note**: Every method under the Database class includes a mount_point parameter that can be used to address the Database secret engine under a custom mount path. E.g., If enabling the Database secret engine using Vault’s CLI commands via vault secrets enable -path=my-database database, the mount_point parameter in vaultx.api.secrets_engines.Database() methods would be set to my-database.

## Enable Database Secrets Engine

```python3
import vaultx
client = vaultx.Client()

client.sys.enable.secrets_engine(
    backend_type='database',
    path='my-database'
)
```

>>**Note**: Example code below is for configuring and connecting to Postgres. See the official developer docs for a list of supported database plugins and detailed configuration requirements.

## Configuration

`vaultx.api.secrets_engines.Database.configure()`

Configures the database engine:

```python3
import vaultx
client = vaultx.Client()

client.secrets.database.configure(
    name='db-connection-name',
    plugin_name='postgresql-database-plugin',
    allowed_roles='role-name',
    connection_url=f'postgresql://{{{{username}}}}:{{{{password}}}}@postgres:5432/postgres?sslmode=disable',
    username='db-username',
    password='db-password',
)
```

>>**Note**: The database needs to be created and available to connect before you can configure the database secrets engine using the above configure method.

## Read Configuration

`vaultx.api.secrets_engines.Database.read_connection()`

Returns the configuration settings for a connection mounted under a path of my-database:

```python3
import vaultx
client = vaultx.Client()

connection_config = client.secrets.database.read_connection(
    name='db-connection-name',
    mount_point='my-database'
)
```

## List Connections

`vaultx.api.secrets_engines.Database.list_connections()`

Returns a list of available connections:

```python3
import vaultx
client = vaultx.Client()

connections = client.secrets.database.list_connections(
    mount_point='my-database'
)
```

## Delete Connection

`vaultx.api.secrets_engines.Database.delete_connection()`

Deletes a connection:

```python3
import vaultx
client = vaultx.Client()

client.secrets.database.delete_connection(
    name='db-connection-name',
    mount_point='my-database'
)
```

## Reset Connection

`vaultx.api.secrets_engines.Database.reset_connection()`

Closes a connection and its underlying plugin and restarts it with the configuration stored:

```python3
import vaultx
client = vaultx.Client()

client.secrets.database.reset_connection(
    name='db-connection-name',
    mount_point='my-database'
)
```

## Create Role

`vaultx.api.secrets_engines.Database.create_role()`

Creates or updates a role definition:

```python3
import vaultx
client = vaultx.Client()

# SQL to create a new user with read only role to public schema
creation_statements = [
    "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
    "GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"
]

# Create a new role for the PostgreSQL connection
client.secrets.database.create_role(
    name='role-name',
    db_name='db-connection-name',
    creation_statements=creation_statements,
    default_ttl='1h',
    max_ttl='24h',
    mount_point='my-database'
)
```

## Read A Role

`vaultx.api.secrets_engines.Database.read_role()`

Creates or updates a role definition:

```python3
import vaultx
client = vaultx.Client()

role = client.secrets.database.read_role(
    name='role-name',
    mount_point='my-database'
)
```

## List All The Roles

`vaultx.api.secrets_engines.Database.list_roles()`

Returns a list of available roles:

```python3
import vaultx
client = vaultx.Client()

roles = client.secrets.database.list_roles(
    mount_point='my-database'
)
```
## Delete A Role

`vaultx.api.secrets_engines.Database.delete_role()`

Deletes a role definition:

```python3
import vaultx
client = vaultx.Client()

client.secrets.database.delete_role(
    name='role-name',
    mount_point='my-database'
)
```

## Rotate Root Credentials

`vaultx.api.secrets_engines.Database.rotate_root_credentials()`

Rotates the root credentials stored for the database connection. This user must have permissions to update its own password.

```python3
import vaultx
client = vaultx.Client()

client.secrets.database.rotate_root_credentials(
    name='db-connection-name',
    mount_point='my-database'
)
```

## Generate Credentials

`vaultx.api.secrets_engines.Database.generate_credentials()`

Generates a new set of dynamic credentials based on the named role:

```python3
import vaultx
client = vaultx.Client()

credentials = client.secrets.database.generate_credentials(
    name='role-name',
    mount_point='my-database'
)
```

## Get Static Credentials

`vaultx.api.secrets_engines.Database.get_static_credentials()`

Returns the current credentials based on the named static role:

```python3
import vaultx
client = vaultx.Client()

credentials = client.secrets.database.get_static_credentials(
    name='role-name',
    mount_point='my-database'
)
```

## Create Static Role

`vaultx.api.secrets_engines.Database.create_static_role()`

Creates or updates a static role:

```python3
import vaultx
client = vaultx.Client()

rotation_statement = ["ALTER USER \"{{name}}\" WITH PASSWORD '{{password}}';"]

credentials = client.secrets.database.create_static_role(
    name='role-name',
    db_name='db-connection-name',
    username='static-role-username', 
    rotation_statements=rotation_statement,
    rotation_period=86400,
    mount_point='my-database', 
)
```

>>**Note**: The username referenced above needs to be pre-created in the database prior to calling this method as Vault will be referencing this username to rotate its password.

## Read Static Role

`vaultx.api.secrets_engines.Database.read_static_role()`

Queries a static role definition:

```python3
import vaultx
client = vaultx.Client()

client.secrets.database.read_static_role(
    name='role-name',
    mount_point='my-database'
)
```

## List Static Roles

`vaultx.api.secrets_engines.Database.list_static_roles()`

Returns a list of available static roles:

```python3
import vaultx
client = vaultx.Client()

static_roles = client.secrets.database.list_static_roles(
    mount_point='my-database'
)
```

## Rotate Static Role Credentials

`vaultx.api.secrets_engines.Database.rotate_static_role_credentials()`

This endpoint is used to rotate the Static Role credentials stored for a given role name. While Static Roles are rotated automatically by Vault at configured rotation periods, users can use this endpoint to manually trigger a rotation to change the stored password and reset the TTL of the Static Role’s password.

```python3
import vaultx
client = vaultx.Client()

client.secrets.database.rotate_static_role_credentials(
    name='role-name',
    mount_point='my-database'
)
```
