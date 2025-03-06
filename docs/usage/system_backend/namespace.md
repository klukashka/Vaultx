# Namespace

## Create Namespace

`vaultx.api.system_backend.Namespace.create_namespace`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

# Create namespace team1 where team1 is a child of root
client.sys.create_namespace(path="team1")

# Create namespace team1/app1 where app1 is a child of team1
client2 = vaultx.Client(url='https://127.0.0.1:8200', namespace="team1")
client2.sys.create_namespace(path="app1")
```

## List Namespaces

`vaultx.api.system_backend.Namespace.list_namespaces`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')
client.sys.create_namespace(path='test_name_space')

client.sys.list_namespaces()
```

## Delete Namespace

`vaultx.api.system_backend.Namespace.delete_namespace`

```python3
import vaultx

# Delete namespace app1 where app1 is a child of team1
client2 = vaultx.Client(url='https://127.0.0.1:8200', namespace="team1")
client2.sys.delete_namespace(path="app1")

# Delete namespace team1
client = vaultx.Client(url='https://127.0.0.1:8200')
client.sys.delete_namespace(path="team1")
```