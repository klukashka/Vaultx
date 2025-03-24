# GitHub

>**Note**: Every method under the Client class's github attribute includes a mount_point parameter that can be used to address the Github auth method under a custom mount path. E.g., If enabling the Github auth method using Vault’s CLI commands via vault auth enable -path=my-github github”, the mount_point parameter in vaultx.api.auth_methods.Github() methods would be set to “my-github”.

## Enabling the Auth Method

`vaultx.api.SystemBackend.enable_auth_method()`

```python3
import vaultx
client = vaultx.Client()

github_auth_path = 'company-github'
description = 'Auth method for use by team members in our company'

if f"{github_auth_path}/" not in client.sys.list_auth_methods()['data']:
    print(f'Enabling the github auth backend at mount_point: {github_auth_path}')
    client.sys.enable_auth_method(
        method_type='github',
        description=description,
        path=github_auth_path,
    )
```

## Configure Connection Parameters

`vaultx.api.auth_methods.Github.configure()`

```python3
import vaultx
client = vaultx.Client()

client.auth.github.configure(
    organization='our-lovely-company',
    max_ttl='48h',  # i.e., A given token can only be renewed for up to 48 hours
)
```

## Reading Configuration

`vaultx.api.auth_methods.Github.read_configuration()`

```python3
import vaultx
client = vaultx.Client()

github_config = client.auth.github.read_configuration()
print(f'The Github auth method is configured with a ttl of: {github_config['data']['ttl']}')
```

## Mapping Teams to Policies

`vaultx.api.auth_methods.Github.map_team()`

```python3
import vaultx
client = vaultx.Client()

teams = [
    dict(name='some-dev-team', policies=['dev-team']),
    dict(name='admin-team', policies=['administrator']),
]
for team in teams:
    client.auth.github.map_team(
        team_name=team['name'],
        policies=team['policies'],
    )
```

## Reading Team Mappings

`vaultx.api.auth_methods.Github.read_team_mapping()`

```python3
import vaultx
client = vaultx.Client()

team_name = 'my-super-cool-team'
github_config = client.auth.github.read_team_mapping(
    team_name=team_name,
)
print(f'The Github team {team_name} is mapped to the following policies: {github_config['data']['value']}')
```

## Mapping Users to Policies

`vaultx.api.auth_methods.Github.map_user()`

```python3
import vaultx
client = vaultx.Client()

users = [
    dict(name='some-dev-user', policies=['dev-team']),
    dict(name='some-admin-user', policies=['administrator']),
]
for user in users:
    client.auth.github.map_user(
        user_name=user['name'],
        policies=user['policies'],
    )
```

## Reading User Mappings

`vaultx.api.auth_methods.Github.read_user_mapping()`

```python3
import vaultx
client = vaultx.Client()

user_name = 'some-dev-user'
github_config = client.auth.github.read_user_mapping(
    user_name=user_name,
)
print('The Github user "{user}" is mapped to the following policies: {policies}'.format(
    user=user_name,
    policies=github_config['data']['value'],
)
```

## Authentication / Login

`vaultx.api.auth_methods.Github.login()`

Log in and automatically update the underlying “token” attribute on the vaultx.adapters.Adapter() instance:

```python3
import vaultx
client = vaultx.Client()
login_response = client.auth.github.login(token='some personal github token')
```
