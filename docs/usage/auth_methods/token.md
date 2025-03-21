# Token

## Authentication

`vaultx.api.auth_methods.Token.is_authenticated()`

```python3
client.token = 'MY_TOKEN'
assert client.is_authenticated() # => True
```

## Token Management

Token creation and revocation:

`vaultx.api.auth_methods.Token.create()`
`vaultx.api.auth_methods.Token.revoke()`

```python3
token = client.auth.token.create(policies=['root'], ttl='1h')

current_token = client.auth.token.lookup_self()
some_other_token = client.auth.token.lookup('xxx')

client.auth.token.revoke('xxx')
client.auth.token.revoke('yyy', orphan=True)

# revoke current token
client.auth.token.revoke_self()
# logout and revoke current token
client.logout(revoke_token=True)

client.auth.token.renew('aaa')

```

Lookup and revoke tokens via a token accessor:

`vaultx.api.auth_methods.Token.lookup()`

```python3
token = client.auth.token.create(policies=['root'], ttl='1h')
token_accessor = token['auth']['accessor']

same_token = client.auth.token.lookup(token_accessor, accessor=True)
client.auth.token.revoke(token_accessor, accessor=True)
```

Wrapping/unwrapping a token:

`vaultx.api.auth_methods.Token.unwrap()`

```python3
wrap = client.auth.token.create(policies=['root'], ttl='1h', wrap_ttl='1m')
result = client.sys.unwrap(wrap['wrap_info']['token'])
```

Login with a wrapped token:

```python3
wrap = client.auth.token.create(policies=['root'], ttl='1h', wrap_ttl='1m')
new_client = hvac.Client()
new_client.auth_cubbyhole(wrap['wrap_info']['token'])
assert new_client.token != wrapped_token['wrap_info']['token']
```