# Wrapping

## Unwrap

`vaultx.api.system_backend.Wrapping.unwrap()`

```python3
import vaultx

client = vaultx.Client(url='https://127.0.0.1:8200')
client.write(
    path="auth/approle-test/role/testrole",
)

result = client.write(
    path='auth/approle-test/role/testrole/secret-id',
    wrap_ttl="10s",
)

unwrap_response = client.sys.unwrap(
    token=result['wrap_info']['token'],
)
print(f'Unwrapped approle role token secret id accessor: {unwrap_response['data']['secret_id_accessor']}')
```