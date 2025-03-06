# Getting Started

## Initialize the Client using TLS

```python3
client = vaultx.Client(url='https://localhost:8200', token=os.environ['VAULT_TOKEN'],)
client.is_authenticated()
```

## Read and Write to Secrets Engines

### KV Secrets Engines - V2

Let's write down a secret, read it and then delete:

```python3
create_response = client.secrets.kv.v2.create_or_update_secret(
    path='foo',
    secret=dict(baz='bar'),
)

read_response = client.secrets.kv.read_secret_version(path='foo')
print(read_response["data"]["data"])

# -> {'baz': 'bar'}

client.secrets.kv.delete_metadata_and_all_versions('foo')
```

### KV Secrets Engines - V1

Preferred usage:

```python3
create_response = client.secrets.kv.v1.create_or_update_secret('foo', secret=dict(baz='bar'))

read_response = client.secrets.kv.v1.read_secret('foo')
print(read_response["data"]["data"])

# -> {'baz': 'bar'}

delete_response = client.secrets.kv.v1.delete_secret('foo')
```

## Async Support

>**Note**: Asynchronous client supports the same methods as the synchronous one does. Use it via _context manager_ or just remember to close it.

```python3
async def some_function():
    async with vaultx.AsyncClient(url='https://localhost:8200') as client:
        await client.is_authenticated()
```

```python3
async def some_function():
    client = vaultx.AsyncClient(url='https://localhost:8200')
    await client.is_authenticated()
    await client.close()
```

Check out how fast it is!

```python3
import vaultx
import time
import asyncio


URL = "http://127.0.0.1:8200"
TOKEN = "root"
PATH = "testing_with_aiohttp"
some_resource = {"some_text": "another_text", "you": 42, 1: 3, 5: None}
n = 100


async def do_for_async_vaultx():
    tasks = []
    async with vaultx.AsyncClient(url=URL, token=TOKEN) as async_vaultx_client:
        start = time.time()
        for _ in range(n):
            tasks.append(async_vaultx_client.is_authenticated())
            tasks.append(async_vaultx_client.secrets.kv.v2.create_or_update_secret(path=PATH, secret=some_resource))
            tasks.append(async_vaultx_client.secrets.kv.v2.read_secret_version(path=PATH))
        await asyncio.gather(*tasks)
    print(f"async vaultx took {time.time() - start} for {n} requests")


asyncio.run(do_for_async_vaultx())
```