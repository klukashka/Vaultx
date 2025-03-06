# Quota

## Create or Update a Quota

`vaultx.api.system_backend.Quota.create_or_update_quota()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

# Create file quota
client.sys.create_or_update_quota(name="quota1", rate=100.0)

# Update quota that already exists
client.sys.create_or_update_quota(name="quota1", rate=101.0)
```

## Read Quota

`vaultx.api.system_backend.Quota.read_quota()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')
client.sys.create_or_update_quota(name="quota1", rate=100.0)
```

## List Quotas

`vaultx.api.system_backend.Quota.list_quotas()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.create_or_update_quota(name="quota1", rate=1000.0, interval="10m")
client.sys.create_or_update_quota(name="quota2", rate=1000.0, path="/kv")
```

## Delete Quota

`vaultx.api.system_backend.Quota.delete_quota()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.delete_quota(name="quota1")
```