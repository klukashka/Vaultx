# Audit

## List Enabled Audit Devices

`vaultx.api.system_backend.Audit.list_enabled_audit_devices()`

```python3
audit_devices = client.sys.list_enabled_audit_devices()

options = {
    'path': '/tmp/vault.log',
    'log_raw': True,
}

client.sys.enable_audit_device('file', options=options, path='somefile')
client.sys.disable_audit_device('oldfile')
```

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

enabled_audit_devices = client.sys.list_enabled_audit_devices()
audit_devices_list = ', '.join(enabled_audit_devices['data'].keys())
print(f'The following audit devices are enabled: {audit_devices_list}')
```

## Disable Audit Device

`vaultx.api.system_backend.Audit.disable_audit_device()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.disable_audit_device(
    path='tmp-file-audit',
)
```

## Calculate hash

`vaultx.api.system_backend.Audit.calculate_hash()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

input_to_hash = 'some sort of string thinger'

audit_hash = client.sys.calculate_hash(
    path='tmp-file-audit',
    input_to_hash=input_to_hash,
)

print(f'The hash for the provided input is: {audit_hash['data']['hash']}')
```

