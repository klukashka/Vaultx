# Key

## Read Root Generation Progress

`vaultx.api.system_backend.Key.read_root_generation_progress()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

root_gen_progress = client.sys.read_root_generation_progress()
print(f'Root generation "started" status: {root_gen_progress['started']}')
```

## Start Root Token Generation

`vaultx.api.system_backend.Key.start_root_token_generation()`

```python3
import vaultx
from tests.utils import get_generate_root_otp

client = vaultx.Client(url='https://127.0.0.1:8200')

new_otp = get_generate_root_otp()
start_generate_root_response = client.sys.start_root_token_generation(
    otp=new_otp,
)
nonce = start_generate_root_response['nonce']
print(f'Nonce for root generation is: {nonce}')
```

## Cancel Root Generation

`vaultx.api.system_backend.Key.cancel_root_generation()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.cancel_root_generation()
```

## Generate Root

`vaultx.api.system_backend.Key.generate_root()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.generate_root(
    key=key,
    nonce=nonce,
)
```

## Get Encryption Key Status

`vaultx.api.system_backend.Key.key_status()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

print(f'Encryption key term is: {client.key_status['term']}')
```

## Rotate Encryption Key

`vaultx.api.system_backend.Key.rotate_encryption_key()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.rotate_encryption_key()
```

## Read Rekey Progress

`vaultx.api.system_backend.Key.read_rekey_progress()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

print(f'Rekey "started" status is: {client.sys.read_rekey_progress()['started']}')
```

## Start Rekey

`vaultx.api.system_backend.Key.start_rekey()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

rekey_response = client.sys.start_rekey()
nonce = rekey_response['nonce']
print(f'Nonce for rekey is: {nonce}')
```

## Cancel Rekey

`vaultx.api.system_backend.Key.cancel_rekey()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.cancel_rekey()
```

## Rekey

`vaultx.api.system_backend.Key.rekey()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.rekey(
    key=key,
    nonce=nonce,
)
```

## Rekey Multi

`vaultx.api.system_backend.Key.rekey_multi()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.rekey_multi(
    keys,
    nonce=nonce,
)
```

## Read Rekey Verify Progress

`vaultx.api.system_backend.Key.read_rekey_verify_progress()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

response = client.sys.read_rekey_verify_progress()

print(
    'Rekey verify progress is %d out of %d' % (
        response['progress'],
        response['t'],
    )
)
```

## Cancel Rekey Verify

`vaultx.api.system_backend.Key.cancel_rekey_verify()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.cancel_rekey_verify()
```

## Rekey Verify

`vaultx.api.system_backend.Key.rekey_verify()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.rekey_verify(
    key,
    nonce=verify_nonce,
)
```

## Rekey Verify Multi

`vaultx.api.system_backend.Key.rekey_verify_multi()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.sys.rekey_verify_multi(
    keys,
    nonce=verify_nonce,
)
```

## Read Backup Keys

`vaultx.api.system_backend.Key.read_backup_keys()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')
rekey_response = client.sys.start_rekey(
    secret_shares=1,
    secret_threshold=1,
    pgp_keys=pgp_keys,
    backup=True,
)
nonce = rekey_response['nonce']

client.sys.rekey_multi(
    keys,
    nonce=nonce,
)

print(f'Backup keys are: {client.sys.read_backup_keys()['data']['keys']}')
```