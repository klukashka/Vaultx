# Transform

## Encode/Decode Example

`vaultx.api.secrets_engines.Transform.encode()`  
`vaultx.api.secrets_engines.Transform.decode()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

input_value = '1111-1111-1111-1111'

role_name = 'vaultx-role'
transformation_name = 'vaultx-fpe-credit-card'
transformations = [transformation_name]

# Create a role and a transformation
client.secrets.transform.create_or_update_role(
    name=role_name,
    transformations=transformations,
)
client.secrets.transform.create_or_update_transformation(
    name=transformation_name,
    transform_type='fpe',
    template='builtin/creditcardnumber',
    tweak_source='internal',
    allowed_roles=[role_name],
)

# Use the role/transformation combination to encode a value
encode_response = client.secrets.transform.encode(
    role_name=role_name,
    value=input_value,
    transformation=transformation_name,
)
print('The encoded value is: %s' % encode_response['data']['encoded_value'])

# Use the role/transformation combination to decode a value
decode_response = client.secrets.transform.decode(
    role_name=role_name,
    value=encode_response['data']['encoded_value'],
    transformation=transformation_name,
)
print('The decoded value is: %s' % decode_response['data']['decoded_value'])
```

**Output:**
```
The encoded value is: ...
The decoded value is: 1111-1111-1111-1111
```

---

## Create/Update Role

`vaultx.api.secrets_engines.Transform.create_or_update_role()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.secrets.transform.create_or_update_role(
    name='vaultx-role',
    transformations=[
        'vaultx-fpe-credit-card',
    ],
)
```

---

## Read Role

`vaultx.api.secrets_engines.Transform.read_role()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

role_name = 'vaultx-role'
client.secrets.transform.create_or_update_role(
    name=role_name,
    transformations=[
        'vaultx-fpe-credit-card',
    ],
)
read_response = client.secrets.transform.read_role(
    name=role_name,
)
print('Role "{}" has the following transformations configured: {}'.format(
    role_name,
    ', '.join(read_response['data']['transformations']),
))
```

**Output:**
```
Role "vaultx-role" has the following transformations configured: vaultx-fpe-credit-card
```

---

## List Roles

`vaultx.api.secrets_engines.Transform.list_roles()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

client.secrets.transform.create_or_update_role(
    name='vaultx-role',
    transformations=[
        'vaultx-fpe-credit-card',
    ],
)
list_response = client.secrets.transform.list_roles()
print('List of transform role names: {}'.format(
    ', '.join(list_response['data']['keys']),
))
```

**Output:**
```
List of transform role names: vaultx-role
```

---

## Delete Role

`vaultx.api.secrets_engines.Transform.delete_role()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

role_name = 'vaultx-role'

# Create a role
client.secrets.transform.create_or_update_role(
    name=role_name,
    transformations=[
        'vaultx-fpe-credit-card',
    ],
)

# Subsequently delete it...
client.secrets.transform.delete_role(
    name=role_name,
)
```

---

## Create/Update Transformation

`vaultx.api.secrets_engines.Transform.create_or_update_transformation()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

transformation_name = 'vaultx-fpe-credit-card'
template = 'builtin/creditcardnumber'
client.secrets.transform.create_or_update_transformation(
    name=transformation_name,
    transform_type='fpe',
    template=template,
    tweak_source='internal',
    allowed_roles=[
        'test-role'
    ],
)
```

---

## Read Transformation

`vaultx.api.secrets_engines.Transform.read_transformation()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

transformation_name = 'vaultx-fpe-credit-card'
template = 'builtin/creditcardnumber'
client.secrets.transform.create_or_update_transformation(
    name=transformation_name,
    transform_type='fpe',
    template=template,
    tweak_source='internal',
    allowed_roles=[
        'vaultx-role'
    ],
)
read_response = client.secrets.transform.read_transformation(
    name=transformation_name,
)
print('Transformation "{}" has the following type configured: {}'.format(
    transformation_name,
    read_response['data']['type'],
))
```

**Output:**
```
Transformation "vaultx-fpe-credit-card" has the following type configured: fpe
```

---

## List Transformations

`vaultx.api.secrets_engines.Transform.list_transformations()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

transformation_name = 'vaultx-fpe-credit-card'
template = 'builtin/creditcardnumber'
client.secrets.transform.create_or_update_transformation(
    name=transformation_name,
    transform_type='fpe',
    template=template,
    tweak_source='internal',
    allowed_roles=[
        'vaultx-role'
    ],
)
list_response = client.secrets.transform.list_transformations()
print('List of transformations: {}'.format(
    ', '.join(list_response['data']['keys']),
))
```

