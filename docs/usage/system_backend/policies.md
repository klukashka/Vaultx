# Policies

## Create or Update ACL Policy

`vaultx.api.system_backend.Policies.create_or_update_acl_policy()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")

# Create ACL Policy
client.sys.create_or_update_acl_policy(
        name="test-acl-policy", policy='path "sys/health" { capabilities = ["read", "sudo"]}',
    )

# Update ACL Policy
client.sys.create_or_update_acl_policy(
        name="test-acl-policy", policy='path "sys/health" { capabilities = ["read"]}',
    )
```

## Read ACL Policy

`vaultx.api.system_backend.Policies.read_acl_policy()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")

# Create ACL Policy
client.sys.create_or_update_acl_policy(
        name="test-acl-policy", policy='path "sys/health" { capabilities = ["read", "sudo"]}',
    )

client.sys.read_acl_policy("test-acl-policy")
```

## List ACL Policies

`vaultx.api.system_backend.Policies.list_acl_policies()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")

client.sys.create_or_update_acl_policy(
        name="test-acl-policy", policy='path "sys/health" { capabilities = ["read"]}',
    )
client.sys.list_acl_policies()
```

## Delete ACL Policy

`vaultx.api.system_backend.Policies.delete_acl_policy()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")
client.sys.delete_acl_policy("test-acl-policy")
```

## Create or Update RGP Policy

`vaultx.api.system_backend.Policies.create_or_update_rgp_policy()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")

policy = """import "time"
import "strings"

main = rule when not strings.has_prefix(request.path, "auth/ldap/login") {
    time.load(token.creation_time).unix > time.load("2017-09-17T13:25:29Z").unix
}
"""

# Create RGP Policy
client.sys.create_or_update_rgp_policy(
        name="test-rgp-policy", policy=policy, enforcement_level="soft-mandatory"
    )

# Update RGP Policy
client.sys.create_or_update_rgp_policy(
        name="test-rgp-policy", policy=policy, enforcement_level="hard-mandatory",
    )
```

## Read RGP Policy

`vaultx.api.system_backend.Policies.read_rgp_policy()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")

policy = """import "time"
import "strings"

main = rule when not strings.has_prefix(request.path, "auth/ldap/login") {
    time.load(token.creation_time).unix > time.load("2017-09-17T13:25:29Z").unix
}
"""

client.sys.create_or_update_rgp_policy(
    name="test-rgp-policy", policy=policy, enforcement_level="soft-mandatory"
)

client.sys.read_rgp_policy("test-rgp-policy")
```

## List RGP Policies

`vaultx.api.system_backend.Policies.list_rgp_policies()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")

policy = """import "time"
import "strings"

main = rule when not strings.has_prefix(request.path, "auth/ldap/login") {
    time.load(token.creation_time).unix > time.load("2017-09-17T13:25:29Z").unix
}
"""

client.sys.create_or_update_rgp_policy(
        name="test-rgp-policy", policy=policy, enforcement_level="soft-mandatory"
    )
client.sys.list_rgp_policies()
```

## Delete RGP Policy

`vaultx.api.system_backend.Policies.delte_rgp_policy()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")
client.sys.delete_rgp_policy("test-rgp-policy")
```

## Create or Update EGP Policy

`vaultx.api.system_backend.Policies.create_or_update_egp_policy()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")

policy = """import "time"
import "strings"

main = rule when not strings.has_prefix(request.path, "auth/ldap/login") {
    time.load(token.creation_time).unix > time.load("2017-09-17T13:25:29Z").unix
}
"""

# Create EGP Policy
client.sys.create_or_update_egp_policy(
        name="test-egp-policy", policy=policy, enforcement_level="soft-mandatory", paths=["/test"]
    )

# Update EGP Policy
client.sys.create_or_update_egp_policy(
        name="test-egp-policy", policy=policy, enforcement_level="hard-mandatory", paths=["/test"],
    )
```

## Read EGP Policy

`vaultx.api.system_backend.Policies.read_egp_policy()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")

policy = """import "time"
import "strings"

main = rule when not strings.has_prefix(request.path, "auth/ldap/login") {
    time.load(token.creation_time).unix > time.load("2017-09-17T13:25:29Z").unix
}
"""

# Create EGP Policy
client.sys.create_or_update_egp_policy(
        name="test-egp-policy", policy=policy, enforcement_level="soft-mandatory", paths=["/test"]
    )

client.sys.read_egp_policy("test-egp-policy")
```

## List EGP Policies

`vaultx.api.system_backend.Policies.list_egp_policies()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")

policy = """import "time"
import "strings"

main = rule when not strings.has_prefix(request.path, "auth/ldap/login") {
    time.load(token.creation_time).unix > time.load("2017-09-17T13:25:29Z").unix
}
"""

client.sys.create_or_update_egp_policy(
        name="test-egp-policy1", policy=policy, enforcement_level="soft-mandatory", paths=["/test"]
    )
client.sys.list_egp_policies()
```

## Delete EGP Policy

`vaultx.api.system_backend.Policies.delete_egp_policy()`

```python3
import vaultx
client = vaultx.Client(url="https://127.0.0.1:8200")
client.sys.delete_egp_policy("test-egp-policy")
```
