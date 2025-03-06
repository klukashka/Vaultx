# KV - Version 2

>**Note**:
> Every method under the `Kv class's v2 attribute` includes a _mount_point_ parameter that can be used 
> to address the KvV2 secret engine under a custom mount path. 
> E.g., If enabling the KvV2 secret engine using Vault’s CLI commands via _vault secrets enable 
> "-path=my-kvv2 -version=2 kv"_, the _mount_point_ parameter in `vaultx.api.secrets_engines.KvV2()` methods would be set to "my-kvv2".

## Configuration

`vaultx.api.secrets_engines.KvV2.configure()`

Setting the default _max_versions_ for a key/value engine version 2 under a path of _kv_:

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.configure(
    max_versions=20,
    mount_point='kv',
)
```

Setting the default _cas_required_ (check-and-set required) flag under the implicit default path of _secret_:

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.configure(
    cas_required=True,
)
```

## Read Configuration

`vaultx.api.secrets_engines.KvV2.configure()`

Reading the configuration of a KV version 2 engine mounted under a path of _kv_:

```python3
import vaultx
client = vaultx.Client()

kv_configuration = client.secrets.kv.v2.read_configuration(
    mount_point='kv',
)

max_ver = kv_configuration['data']['max_versions']
print(f'Config under path "kv": max_versions set to "{max_ver}"')

cas = kv_configuration['data']['cas_required']
print('Config under path "kv": check-and-set require flag set to {cas}')

```

## Read Secret Versions

`vaultx.api.secrets_engines.KvV2.read_secret_version()`

Read the latest version of a given secret/path (“vaultx”):

```python3
import vaultx
client = vaultx.Client()

secret_version_response = client.secrets.kv.v2.read_secret_version(
    path='vaultx',
)

data = secret_version_response['data']['data'].keys()
print(f'Latest version of secret under path "vaultx" contains the following keys: {data}')

date = secret_version_response['data']['metadata']['created_time']
print(f'Latest version of secret under path "vaultx" created at: {date}')

ver = secret_version_response['data']['metadata']['version']
print(f'Latest version of secret under path "vaultx" is version #{ver}')
```

Read specific version (1) of a given secret/path (“vaultx”):

```python3
import vaultx
client = vaultx.Client()

secret_version_response = client.secrets.kv.v2.read_secret_version(
    path='vaultx',
    version=1,
)

data = secret_version_response['data']['data'].keys()
print(f'Version 1 of secret under path "vaultx" contains the following keys: {data}')

date = secret_version_response['data']['metadata']['created_time']
print(f'Version 1 of secret under path "vaultx" created at: {date}')
```

## Create/Update Secret

`vaultx.api.secrets_engines.KvV2.create_or_update_secret()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.create_or_update_secret(
    path='vaultx',
    secret=dict(pssst='this is secret'),
)
```

_cas_ parameter with an argument that doesn’t match the current version:

```python3
import vaultx
client = vaultx.Client()

# Assuming a current version of "6" for the path "vaultx" =>
client.secrets.kv.v2.create_or_update_secret(
    path='vaultx',
    secret=dict(pssst='this is secret'),
    cas=5,
)  # Raises vaultx.exceptions.InvalidRequest
```

_cas_ parameter set to 0 will only succeed if the path hasn’t already been written.

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.create_or_update_secret(
    path='vaultx',
    secret=dict(pssst='this is secret #1'),
    cas=0,
)

client.secrets.kv.v2.create_or_update_secret(
    path='vaultx',
    secret=dict(pssst='this is secret #2'),
    cas=0,
)  # => Raises VaultxError with 400 status code
```

# Patch Existing Secret

Method (similar to the Vault CLI command _vault kv patch_) to update an existing path. 
Either to add a new key/value to the secret and/or update the value for an existing key. 
Raises a VaultxError if the path hasn’t been written to previously.

`vaultx.api.secrets_engines.KvV2.patch()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.patch(
    path='vaultx',
    secret=dict(pssst='this is a patched secret'),
)
```

## Delete Latest Version of Secret

`vaultx.api.secrets_engines.KvV2.delete_latest_version_of_secret()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.delete_latest_version_of_secret(
    path=vaultx,
)
```

## Delete Secret Versions

`vaultx.api.secrets_engines.KvV2.delete_secret_versions()`

Marking the first 3 versions of a secret deleted under path “vaultx”:

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.delete_secret_versions(
    path='vaultx',
    versions=[1, 2, 3],
)
```

## Undelete Secret Version

`vaultx.api.secrets_engines.KvV2.undelete_secret_versions()`

Marking the last 3 versions of a secret deleted under path “vaultx” as “undeleted”:

```python3
import vaultx
client = vaultx.Client()

vaultx_path_metadata = client.secrets.kv.v2.read_secret_metadata(
    path='vaultx',
)

oldest_version = vaultx_path_metadata['data']['oldest_version']
current_version = vaultx_path_metadata['data']['current_version']
versions_to_undelete = range(max(oldest_version, current_version - 2), current_version + 1)

client.secrets.kv.v2.undelete_secret_versions(
    path='vaultx',
    versions=versions_to_undelete,
)
```

## Destroy Secret Versions

`vaultx.api.secrets_engines.KvV2.destroy_secret_versions()`

Destroying the first three versions of a secret under path ‘vaultx’:

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.destroy_secret_versions(
    path='vaultx',
    versions=[1, 2, 3],
)
```

## List Secrets

`vaultx.api.secrets_engines.KvV2.list_secrets()`

Listing secrets under the ‘vaultx’ path prefix:

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.create_or_update_secret(
    path='vaultx/big-ole-secret',
    secret=dict(pssst='this is a large secret'),
)

client.secrets.kv.v2.create_or_update_secret(
    path='vaultx/lil-secret',
    secret=dict(pssst='this secret... not so big'),
)

list_response = client.secrets.kv.v2.list_secrets(
    path='vaultx',
)

print('The following paths are available under "vaultx" prefix: {keys}'.format(
    keys=','.join(list_response['data']['keys']),
))
```

## Read Secret Metadata

`vaultx.api.secrets_engines.KvV2.read_secret_metadata()`

```python3
import vaultx
client = vaultx.Client()

vaultx_path_metadata = client.secrets.kv.v2.read_secret_metadata(
    path='vaultx',
)

print('Secret under path vaultx is on version {cur_ver}, with an oldest version of {old_ver}'.format(
    cur_ver=vaultx_path_metadata['data']['oldest_version'],
    old_ver=vaultx_path_metadata['data']['current_version'],
))
```

## Update Metadata

`vaultx.api.secrets_engines.KvV2.update_metadata()`

Set max versions for a given path (“vaultx”) to 3:

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.update_metadata(
    path='vaultx',
    max_versions=3,
)
```

Set cas (check-and-set) parameter as required for a given path (“vaultx”):

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.update_metadata(
    path='vaultx',
    cas_required=True,
)
```

Set “delete_version_after” value to 30 minutes for all new versions written to the “vaultx” path / key:

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.update_metadata(
    path='vaultx',
    delete_version_after="30m",
)
```

Describe the secret with custom metadata values in `custom_metadata`:

```python3
import vaultx
client = vaultx.Client()

clients.secrets.kv.v2.update_metadata(
    path='vaultx',
    custom_metadata={
        "type": "api-token",
        "color": "blue",
    },
)
```

## Delete Metadata and All Versions

`vaultx.api.secrets_engines.KvV2.delete_metadata_and_all_versions()`

Delete all versions and metadata for a given path:

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v2.delete_metadata_and_all_versions(
    path='vaultx',
)
```
