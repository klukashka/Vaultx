# Leader

## Read Leader Status

`vaultx.api.systm_backend.Leader.read_leader_status()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

status = client.sys.read_leader_status()
print(f'HA status is: {status['ha_enabled']}')
```


## Step Down

`vaultx.api.systm_backend.Leader.step_down()`

```python3
import vaultx

client = vaultx.Client(url='https://127.0.0.1:8200')
client.sys.step_down()
```