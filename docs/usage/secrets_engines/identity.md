# Identity

## Entity

## Create or Update Entity

`vaultx.api.secrets_engines.Identity.create_or_update_entity()`

```python3
import vaultx
client = vaultx.Client()

create_response = client.secrets.identity.create_or_update_entity(
    name='vaultx-entity',
    metadata=dict(extra_data='yup'),
)
entity_id = create_response['data']['id']
print('Entity ID for "vaultx-entity" is: {id}'.format(id=entity_id))
```

## Create or Update Entity by Name

`vaultx.api.secrets_engines.Identity.create_or_update_entity_by_name()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.create_or_update_entity_by_name(
    name='vaultx-entity',
    metadata=dict(new_data='uhuh'),
)
```

## Read Entity

`vaultx.api.secrets_engines.Identity.read_entity()`

```python3
import vaultx
client = vaultx.Client()

read_response = client.secrets.identity.read_entity(
    entity_id=entity_id,
)
name = read_response['data']['name']
print('Name for entity ID {id} is: {name}'.format(id=entity_id, name=name))
```

## Read Entity by Name

`vaultx.api.secrets_engines.Identity.read_entity_by_name()`

```python3
import vaultx
client = vaultx.Client()

read_response = client.secrets.identity.read_entity_by_name(
    name='vaultx-entity',
)
entity_id = read_response['data']['id']
print('Entity ID for "vaultx-entity" is: {id}'.format(id=entity_id))
```

## Update Entity

`vaultx.api.secrets_engines.Identity.update_entity()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.update_entity(
    entity_id=entity_id,
    metadata=dict(new_metadata='yup'),
)
```

## Delete Entity

`vaultx.api.secrets_engines.Identity.delete_entity()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.delete_entity(
    entity_id=entity_id,
)
```

## Delete Entity by Name

`vaultx.api.secrets_engines.Identity.delete_entity_by_name()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.delete_entity_by_name(
    name='vaultx-entity',
)
```

## List Entities

`vaultx.api.secrets_engines.Identity.list_entities()`

```python3
import vaultx
client = vaultx.Client()

list_response = client.secrets.identity.list_entities()
entity_keys = list_response['data']['keys']
print('The following entity IDs are currently configured: {keys}'.format(keys=entity_keys))
```

## List Entities by Name

`vaultx.api.secrets_engines.Identity.list_entities_by_name()`

```python3
import vaultx
client = vaultx.Client()

list_response = client.secrets.identity.list_entities_by_name()
entity_keys = list_response['data']['keys']
print('The following entity names are currently configured: {keys}'.format(keys=entity_keys))
```

## Merge Entities

`vaultx.api.secrets_engines.Identity.merge_entities()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.merge_entities(
    from_entity_ids=from_entity_ids,
    to_entity_id=to_entity_id,
)
```

---

## Entity Alias

## Create or Update Entity Alias

`vaultx.api.secrets_engines.Identity.create_or_update_entity_alias()`

```python3
import vaultx
client = vaultx.Client()

create_response = client.secrets.identity.create_or_update_entity_alias(
    name='vaultx-entity-alias',
    canonical_id=entity_id,
    mount_accessor='auth_approle_73c16de3',
)
alias_id = create_response['data']['id']
print('Alias ID for "vaultx-entity-alias" is: {id}'.format(id=alias_id))
```

## Read Entity Alias

`vaultx.api.secrets_engines.Identity.read_entity_alias()`

```python3
import vaultx
client = vaultx.Client()

read_response = client.secrets.identity.read_entity_alias(
    alias_id=alias_id,
)
name = read_response['data']['name']
print('Name for entity alias {id} is: {name}'.format(id=alias_id, name=name))
```

## Update Entity Alias

`vaultx.api.secrets_engines.Identity.update_entity_alias()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.update_entity_alias(
    alias_id=alias_id,
    name='new-alias-name',
    canonical_id=entity_id,
    mount_accessor='auth_approle_73c16de3',
)
```

## List Entity Aliases

`vaultx.api.secrets_engines.Identity.list_entity_aliases()`

```python3
import vaultx
client = vaultx.Client()

list_response = client.secrets.identity.list_entity_aliases()
alias_keys = list_response['data']['keys']
print('The following entity alias IDs are currently configured: {keys}'.format(keys=alias_keys))
```

## Delete Entity Alias

`vaultx.api.secrets_engines.Identity.delete_entity_alias()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.delete_entity_alias(
    alias_id=alias_id,
)
```

---

## Group

## Create or Update Group

