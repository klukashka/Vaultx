# Mount

## List Mounted Secrets Engines

`vautlx.api.system_backend.Mount.list_mounted_secrets_engines()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

secrets_engines_list = client.sys.list_mounted_secrets_engines()['data']
print('The following secrets engines are mounted: %s' % ', '.join(sorted(secrets_engines_list.keys())))
```

## Enable Secrets Engines

`vautlx.api.system_backend.Mount.enable_secrets_engine()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.enable_secrets_engine(
    backend_type='kv',
    path='vaultx-kv',
)
```

## Disable Secrets Engines

`vautlx.api.system_backend.Mount.disable_secrets_engine()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.disable_secrets_engine(
    path='vaultx-kv',
)
```

## Read Mount Configuration

`vautlx.api.system_backend.Mount.read_mount_configuration()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

secret_backend_tuning = client.sys.read_mount_configuration(path='vaultx-kv')
print('The max lease TTL for the "vaultx-kv" backend is: {max_lease_ttl}'.format(
    max_lease_ttl=secret_backend_tuning['data']['max_lease_ttl'],
 ))
```

## Tune Mount Configuration

`vautlx.api.system_backend.Mount.tune_mount_configuration()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.tune_mount_configuration(
    path='vaultx-kv',
    default_lease_ttl='3600s',
    max_lease_ttl='8600s',
)
```

## Move Backend

`vautlx.api.system_backend.Mount.move_backend()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.move_backend(
    from_path='vaultx-kv',
    to_path='kv-vaultx',
)
```