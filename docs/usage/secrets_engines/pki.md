# PKI

## Read CA Certificate

`vaultx.api.secrets_engines.PKI.read_ca_certificate()`

Retrieve the current CA certificate.

```python3
import vaultx
client = vaultx.Client()

read_ca_certificate_response = client.secrets.pki.read_ca_certificate()
print('Current PKI CA Certificate: {}'.format(read_ca_certificate_response))
```

## Read CA Certificate Chain

`vaultx.api.secrets_engines.PKI.read_ca_certificate_chain()`

Retrieve the current CA certificate chain.

```python3
import vaultx
client = vaultx.Client()

read_ca_certificate_chain_response = client.secrets.pki.read_ca_certificate_chain()
print('Current PKI CA Certificate Chain: {}'.format(read_ca_certificate_chain_response))
```

## Read Certificate

`vaultx.api.secrets_engines.PKI.read_certificate()`

Retrieve a certificate by its serial number.

```python3
import vaultx
client = vaultx.Client()

read_certificate_response = client.secrets.pki.read_certificate(serial='crl')
print('Current PKI CRL: {}'.format(read_certificate_response))
```

## List Certificates

`vaultx.api.secrets_engines.PKI.list_certificates()`

List all certificates by their serial numbers.

```python3
import vaultx
client = vaultx.Client()

list_certificate_response = client.secrets.pki.list_certificates()
print('Current certificates (serial numbers): {}'.format(list_certificate_response))
```

## Submit CA Information

`vaultx.api.secrets_engines.PKI.submit_ca_information()`

Submit CA information to the PKI secrets engine.

```python3
import vaultx
client = vaultx.Client()

submit_ca_information_response = client.secrets.pki.submit_ca_information(
    '-----BEGIN RSA PRIVATE KEY-----\n...\n-----END CERTIFICATE-----'
)
print(submit_ca_information_response)
```

## Read CRL Configuration

`vaultx.api.secrets_engines.PKI.read_crl_configuration()`

Retrieve the current CRL configuration.

```python3
import vaultx
client = vaultx.Client()

read_crl_configuration_response = client.secrets.pki.read_crl_configuration()
print('CRL configuration: {}'.format(read_crl_configuration_response))
```

## Set CRL Configuration

`vaultx.api.secrets_engines.PKI.set_crl_configuration()`

Configure the CRL expiration and disable/enable status.

```python3
import vaultx
client = vaultx.Client()

set_crl_configuration_response = client.secrets.pki.set_crl_configuration(
    expiry='72h',
    disable=False
)
print(set_crl_configuration_response)
```

## Read URLs

`vaultx.api.secrets_engines.PKI.read_urls()`

Retrieve the current PKI URLs.

```python3
import vaultx
client = vaultx.Client()

read_urls_response = client.secrets.pki.read_urls()
print('Get PKI URLs: {}'.format(read_urls_response))
```

## Set URLs

`vaultx.api.secrets_engines.PKI.set_urls()`

Configure the PKI URLs.

```python3
import vaultx
client = vaultx.Client()

set_urls_response = client.secrets.pki.set_urls(
    {
        'issuing_certificates': ['http://127.0.0.1:8200/v1/pki/ca'],
        'crl_distribution_points': ['http://127.0.0.1:8200/v1/pki/crl']
    }
)
print(set_urls_response)
```

## Read CRL

`vaultx.api.secrets_engines.PKI.read_crl()`

Retrieve the current Certificate Revocation List (CRL).

```python3
import vaultx
client = vaultx.Client()

read_crl_response = client.secrets.pki.read_crl()
print('Current CRL: {}'.format(read_crl_response))
```

## Rotate CRLs

`vaultx.api.secrets_engines.PKI.rotate_crl()`

Rotate the CRL.

```python3
import vaultx
client = vaultx.Client()

rotate_crl_response = client.secrets.pki.rotate_crl()
print('Rotate CRL: {}'.format(rotate_crl_response))
```

## Generate Intermediate

`vaultx.api.secrets_engines.PKI.generate_intermediate()`

Generate an intermediate CA certificate.

```python3
import vaultx
client = vaultx.Client()

generate_intermediate_response = client.secrets.pki.generate_intermediate(
    type='exported',
    common_name='Vault integration tests'
)
print('Intermediate certificate: {}'.format(generate_intermediate_response))
```

## Set Signed Intermediate

`vaultx.api.secrets_engines.PKI.set_signed_intermediate()`

Set a signed intermediate CA certificate.

```python3
import vaultx
client = vaultx.Client()

set_signed_intermediate_response = client.secrets.pki.set_signed_intermediate(
    '-----BEGIN CERTIFICATE...'
)
print(set_signed_intermediate_response)
```

## Generate Certificate

`vaultx.api.secrets_engines.PKI.generate_certificate()`

Generate a certificate using a role.

```python3
import vaultx
client = vaultx.Client()

generate_certificate_response = client.secrets.pki.generate_certificate(
    name='myrole',
    common_name='test.example.com'
)
print('Certificate: {}'.format(generate_certificate_response))
```

## Revoke Certificate

`vaultx.api.secrets_engines.PKI.revoke_certificate()`

Revoke a certificate by its serial number.

```python3
import vaultx
client = vaultx.Client()

revoke_certificate_response = client.secrets.pki.revoke_certificate(
    serial_number='39:dd:2e...'
)
print('Certificate: {}'.format(revoke_certificate_response))
```

