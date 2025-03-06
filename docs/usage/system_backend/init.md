# Init

## Read Status

`vaultx.api.system_backend.Init.read_init_status()`

```python3
import vaultx

client = vaultx.Client(url='https://127.0.0.1:8200')

read_response = client.sys.read_init_status()
print(f'Vault initialize status: {read_response['initialized']}')
```

## Is Initialized

```python3
import vaultx

client = vaultx.Client(url='https://127.0.0.1:8200')

print(f'Vault initialize status: {client.sys.is_initialized()}')
```

## Initialize

```python3
import vaultx

client = vaultx.Client(url='https://127.0.0.1:8200')

init_result = client.sys.initialize()

root_token = init_result['root_token']
unseal_keys = init_result['keys']
```

When called for a previously initialized Vault cluster, an exception with 400 status code is raised:

```python3
import vaultx

client = vaultx.Client(url='https://127.0.0.1:8200')

init_result = client.sys.initialize()
```