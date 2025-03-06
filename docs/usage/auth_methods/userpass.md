# Userpass

## Authentication

`vaultx.api.auth_methods.Userpass.login()`

```python3
import hvac
client = hvac.Client()

client.auth.userpass.login(
    username='<some_username>',
    password='<username_password>',
)
```