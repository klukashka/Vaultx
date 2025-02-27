# Why Vaultx?

### It is important to say, that Vaultx is inspired by [hvac](https://github.com/hvac/hvac). Architecture and interface are taken from there.

### Then, why use Vaultx instead of hvac?

### There are several reasons for that:

- Based on **httpx**. Vaultx uses [httpx](https://github.com/encode/httpx) instead of [requests](https://github.com/psf/requests). This means you will receive responses faster.
- Has **asynchronous client** implementation (currently in develop). It has the same interface and supports all the methods which synchronous one does.
- Has **the same interface** as hvac, so it will be easier to integrate it into your code.