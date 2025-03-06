# Capabilities

## Get Capabilities

`vaultx.api.system_backend.Capabilities.get_capabilities()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200', token="TOKEN")

capabilities = client.sys.get_capabilities(paths=["path1", "path2"])
print(f'Vault capabilities are: {capabilities}')
```