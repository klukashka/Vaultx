# Why Vaultx?

>**Note**: Vaultx is inspired by [hvac](https://github.com/hvac/hvac). Architecture and interface are taken from there.

### There are several reasons for that

- Based on [httpx](https://github.com/encode/httpx). Vaultx uses [httpx](https://github.com/encode/httpx) instead of [requests](https://github.com/psf/requests). This means you will receive responses faster.
- Has async client implementation. It has the same interface and supports the methods which synchronous one does.
- Has the same interface as [httpx](https://github.com/encode/httpx), so it will be easier to integrate it into your code.

### Let's check out benchmarks
(here should be benchmarks comparing vaultx with hvac)