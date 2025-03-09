# Why Vaultx?

>**Note**: Vaultx is inspired by [hvac](https://github.com/hvac/hvac). Architecture and interface are taken from there.

### There are several reasons for that

- Based on [httpx](https://github.com/encode/httpx). Vaultx uses [httpx](https://github.com/encode/httpx) instead of [requests](https://github.com/psf/requests). This means you will receive responses faster.
- Has async client implementation. It has the same interface and supports the same methods which synchronous one does.
- Has the same interface as [httpx](https://github.com/encode/httpx), so it will be easier to integrate it into your code.

### Let's check out benchmarks
We'll compare _HVAC_, _Vaultx_ and _Async Vaultx_ in _average performance_. The tasks are simple: to write and to read.
There will be 11 _epochs_ (number of operations): _[1, 5, 10, 20, 50, 100, 200, 350, 500, 750, 1000]_. 
Each epoch will be repeated _5_ times (_repeats_) to measure the average performance. Here is the code:

<details>

<summary>Code</summary>

```python3
import asyncio
import time

import hvac

import vaultx


resource = {
    "config": {
        "name": "John Doe",
        "age": 42,
        "Address": {"ADDRESS": "123 Main St", "city": None},
        "preferences": {"FaVoriteS": ["a", "b", "c"]},
        "is_active": True,
    }
}


URL = "http://127.0.0.1:8200"
TOKEN = "root"
PATH = "testing_with_aiohttp"


def do_for_hvac(n: int):
    hvac_client = hvac.Client(url=URL, token=TOKEN)
    start = time.time()
    for _ in range(n):
        hvac_client.is_authenticated()
        hvac_client.secrets.kv.v2.create_or_update_secret(path=PATH, secret=resource)
        hvac_client.secrets.kv.v2.read_secret_version(path=PATH, raise_on_deleted_version=False)
    total_time = time.time() - start
    print(f"hvac took {total_time} for {n} requests")
    return total_time


def do_for_vaultx(n: int):
    with vaultx.Client(url=URL, token=TOKEN) as vaultx_client:
        start = time.time()
        for _ in range(n):
            vaultx_client.is_authenticated()
            vaultx_client.secrets.kv.v2.create_or_update_secret(path=PATH, secret=resource)
            vaultx_client.secrets.kv.v2.read_secret_version(path=PATH)
    total_time = time.time() - start
    print(f"vaultx took {total_time} for {n} requests")
    return total_time


async def do_for_async_vaultx(n: int):
    tasks = []
    async_vaultx_client = vaultx.AsyncClient(url=URL, token=TOKEN)
    start = time.time()
    for _ in range(n):
        tasks.append(async_vaultx_client.is_authenticated())
        tasks.append(async_vaultx_client.secrets.kv.v2.create_or_update_secret(path=PATH, secret=resource))
        tasks.append(async_vaultx_client.secrets.kv.v2.read_secret_version(path=PATH))
    await asyncio.gather(*tasks)
    await async_vaultx_client.close()
    total_time = time.time() - start
    print(f"async vaultx took {total_time} for {n} requests")
    return total_time


results = [[] for _ in range(3)]

epochs = [1, 5, 10, 20, 50, 100, 200, 350, 500, 750, 1000]
repeats = 5
for iterations in epochs:
    for i, function in enumerate((do_for_hvac, do_for_vaultx, do_for_async_vaultx)):
        time.sleep(1)
        average = 0
        for _ in range(repeats):
            time.sleep(0.5)
            if function.__name__ != "do_for_async_vaultx":
                average += function(iterations)
            else:
                average += asyncio.run(function(iterations))
        results[i].append(average / repeats)

print(results)

```
</details>

You can try it yourself by running the server locally in terminal via `vault server -dev -dev-root-token-id="root" -address="http://127.0.0.1:8200"`.

The benchmarks are run on _Ubuntu 24.04.2 LTS_ with _Intel® Core™ i5-7300U × 4_ CPU and _12.0 GiB_ Memory. The results are:

<details>

<summary>Results</summary>

```python3
results = [
    [0.017037343978881837, 0.07232718467712403, 0.14330039024353028, 0.26955699920654297, 0.6601319789886475, 1.1966200351715088, 1.9504114627838134, 3.431483840942383, 4.743838691711426, 7.084809923171997, 8.356381607055663], 
    [0.013585186004638672, 0.049878406524658206, 0.10232477188110352, 0.19789347648620606, 0.48628926277160645, 0.7989840030670166, 1.6327192306518554, 3.0580058097839355, 4.089705991744995, 6.210736465454102, 6.706547641754151],
    [0.013380289077758789, 0.0471491813659668, 0.10409841537475586, 0.14378628730773926, 0.2310150146484375, 0.3415419578552246, 0.5561285495758057, 0.8834378242492675, 1.2136030197143555, 1.7599134922027588, 2.2954917907714845]
]
```

</details>

Let's make a graph and its logarithmic version for the better visibility:

![Image](https://github.com/user-attachments/assets/5b7dbc50-8c50-4aff-9031-20bbfc48845c)
![Image](https://github.com/user-attachments/assets/36fc3b47-dd48-4ff1-89fa-eac01d458515)
