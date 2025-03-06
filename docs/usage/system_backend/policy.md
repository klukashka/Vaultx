# Policy

## Create or Update Policy

`vaultx.api.system_backend.Policy.create_or_update_policy()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

policy = '''
    path "sys" {
        capabilities = ["deny"]
    }
    path "secret" {
        capabilities = ["create", "read", "update", "delete", "list"]
    }
'''
client.sys.create_or_update_policy(
    name='secret-writer',
    policy=policy,
)
```

## Read Policy

`vaultx.api.system_backend.Policy.read_policy()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

vaultx_policy_rules = client.sys.read_policy(name='secret-writer')['data']['rules']
print('secret-writer policy rules:\n%s' % vaultx_policy_rules)
```

## List Policies

`vaultx.api.system_backend.Policy.list_policies()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

list_policies_resp = client.sys.list_policies()['data']['policies']
print('List of currently configured policies: %s' % ', '.join(list_policies_resp))

```

## Delete Policy

`vaultx.api.system_backend.Policy.delete_policy()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.delete_policy(
    name='secret-writer',
)
```