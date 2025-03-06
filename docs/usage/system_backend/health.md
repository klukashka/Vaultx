# Health

## Read Status

`vaultx.api.system_backend.Health.read_health_status()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

status = client.sys.read_health_status(method='GET')
print(f'Vault initialization status is: {status['initialized']}')
```