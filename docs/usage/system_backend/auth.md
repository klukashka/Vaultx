# Auth

## List Auth Methods

`vaultx.api.system_backend.Auth.list_auth_methods()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

auth_methods = client.sys.list_auth_methods()
auth_methods_list = ', '.join(auth_methods['data'].keys())
print(f'The following auth methods are enabled: {auth_methods_list}')
```

## Enable Auth Method

`vaultx.api.system_backend.Auth.list_auth_methods()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.enable_auth_method(
    method_type='github',
    path='github-vaultx',
)
```

## Disable Auth Method

`vaultx.api.system_backend.Auth.disable_auth_method()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.disable_auth_method(
    path='github-vaultx',
)
```

## Read Auth Method Tuning

`vaultx.api.system_backend.Auth.read_auth_method_tuning()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')
response = client.sys.read_auth_method_tuning(
    path='github-vaultx',
)

max_ttl = response['data']['max_lease_ttl']
print(f'The max lease TTL for the auth method under path "github-vaultx" is: {max_ttl}')
```

## Tune Auth Method

`vaultx.api.system_backend.Auth.tune_auth_method()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.tune_auth_method(
    path='github-vaultx',
    description='The Github auth method for vaultx users',
)
```