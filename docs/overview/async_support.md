# Async Support

## About Async

Vaultx offers a standard synchronous API by default, but also gives you the option of an async client if you need it.
Async is a concurrency model that is far more efficient than multi-threading, 
and can provide significant performance benefits (check out [benchmarks](./why_vaultx.md#lets-check-out-benchmarks)).

If you are working with async, you'll also want to use Vaultx's async client.

## Usage

Use async client via _context manager_ or just remember to close it.

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

Here is another example:

```python3
import vaultx


async def very_important_func():
    client = vaultx.AsyncClient(url='http://localhost:8200', token='root')
    await client.auth.approle.create_or_update_approle("testrole")
    create_result = await client.auth.approle.generate_secret_id(
        "testrole", {"foo": "bar"}
    )
    secret_id = create_result["data"]["secret_id"]
    result = await client.auth.approle.read_secret_id("testrole", secret_id)
    await client.auth.approle.destroy_secret_id("testrole", secret_id)

    await client.close()
```