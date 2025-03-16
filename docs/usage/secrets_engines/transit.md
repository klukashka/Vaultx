# Transit

## Create Key

`vaultx.api.secrets_engines.Transit.create_key()`

Create a new named encryption key of the specified type.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.secrets.transit.create_key(name='vaultx-key')
```

## Read Key

`vaultx.api.secrets_engines.Transit.read_key()`

Read information about a named encryption key.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

read_key_response = client.secrets.transit.read_key(name='vaultx-key')
latest_version = read_key_response['data']['latest_version']
print('Latest version for key "vaultx-key" is: {ver}'.format(ver=latest_version))
```

## List Keys

`vaultx.api.secrets_engines.Transit.list_keys()`

List all keys (if there are any).

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

list_keys_response = client.secrets.transit.list_keys()
keys = list_keys_response['data']['keys']
print('Currently configured keys: {keys}'.format(keys=keys))
```

## Delete Key

`vaultx.api.secrets_engines.Transit.delete_key()`

Delete a named encryption key.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

key_name = 'gonna-delete-this-key'

client.secrets.transit.create_key(name=key_name)

# Update key to allow deletion
client.secrets.transit.update_key_configuration(
    name=key_name,
    deletion_allowed=True,
)

# Delete the key
client.secrets.transit.delete_key(name=key_name)
```

## Update Key Configuration

`vaultx.api.secrets_engines.Transit.update_key_configuration()`

Tune configuration values for a given key.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.secrets.transit.update_key_configuration(
    name='vaultx-key',
    exportable=True,
)
```

## Rotate Key

`vaultx.api.secrets_engines.Transit.rotate_key()`

Rotate the version of the named key.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.secrets.transit.rotate_key(name='vaultx-key')
```

---

## Export Key

`vaultx.api.secrets_engines.Transit.export_key()`

Return the named key.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

export_key_response = client.secrets.transit.export_key(
    name='vaultx-key',
    key_type='hmac-key',
)
print('Exported keys: %s' % export_key_response['data']['keys'])
```

## Encrypt Data

`vaultx.api.secrets_engines.Transit.encrypt_data()`

Encrypt the provided plaintext using the named key.

```python3
import base64
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

encrypt_data_response = client.secrets.transit.encrypt_data(
    name='vaultx-key',
    plaintext=base64.b64encode('hi its me vaultx'.encode()).decode(),
)
ciphertext = encrypt_data_response['data']['ciphertext']
print('Encrypted plaintext ciphertext is: {cipher}'.format(cipher=ciphertext))
```

## Decrypt Data

`vaultx.api.secrets_engines.Transit.decrypt_data()`

Decrypt the provided ciphertext using the named key.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

decrypt_data_response = client.secrets.transit.decrypt_data(
    name='vaultx-key',
    ciphertext=ciphertext,
)
plaintext = decrypt_data_response['data']['plaintext']
print('Decrypted plaintext is: {text}'.format(text=plaintext))
```

## Rewrap Data

`vaultx.api.secrets_engines.Transit.rewrap_data()`

Rewrap the provided ciphertext using the latest version of the named key.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

rewrap_data_response = client.secrets.transit.rewrap_data(
    name='vaultx-key',
    ciphertext=ciphertext,
)
rewrapped_ciphertext = rewrap_data_response['data']['ciphertext']
print('Rewrapped ciphertext is: {cipher}'.format(cipher=rewrapped_ciphertext))
```

## Generate Data Key

`vaultx.api.secrets_engines.Transit.generate_data_key()`

Generate a new high-entropy key and the value encrypted with the named key.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

gen_key_response = client.secrets.transit.generate_data_key(
    name='vaultx-key',
    key_type='plaintext',
)
ciphertext = gen_key_response['data']['ciphertext']
print('Generated data key ciphertext is: {cipher}'.format(cipher=ciphertext))
```

## Generate Random Bytes

`vaultx.api.secrets_engines.Transit.generate_random_bytes()`

Return high-quality random bytes of the specified length.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

gen_bytes_response = client.secrets.transit.generate_random_bytes(n_bytes=32)
random_bytes = gen_bytes_response['data']['random_bytes']
print('Here are some random bytes: {bytes}'.format(bytes=random_bytes))
```

## Hash Data

`vaultx.api.secrets_engines.Transit.hash_data()`

Return the cryptographic hash of given data using the specified algorithm.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

hash_data_response = client.secrets.transit.hash_data(
    hash_input=base64.b64encode('hi its me vaultx'.encode()).decode(),
    algorithm='sha2-256',
)
sum = hash_data_response['data']['sum']
print('Hashed data is: {sum}'.format(sum=sum))
```

## Generate HMAC

`vaultx.api.secrets_engines.Transit.generate_hmac()`

Return the digest of given data using the specified hash algorithm and the named key.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

generate_hmac_response = client.secrets.transit.generate_hmac(
    name='vaultx-key',
    hash_input=base64.b64encode('hi its me vaultx'.encode()).decode(),
    algorithm='sha2-256',
)
hmac = generate_hmac_response['data']
print("HMAC'd data is: {hmac}".format(hmac=hmac))
```

## Sign Data

`vaultx.api.secrets_engines.Transit.sign_data()`

Return the cryptographic signature of the given data using the named key and the specified hash algorithm.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

sign_data_response = client.secrets.transit.sign_data(
    name='vaultx-signing-key',
    hash_input=base64.b64encode('hi its me vaultx'.encode()).decode(),
)
signature = sign_data_response['data']['signature']
print('Signature is: {signature}'.format(signature=signature))
```

## Verify Signed Data

`vaultx.api.secrets_engines.Transit.verify_signed_data()`

Return whether the provided signature is valid for the given data.

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

verify_signed_data_response = client.secrets.transit.verify_signed_data(
    name='vaultx-signing-key',
    hash_input=base64.b64encode('hi its me vaultx'.encode()).decode(),
    signature=signature,
)
valid = verify_signed_data_response['data']['valid']
print('Signature is valid?: {valid}'.format(valid=valid))
```
