import os
import warnings
from typing import Optional, Union

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase
from vaultx.exceptions import VaultxError
from vaultx.utils import validate_pem_format


class Cert(VaultApiBase):
    """
    Cert Auth Method (API).

    Reference: https://www.vaultproject.io/api/auth/cert/index.html
    """

    def create_ca_certificate_role(
        self,
        name: str,
        certificate: str = "",
        certificate_file: str = "",
        allowed_common_names: Union[list[str], str] = "",
        allowed_dns_sans: Union[list[str], str] = "",
        allowed_email_sans: Union[list[str], str] = "",
        allowed_uri_sans: Union[list[str], str] = "",
        allowed_organizational_units: Union[list[str], str] = "",
        required_extensions: Union[list[str], str] = "",
        display_name: str = "",
        token_ttl: Union[str, int] = 0,
        token_max_ttl: Union[str, int] = 0,
        token_policies: Optional[Union[list[str], str]] = None,
        token_bound_cidrs: Optional[Union[list[str], str]] = None,
        token_explicit_max_ttl: Union[str, int] = 0,
        token_no_default_policy: bool = False,
        token_num_uses: int = 0,
        token_period: Union[str, int] = 0,
        token_type: str = "",
        mount_point: str = "cert",
    ) -> VaultxResponse:
        """
        Create CA Certificate Role.

        Sets a CA cert and associated parameters in a role name.

        Supported methods:
            POST:	/auth/<mount point>/certs/:name. Produces: 204 (empty body)

        :param name: The name of the certificate role.
        :param certificate: The PEM-format CA certificate. Either certificate or certificate_file is required.
            NOTE: Passing a certificate file path with the certificate argument is deprecated and will be dropped in
            version 3.0.0
        :param certificate_file: File path to the PEM-format CA certificate.  Either certificate_file or certificate is
            required.
        :param allowed_common_names: Constrain the Common Names in the client certificate with a globbed pattern. Value
            is a comma-separated list of patterns. Authentication requires at least one Name matching at least one
            pattern. If not set, defaults to allowing all names.
        :param allowed_dns_sans: Constrain the Alternative Names in the client certificate with a globbed pattern. Value
            is a comma-separated list of patterns. Authentication requires at least
            one DNS matching at least one pattern. If not set, defaults to allowing all dns.
        :param allowed_email_sans: Constrain the Alternative Names in the client certificate with a globbed pattern.
            Value is a comma-separated list of patterns. Authentication requires at least one Email matching at least
            one pattern. If not set, defaults to allowing all emails.
        :param allowed_uri_sans: Constrain the Alternative Names in the client certificate with a globbed pattern.
            Value is a comma-separated list of URI patterns. Authentication requires at least one URI matching at least
            one pattern. If not set, defaults to allowing all URIs.
        :param allowed_organizational_units: Constrain the Organizational Units (OU) in the client certificate with a
            globbed pattern. Value is a comma-separated list of OU patterns. Authentication requires at least one OU
            matching at least one pattern. If not set, defaults to allowing all OUs.
        :param required_extensions: Require specific Custom Extension OIDs to exist and match the pattern. Value is a
            comma separated string or array of oid:value. Expects the extension value to be some type of ASN1 encoded
            string. All conditions must be met. Supports globbing on value.
        :param display_name: The display_name to set on tokens issued when authenticating against this CA certificate.
            If not set, defaults to the name of the role.
        :param token_ttl: The incremental lifetime for generated tokens. This current value of this will be referenced
            at renewal time.
        :param token_max_ttl: The maximum lifetime for generated tokens. This current value of this will be referenced
            at renewal time.
        :param token_policies: List of policies to encode onto generated tokens. Depending on the auth method, this list
            may be supplemented by user/group/other values.
        :param token_bound_cidrs: List of CIDR blocks; if set, specifies blocks of IP addresses which can authenticate
            successfully, and ties the resulting token to these blocks as well.
        :param token_explicit_max_ttl: If set, will encode an explicit max TTL onto the token. This is a hard cap even
            if token_ttl and token_max_ttl would otherwise allow a renewal.
        :param token_no_default_policy: If set, the default policy will not be set on generated tokens; otherwise it
            will be added to the policies set in token_policies.
        :param token_num_uses: The maximum number of times a generated token may be used (within its lifetime); 0 means
            unlimited. If you require the token to have the ability to create child tokens,
            you will need to set this value to 0.
        :param token_period: The period, if any, to set on the token.
        :param token_type: The type of token that should be generated. Can be service, batch, or default to use the
            mount's tuned default (which unless changed will be service tokens). For token store roles, there are two
            additional possibilities: default-service and default-batch which specify the type to return unless the
            client requests a different type at generation time.
        :param mount_point:
        """
        token_policies = [] if token_policies is None else token_policies
        token_bound_cidrs = [] if token_bound_cidrs is None else token_bound_cidrs
        if certificate:
            try:
                utils.validate_pem_format("", certificate)
                cert = certificate
            except VaultxError:
                with open(certificate) as f_cert:
                    warnings.warn(
                        "Passing a certificate file path to `certificate` is deprecated."
                        "Use `certificate_file` instead.",
                        stacklevel=2,
                    )
                    cert = f_cert.read()
        elif certificate_file:
            with open(certificate_file) as f_cert:
                cert = f_cert.read()
        else:
            raise VaultxError("`certificate` or `certificate_file` must be provided")

        params = utils.remove_nones(
            {
                "name": name,
                "certificate": cert,
                "allowed_common_names": allowed_common_names,
                "allowed_dns_sans": allowed_dns_sans,
                "allowed_email_sans": allowed_email_sans,
                "allowed_uri_sans": allowed_uri_sans,
                "allowed_organizational_units": allowed_organizational_units,
                "required_extensions": required_extensions,
                "display_name": display_name,
                "token_ttl": token_ttl,
                "token_max_ttl": token_max_ttl,
                "token_policies": token_policies,
                "token_bound_cidrs": token_bound_cidrs,
                "token_explicit_max_ttl": token_explicit_max_ttl,
                "token_no_default_policy": token_no_default_policy,
                "token_num_uses": token_num_uses,
                "token_period": token_period,
                "token_type": token_type,
            }
        )

        api_path = f"/v1/auth/{mount_point}/certs/{name}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_ca_certificate_role(self, name: str, mount_point: str = "cert") -> VaultxResponse:
        """
        Get information associated with the named role.

        Supported methods:
            GET: /auth/<mount point>/certs/{name}. Produces: 200 application/json

        :param name: The name of the certificate role
        :param mount_point:
        :return: The VaultxResponse of the read_ca_certificate_role request.
        """
        params = {
            "name": name,
        }
        api_path = f"/v1/auth/{mount_point}/certs/{name}"
        return self._adapter.get(
            url=api_path,
            json=params,
        )

    def list_certificate_roles(self, mount_point: str = "cert") -> VaultxResponse:
        """
        List configured certificate names.

        Supported methods:
            LIST: /auth/<mount point>/certs. Produces: 200 application/json

        :param mount_point:
        :type mount_point:
        :return: The response of the list_certificate request.
        """
        api_path = f"/v1/auth/{mount_point}/certs"
        return self._adapter.list(url=api_path)

    def delete_certificate_role(self, name: str, mount_point: str = "cert") -> VaultxResponse:
        """
        List existing LDAP existing groups that have been created in this auth method.

        Supported methods:
            DELETE: /auth/{mount_point}/groups. Produces: 204 (empty body)

        :param name: The name of the certificate role.
        :param mount_point:
        """
        api_path = f"/v1/auth/{mount_point}/certs/{name}"
        return self._adapter.delete(
            url=api_path,
        )

    def configure_tls_certificate(self, mount_point: str = "cert", disable_binding: bool = False) -> VaultxResponse:
        """
        Configure options for the method.

        Supported methods:
            POST: /auth/<mount point>/config. Produces: 204 (empty body)

        :param disable_binding: If set, during renewal, skips the matching of presented client identity with the client
            identity used during login.
        :param mount_point:
        """
        params = {
            "disable_binding": disable_binding,
        }
        api_path = f"/v1/auth/{mount_point}/config"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def _validate_cacert(self, cacert: str) -> str:
        """Validate the CA certificate or use the adapter's certificate."""
        if not cacert:
            if not self._adapter._kwargs.get("verify"):
                raise VaultxError("CertificateAuthError: cacert must be True, a file_path, or valid CA Certificate.")
            cacert = self._adapter._kwargs.get("verify", "")
        else:
            validate_pem_format("verify", cacert)
        return cacert

    def _validate_cert_pem(self, cert_pem: str, key_pem: str) -> Union[bool, dict]:
        """Validate the cert_pem and key_pem parameters."""
        try:
            if validate_pem_format("cert_pem", cert_pem):
                return True
        except VaultxError as e:
            if not (os.path.exists(cert_pem) or self._adapter._kwargs.get("cert")):
                raise FileNotFoundError("Can't find the certificate.") from e
            return {"cert_pem": cert_pem, "key_pem": key_pem}
        return False

    def login(
        self,
        name: str = "",
        cacert: str = "",
        cert_pem: str = "",
        key_pem: str = "",
        mount_point: str = "cert",
        use_token: bool = True,
    ) -> VaultxResponse:
        """
        Log in and fetch a token. If there is a valid chain to a CA configured in the method and all role constraints
            are matched, a token will be issued. If the certificate has DNS SANs in it, each of those will be verified.
            If Common Name is required to be verified, then it should be a fully qualified DNS domain name and must be
            duplicated as a DNS SAN

        Supported methods:
            POST: /auth/<mount point>/login Produces: 200 application/json

        :param name: Authenticate against only the named certificate role, returning its policy list if successful. If
            not set, defaults to trying all certificate roles and returning any one that matches.
        :param cacert: The value used here is for the Vault TLS Listener CA certificate, not the CA that issued the
            client authentication certificate. This can be omitted if the CA used to issue the Vault server certificate
            is trusted by the local system executing this command.
        :param cert_pem: cert.pem directly or the location of the cert.pem used to authenticate the host.
        :param key_pem: Location of the public key.pem used to authenticate the host.
        :param mount_point:
        :param use_token: If the returned token is stored in the client
        :return: The response of the login request.
        """
        params = {}
        if name != "":
            params["name"] = name
        api_path = f"/v1/auth/{mount_point}/login"

        cacert = self._validate_cacert(cacert)

        tls_update = self._validate_cert_pem(cert_pem, key_pem)

        additional_request_kwargs = {}
        if tls_update:
            additional_request_kwargs = {
                "verify": cacert,
                "cert": ([cert_pem, key_pem]),
            }

        return self._adapter.login(url=api_path, use_token=use_token, json=params, **additional_request_kwargs)