## Create/Update Role

`vaultx.api.secrets_engines.PKI.create_or_update_role()`

Create or update a role for certificate generation.

```python3
import vaultx
client = vaultx.Client()

create_or_update_role_response = client.secrets.pki.create_or_update_role(
    'mynewrole',
    {
        'ttl': '72h',
        'allow_localhost': 'false'
    }
)
print('New role: {}'.format(create_or_update_role_response))
```

## Read Role

`vaultx.api.secrets_engines.PKI.read_role()`

Retrieve the configuration of a role.

```python3
import vaultx
client = vaultx.Client()

read_role_response = client.secrets.pki.read_role('myrole')
print('Role definition: {}'.format(read_role_response))
```

## List Roles

`vaultx.api.secrets_engines.PKI.list_roles()`

List all available roles.

```python3
import vaultx
client = vaultx.Client()

list_roles_response = client.secrets.pki.list_roles()
print('List of available roles: {}'.format(list_roles_response))
```

## Delete Role

`vaultx.api.secrets_engines.PKI.delete_role()`

Delete a role.

```python3
import vaultx
client = vaultx.Client()

delete_role_response = client.secrets.pki.delete_role('role2delete')
print(delete_role_response)
```

## Generate Root

`vaultx.api.secrets_engines.PKI.generate_root()`

Generate a new root CA certificate.

```python3
import vaultx
client = vaultx.Client()

generate_root_response = client.secrets.pki.generate_root(
    type='exported',
    common_name='New root CA'
)
print('New root CA: {}'.format(generate_root_response))
```

## Delete Root

`vaultx.api.secrets_engines.PKI.delete_root()`

Delete the current root CA certificate.

```python3
import vaultx
client = vaultx.Client()

delete_root_response = client.secrets.pki.delete_root()
print(delete_root_response)
```

## Sign Intermediate

`vaultx.api.secrets_engines.PKI.sign_intermediate()`

Sign an intermediate CA certificate.

```python3
import vaultx
client = vaultx.Client()

sign_intermediate_response = client.secrets.pki.sign_intermediate(
    csr='....',
    common_name='example.com',
)
print('Signed certificate: {}'.format(sign_intermediate_response))
```

## Sign Self-Issued

`vaultx.api.secrets_engines.PKI.sign_self_issued()`

Sign a self-issued certificate.

```python3
import vaultx
client = vaultx.Client()

sign_self_issued_response = client.secrets.pki.sign_self_issued(
    certificate='...'
)
print('Signed certificate: {}'.format(sign_self_issued_response))
```

## Sign Certificate

`vaultx.api.secrets_engines.PKI.sign_certificate()`

Sign a certificate using a role.

```python3
import vaultx
client = vaultx.Client()

sign_certificate_response = client.secrets.pki.sign_certificate(
    name='myrole',
    csr='...',
    common_name='example.com'
)
print('Signed certificate: {}'.format(sign_certificate_response))
```

## Sign Verbatim

`vaultx.api.secrets_engines.PKI.sign_verbatim()`

Sign a certificate verbatim.

```python3
import vaultx
client = vaultx.Client()

sign_verbatim_response = client.secrets.pki.sign_verbatim(
    name='myrole',
    csr='...'
)
print('Signed certificate: {}'.format(sign_verbatim_response))
```

## Tidy

`vaultx.api.secrets_engines.PKI.tidy()`

Tidy up the PKI secrets engine.

```python3
import vaultx
client = vaultx.Client()

tidy_response = client.secrets.pki.tidy()
print(tidy_response)
```

## Read Issuer

`vaultx.api.secrets_engines.PKI.read_issuer()`

Retrieve details of a specific issuer.

```python3
import vaultx
client = vaultx.Client()

issuer_list_response = client.secrets.pki.list_issuers()
issuer_read_response = client.secrets.pki.read_issuer(issuer_list_response["keys"][0])
print(issuer_read_response)
```

## List Issuers

`vaultx.api.secrets_engines.PKI.list_issuers()`

List all available issuers.

```python3
import vaultx
client = vaultx.Client()

issuer_list_response = client.secrets.pki.list_issuers()
print(issuer_list_response)
```

## Update Issuer

`vaultx.api.secrets_engines.PKI.update_issuer()`

Update an issuer's configuration.

```python3
import vaultx
client = vaultx.Client()

issuer_list_response = client.secrets.pki.list_issuers()
issuer_update_response = client.secrets.pki.update_issuer(
    issuer_list_response["keys"][0],
    extra_params={'issuer_name': 'my_new_issuer_name'}
)
print(issuer_update_response)
```

## Revoke Issuer

`vaultx.api.secrets_engines.PKI.revoke_issuer()`

Revoke an issuer.

```python3
import vaultx
client = vaultx.Client()

issuer_list_response = client.secrets.pki.list_issuers()
issuer_revoke_response = client.secrets.pki.revoke_issuer(issuer_list_response["keys"][0])
print(issuer_revoke_response)
```

## Delete Issuer

`vaultx.api.secrets_engines.PKI.delete_issuer()`

Delete an issuer.

```python3
import vaultx
client = vaultx.Client()

issuer_list_response = client.secrets.pki.list_issuers()
issuer_delete_response = client.secrets.pki.delete_issuer(issuer_list_response["keys"][0])
print(issuer_delete_response)
```