**Output:**
```
List of transformations: vaultx-fpe-credit-card
```

---

## Delete Transformation

`vaultx.api.secrets_engines.Transform.delete_transformation()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

transformation_name = 'vaultx-fpe-credit-card'
template = 'builtin/creditcardnumber'

# Create a transformation
client.secrets.transform.create_or_update_transformation(
    name=transformation_name,
    transform_type='fpe',
    template=template,
    tweak_source='internal',
    allowed_roles=[
        'vaultx-role'
    ],
)

# Subsequently delete it...
client.secrets.transform.delete_transformation(
    name=transformation_name,
)
```

---

## Create/Update Template

`vaultx.api.secrets_engines.Transform.create_or_update_template()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

template_name = 'vaultx-template'
create_response = client.secrets.transform.create_or_update_template(
    name=template_name,
    template_type='regex',
    pattern='(\\d{9})',
    alphabet='builtin/numeric',
)
print(create_response)
```

---

## Read Template

`vaultx.api.secrets_engines.Transform.read_template()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

template_name = 'vaultx-template'
client.secrets.transform.create_or_update_template(
    name=template_name,
    template_type='regex',
    pattern='(\\d{9})',
    alphabet='builtin/numeric',
)
read_response = client.secrets.transform.read_template(
    name=template_name,
)
print('Template "{}" has the following type configured: {}'.format(
    template_name,
    read_response['data']['type'],
))
```

**Output:**
```
Template "vaultx-template" has the following type configured: regex
```

---

## List Templates

`vaultx.api.secrets_engines.Transform.list_templates()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

template_name = 'vaultx-template'
client.secrets.transform.create_or_update_template(
    name=template_name,
    template_type='regex',
    pattern='(\\d{9})',
    alphabet='builtin/numeric',
)
list_response = client.secrets.transform.list_templates()
print('List of templates: {}'.format(
    ', '.join(list_response['data']['keys']),
))
```

**Output:**
```
List of templates: builtin/creditcardnumber, builtin/socialsecuritynumber, vaultx-template
```

---

## Delete Template

`vaultx.api.secrets_engines.Transform.delete_template()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

template_name = 'vaultx-template'
client.secrets.transform.create_or_update_template(
    name=template_name,
    template_type='regex',
    pattern='(\\d{9})',
    alphabet='builtin/numeric',
)

# Subsequently delete it...
client.secrets.transform.delete_template(
    name=template_name,
)
```

---

## Create/Update Alphabet

`vaultx.api.secrets_engines.Transform.create_or_update_alphabet()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

alphabet_name = 'vaultx-alphabet'
alphabet_value = 'abc'
client.secrets.transform.create_or_update_alphabet(
    name=alphabet_name,
    alphabet=alphabet_value,
)
```

---

## Read Alphabet

`vaultx.api.secrets_engines.Transform.read_alphabet()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

alphabet_name = 'vaultx-alphabet'
alphabet_value = 'abc'
client.secrets.transform.create_or_update_alphabet(
    name=alphabet_name,
    alphabet=alphabet_value,
)
read_response = client.secrets.transform.read_alphabet(
    name=alphabet_name,
)
print('Alphabet "{}" has this jazz: {}'.format(
    alphabet_name,
    read_response['data']['alphabet'],
))
```

**Output:**
```
Alphabet "vaultx-alphabet" has this jazz: abc
```

---

## List Alphabets

`vaultx.api.secrets_engines.Transform.list_alphabets()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

alphabet_name = 'vaultx-alphabet'
alphabet_value = 'abc'
client.secrets.transform.create_or_update_alphabet(
    name=alphabet_name,
    alphabet=alphabet_value,
)
list_response = client.secrets.transform.list_alphabets()
print('List of alphabets: {}'.format(
    ', '.join(list_response['data']['keys']),
))
```

**Output:**
```
List of alphabets: builtin/alphalower, ..., vaultx-alphabet
```

---

## Delete Alphabet

`vaultx.api.secrets_engines.Transform.delete_alphabet()`

```python3
import vaultx
client = vaultx.Client(url='https://127.0.0.1:8200')

alphabet_name = 'vaultx-alphabet'
alphabet_value = 'abc'

# Create an alphabet
client.secrets.transform.create_or_update_alphabet(
    name=alphabet_name,
    alphabet=alphabet_value,
)

# Subsequently delete it...
client.secrets.transform.delete_alphabet(
    name=alphabet_name,
)
```
