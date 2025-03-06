# KV Secrets Engines

The `vaultx.api.secrets_engines.Kv` instance under the `Client class's secrets.kv attribute` is a wrapper 
to expose either version 1 (`KvV1`) or version 2 of the key/value secrets engines’ API methods (`KvV2`). 
At present, this class defaults to version 2 when accessing methods on the instance.

## Setting the Default KV Version

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.default_kv_version = 1
client.secrets.kv.read_secret(path='vaultx')  # => calls vaultx.api.secrets_engines.KvV1.read_secret
```

## Explicitly Calling a KV Version Method

```python3
import vaultx
client = vaultx.Client()

client.secrets.kv.v1.read_secret(path='vaultx')
client.secrets.kv.v2.read_secret_version(path='vaultx')
```

## Specific KV Version Usage

* [KV - Version 1](./kv_v1.md)
* [KV - Version 2](./kv_v2.md)