`vaultx.api.secrets_engines.Identity.create_or_update_group()`

```python3
import vaultx
client = vaultx.Client()

create_response = client.secrets.identity.create_or_update_group(
    name='vaultx-group',
    metadata=dict(extra_data='we gots em'),
)
group_id = create_response['data']['id']
print('Group ID for "vaultx-group" is: {id}'.format(id=group_id))
```

## Read Group

`vaultx.api.secrets_engines.Identity.read_group()`

```python3
import vaultx
client = vaultx.Client()

read_response = client.secrets.identity.read_group(
    group_id=group_id,
)
name = read_response['data']['name']
print('Name for group ID {id} is: {name}'.format(id=group_id, name=name))
```

## Update Group

`vaultx.api.secrets_engines.Identity.update_group()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.update_group(
    group_id=group_id,
    metadata=dict(new_metadata='yup'),
)
```

## Delete Group

`vaultx.api.secrets_engines.Identity.delete_group()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.delete_group(
    group_id=group_id,
)
```

## List Groups

`vaultx.api.secrets_engines.Identity.list_groups()`

```python3
import vaultx
client = vaultx.Client()

list_response = client.secrets.identity.list_groups()
group_keys = list_response['data']['keys']
print('The following group IDs are currently configured: {keys}'.format(keys=group_keys))
```

## List Groups by Name

`vaultx.api.secrets_engines.Identity.list_groups_by_name()`

```python3
import vaultx
client = vaultx.Client()

list_response = client.secrets.identity.list_groups_by_name()
group_keys = list_response['data']['keys']
print('The following group names are currently configured: {keys}'.format(keys=group_keys))
```

## Create or Update Group by Name

`vaultx.api.secrets_engines.Identity.create_or_update_group_by_name()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.create_or_update_group_by_name(
    name='vaultx-group',
    metadata=dict(new_data='uhuh'),
)
```

## Read Group by Name

`vaultx.api.secrets_engines.Identity.read_group_by_name()`

```python3
import vaultx
client = vaultx.Client()

read_response = client.secrets.identity.read_group_by_name(
    name='vaultx-group',
)
group_id = read_response['data']['id']
print('Group ID for "vaultx-group" is: {id}'.format(id=group_id))
```

## Delete Group by Name

`vaultx.api.secrets_engines.Identity.delete_group_by_name()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.delete_group_by_name(
    name='vaultx-group',
)
```

---

## Group Alias

## Create or Update Group Alias

`vaultx.api.secrets_engines.Identity.create_or_update_group_alias()`

```python3
import vaultx
client = vaultx.Client()

create_response = client.secrets.identity.create_or_update_group_alias(
    name='vaultx-group-alias',
    canonical_id=group_id,
    mount_accessor='auth_approle_73c16de3',
)
alias_id = create_response['data']['id']
print('Group alias ID for "vaultx-group-alias" is: {id}'.format(id=alias_id))
```

## Update Group Alias

`vaultx.api.secrets_engines.Identity.update_group_alias()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.update_group_alias(
    alias_id=alias_id,
    name='new-alias-name',
    canonical_id=group_id,
    mount_accessor='auth_approle_73c16de3',
)
```

## Read Group Alias

`vaultx.api.secrets_engines.Identity.read_group_alias()`

```python3
import vaultx
client = vaultx.Client()

read_response = client.secrets.identity.read_group_alias(
    alias_id=alias_id,
)
name = read_response['data']['name']
print('Name for group alias {id} is: {name}'.format(id=alias_id, name=name))
```

## Delete Group Alias

`vaultx.api.secrets_engines.Identity.delete_group_alias()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.delete_group_alias(
    alias_id=alias_id,
)
```

## List Group Aliases

`vaultx.api.secrets_engines.Identity.list_group_aliases()`

```python3
import vaultx
client = vaultx.Client()

list_response = client.secrets.identity.list_group_aliases()
alias_keys = list_response['data']['keys']
print('The following group alias IDs are currently configured: {keys}'.format(keys=alias_keys))
```

---

## Lookup

## Lookup Entity

`vaultx.api.secrets_engines.Identity.lookup_entity()`

```python3
import vaultx
client = vaultx.Client()

lookup_response = client.secrets.identity.lookup_entity(
    name='vaultx-entity',
)
entity_id = lookup_response['data']['id']
print('Entity ID for "vaultx-entity" is: {id}'.format(id=entity_id))
```

## Lookup Group

`vaultx.api.secrets_engines.Identity.lookup_group()`

