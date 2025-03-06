# KV - Version 1

>**Note**:
> Every method under the `Kv class's v1 attribute` includes a _mount_point_ parameter 
> that can be used to address the KvV1 secret engine under a custom mount path. 
> E.g., If enabling the KvV1 secret engine using Vault’s CLI commands 
> via _vault secrets enable "-path=my-kvv1 -version=1 kv"_, 
> the _mount_point_ parameter in `vaultx.api.secrets_engines.KvV1()` methods would be set to "my-kvv1".

## Read a Secret

`vaultx.api.secrets_engines.KvV1.read_secret()`

```python3
import vaultx
client = vaultx.Client()

# The following path corresponds, when combined with the mount point, to a full Vault API route of "v1/secretz/vaultx"
mount_point = 'secretz'
secret_path = 'vaultx'

read_secret_result = client.secrets.kv.v1.read_secret(
    path=secret_path,
    mount_point=mount_point,
)

psst = psst=read_secret_result['data']['psst']
print(f'The "psst" key under the secret path ("/v1/secret/vaultx") is: {psst}')
```

## List Secrets

`vaultx.api.secrets_engines.KVV1.list_secrets()`

```python3
import vaultx
client = vaultx.Client()
vaultx_secret = {
    'psst': 'this is so secret yall',
}

client.secrets.kv.v1.create_or_update_secret(
    path='vaultx',
    secret=vaultx_secret,
)

read_secret_result = client.secrets.kv.v1.read_secret(
    path='vaultx',
)

psst = read_secret_result['data']['psst']
print(f'The "psst" key under the secret path ("/v1/secret/vaultx") is: {psst}')
```

## Create or Update a Secret

`vaultx.api.secrets_engines.KvV1.create_or_update_secret()`

```python3
import vaultx
client = vaultx.Client()
vaultx_secret = {
    'psst': 'this is so secret yall',
}

client.secrets.kv.v1.create_or_update_secret(
    path='vaultx',
    secret=vaultx_secret,
)

read_secret_result = client.secrets.kv.v1.read_secret(
    path='vaultx',
)

psst = read_secret_result['data']['psst']
print(f'The "psst" key under the secret path ("/v1/secret/vaultx") is: {psst}')
```

## Delete a Secret

`vaultx.api.secrets_engines.KvV1.delete_secret()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v1.delete_secret(
    path='vaultx',
)

# The following will raise a VaultxError with 404 status code
read_secret_result = client.secrets.kv.v1.read_secret(
    path='vaultx',
)
```