# Lease

## Read Lease

`vaultx.api.system_backend.Lease.read_lease()`

```python3
read_lease_response = client.sys.read_lease(lease_id=lease_id)

print(f'Expire time for lease ID {lease_id} is: {read_lease_response['data']['expire_time']}')
```

## List Leases

`vaultx.api.system_backend.Lease.list_leases()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

list_leases_response = client.sys.list_leases(
    prefix='pki',
)
print(f'The follow lease keys are active under the "pki" prefix: {list_leases_response['data']['keys']}')
```

## Renew Lease

`vaultx.api.system_backend.Lease.renew_lease()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.renew_lease(
    lease_id=lease_id,
    increment=500,
)
```

## Revoke Lease

`vaultx.api.system_backend.Lease.revoke_lease()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.revoke_lease(
    lease_id=lease_id,
)
```

## Revoke Prefix

`vaultx.api.system_backend.Lease.revoke_prefix()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.revoke_prefix(
    prefix='pki',
)
```

## Revoke Force

`vaultx.api.system_backend.Lease.revoke_force()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.revoke_force(
    prefix='pki',
)
```