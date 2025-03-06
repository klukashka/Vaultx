# Seal

## Seal Status

`vaultx.api.system_backend.Seal.seal_status()`

```python3
import hvac
client = hvac.Client(url='https://127.0.0.1:8200')

print(f'Is Vault sealed: {client.seal_status['sealed']}')
```

## Is Sealed

`vaultx.api.system_backend.Seal.is_sealed()`

```python3
import hvac
client = hvac.Client(url='https://127.0.0.1:8200')

print('Is Vault sealed: %s' % client.sys.is_sealed())
```

## Read Seal Status

`vaultx.api.system_backend.Seal.read_seal_status()`

```python3
import hvac
client = hvac.Client(url='https://127.0.0.1:8200')

print(f'Is Vault sealed: {client.sys.read_seal_status()['sealed']}')
```

## Seal

`vaultx.api.system_backend.Seal.seal()`

```python3
import hvac
client = hvac.Client(url='https://127.0.0.1:8200')

client.sys.seal()
```

## Submit Unseal Key

`vaultx.api.system_backend.Seal.submit_unseal_key()`

```python3
import hvac
client = hvac.Client(url='https://127.0.0.1:8200')

client.sys.submit_unseal_key(key=key)
```

## Submit Unseal Keys

`vaultx.api.system_backend.Seal.submit_unseal_keys()`

```python3
import hvac
client = hvac.Client(url='https://127.0.0.1:8200')

client.sys.submit_unseal_keys(keys=keys)
```