```python3
import vaultx
client = vaultx.Client()

lookup_response = client.secrets.identity.lookup_group(
    name='vaultx-group',
)
group_id = lookup_response['data']['id']
print('Group ID for "vaultx-group" is: {id}'.format(id=group_id))
```

---

## Tokens

## Configure Tokens Backend

`vaultx.api.secrets_engines.Identity.configure_tokens_backend()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.configure_tokens_backend(
    issuer='https://python-vaultx.org:1234',
)
```

## Read Tokens Backend Configuration

`vaultx.api.secrets_engines.Identity.read_tokens_backend_configuration()`

```python3
import vaultx
client = vaultx.Client()

config = client.secrets.identity.read_tokens_backend_configuration()
print('Tokens backend issuer: {issuer}'.format(issuer=config['data']['issuer']))
```

## Create Named Key

`vaultx.api.secrets_engines.Identity.create_named_key()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.create_named_key(
    name='vaultx',
)
```

## Read Named Key

`vaultx.api.secrets_engines.Identity.read_named_key()`

```python3
import vaultx
client = vaultx.Client()

key_response = client.secrets.identity.read_named_key(
    name='vaultx',
)
print('Identity key "vaultx" algorithm is: {algorithm}'.format(
    algorithm=key_response['data']['algorithm'],
))
```

## Delete Named Key

`vaultx.api.secrets_engines.Identity.delete_named_key()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.delete_named_key(
    name='vaultx',
)
```

## List Named Keys

`vaultx.api.secrets_engines.Identity.list_named_keys()`

```python3
import vaultx
client = vaultx.Client()

list_keys_resp = client.secrets.identity.list_named_keys()
print('Current token key names: {names}'.format(
    names=', '.join(list_keys_resp['data']['keys']),
))
```

## Rotate Named Key

`vaultx.api.secrets_engines.Identity.rotate_named_key()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.rotate_named_key(
    name='vaultx',
    verification_ttl='24h',
)
```

## Create or Update Role

`vaultx.api.secrets_engines.Identity.create_or_update_role()`

```python3
import vaultx
client = vaultx.Client()

key_name = 'vaultx-key'
token_client_id = 'some-client-id'
client.secrets.identity.create_named_key(
    name=key_name,
    allowed_client_ids=[token_client_id],
)
client.secrets.identity.create_or_update_role(
    name='vaultx-person',
    key_name=key_name,
    client_id=token_client_id,
)
```

## Read Role

`vaultx.api.secrets_engines.Identity.read_role()`

```python3
import vaultx
client = vaultx.Client()

read_resp = client.secrets.identity.read_role(
    name='vaultx-person',
)
print('Identity role "vaultx-person" is set to use key: {key_name}'.format(
    key_name=read_resp['data']['key'],
))
```

## Delete Role

`vaultx.api.secrets_engines.Identity.delete_role()`

```python3
import vaultx
client = vaultx.Client()

client.secrets.identity.delete_role(
    name='vaultx-person',
)
```

## List Roles

`vaultx.api.secrets_engines.Identity.list_roles()`

```python3
import vaultx
client = vaultx.Client()

response = client.secrets.identity.list_roles()
print('Current token role names: {names}'.format(
    names=', '.join(response['data']['keys']),
))
```

## Generate Signed ID Token

`vaultx.api.secrets_engines.Identity.generate_signed_id_token()`

```python3
import vaultx
client = vaultx.Client()

response = client.secrets.identity.generate_signed_id_token(
    name='vaultx-person',
)
print('Generated signed id token: {token}'.format(
    token=response['data']['token'],
))
```

## Introspect Signed ID Token

`vaultx.api.secrets_engines.Identity.introspect_signed_id_token()`

```python3
import vaultx
client = vaultx.Client()

response = client.secrets.identity.introspect_signed_id_token(
    token='some-generated-signed-id-token',
)
print('Specified token is active?: {active}'.format(
    active=response['active'],
))
```

## Read .well-known Configurations

`vaultx.api.secrets_engines.Identity.read_well_known_configurations()`

```python3
import vaultx
client = vaultx.Client()

response = client.secrets.identity.read_well_known_configurations()
print('JWKS URI is: {jwks_uri}'.format(
    jwks_uri=response['jwks_uri'],
))
```

## Read Active Public Keys

`vaultx.api.secrets_engines.Identity.read_active_public_keys()`

```python3
import vaultx
client = vaultx.Client()

response = client.secrets.identity.read_active_public_keys()
print('Active public keys: {keys}'.format(
    keys=response['keys'],
))
```
