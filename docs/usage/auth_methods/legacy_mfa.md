# Legacy MFA

## Configure Legacy MFA Auth Method Settings

`vaultx.api.auth_methods.LegacyMfa.configure()`

>**Note**: The legacy/unsupported MFA auth method covered by this class’s configuration API route only supports integration with a subset of Vault auth methods. See the list of supported auth methods in this module’s "SUPPORTED_AUTH_METHODS" attribute and/or the associated Vault LegacyMFA documentation for additional information.

```python3
import vaultx
client = vaultx.Client()

userpass_auth_path = 'some-userpass'

if f'{userpass_auth_path}/' not in client.sys.list_auth_methods()['data']:
    print(f'Enabling the userpass auth backend at mount_point: {userpass_auth_path}')
    client.sys.enable_auth_method(
        method_type='userpass',
        path=userpass_auth_path,
    )

client.auth.legacymfa.configure(
    mount_point=userpass_auth_path,
)
```

## Reading the Legacy MFA Auth Method Configuration

`vaultx.api.auth_methods.LegacyMfa.read_configuration()`

```python3
import vaultx
client = vaultx.Client()

mfa_configuration = client.auth.legacymfa.read_configuration()
print('The LegacyMFA auth method is configured with a MFA type of: {mfa_type}'.format(
    mfa_type=mfa_configuration['data']['type']
)
```

## Configure Duo LegacyMFA Type Access Credentials

`vaultx.api.auth_methods.LegacyMfa.configure_duo_access()`

```python3
from getpass import getpass

import vaultx
client = vaultx.Client()

secret_key_prompt = 'Please enter the Duo access secret key to configure: '
duo_access_secret_key = getpass(prompt=secret_key_prompt)

client.auth.legacymfa.configure_duo_access(
    mount_point=userpass_auth_path,
    host='api-1234abcd.duosecurity.com',
    integration_key='SOME_DUO_IKEY',
    secret_key=duo_access_secret_key,
)
```

## Configure Duo Legacy MFA Type Behavior

`vaultx.api.auth_methods.LegacyMfa.configure_duo_behavior()`

```python3
import vaultx
client = vaultx.Client()

client.auth.legacymfa.configure_duo_behavior(
    mount_point=userpass_auth_path,
    username_format='%s@vaultx.network',
)
```

## Read Duo Legacy MFA Type Behavior

`vaultx.api.auth_methods.LegacyMfa.read_duo_behavior_configuration()`

```python3
import vaultx
client = vaultx.Client()

duo_behavior_config = client.auth.legacymfa.read_duo_behavior_configuration(
    mount_point=userpass_auth_path,
)
print('The Duo LegacyMFA behavior is configured with a username_format of: {username_format}'.format(
    username_format=duo_behavior_config['data']['username_format'],
))
```

## Authentication / Login

```python3
from getpass import getpass

import vaultx

login_username = 'someuser'
password_prompt = 'Please enter your password for the userpass (with MFA) authentication backend: '
login_password = getpass(prompt=password_prompt)
passcode_prompt = 'Please enter your OTP for the userpass (with MFA) authentication backend: '
userpass_mfa_passcode = getpass(prompt=passcode_prompt)

client = vaultx.Client()

# Here the mount_point parameter corresponds to the path provided when enabling the backend
client.auth.legacymfa.auth_userpass(
    username=login_username,
    password=login_password,
    mount_point=userpass_auth_path,
    passcode=userpass_mfa_passcode,
)
print(client.is_authenticated)  # => True
```
