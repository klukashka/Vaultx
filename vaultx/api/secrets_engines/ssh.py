from typing import Optional

from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase


DEFAULT_MOUNT_POINT = "ssh"


class Ssh(VaultApiBase):
    """
    SSH Secrets Engine (API).
    Reference: https://www.vaultproject.io/api-docs/secret/ssh
    """

    def create_role(
        self,
        name: str = "",
        key: str = "",
        admin_user: str = "",
        default_user: str = "",
        cidr_list: str = "",
        exclude_cidr_list: str = "",
        port: int = 22,
        key_type: str = "",
        key_bits: int = 1024,
        install_script: str = "",
        allowed_users: str = "",
        allowed_users_template: str = "",
        allowed_domains: str = "",
        key_option_specs: str = "",
        ttl: str = "",
        max_ttl: str = "",
        allowed_critical_options: str = "",
        allowed_extensions: str = "",
        default_critical_options: Optional[dict] = None,
        default_extensions: Optional[dict] = None,
        allow_user_certificates: str = "",
        allow_host_certificates: bool = False,
        allow_bare_domains: bool = False,
        allow_subdomains: bool = False,
        allow_user_key_ids: bool = False,
        key_id_format: str = "",
        allowed_user_key_lengths: Optional[dict[str, int]] = None,
        algorithm_signer: str = "",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint creates or updates a named role.

        :param name: Specifies the name of the role to create.
        :param key: Specifies the name of the registered key in Vault.
        :param admin_user: Specifies the admin user at remote host.
        :param default_user: Specifies the default username for which a credential will be generated.
        :param cidr_list: Specifies a comma separated list of CIDR blocks for which the role is applicable for.
        :param exclude_cidr_list: Specifies a comma-separated list of CIDR blocks.
        :param port: Specifies the port number for SSH connection.
        :param key_type:  Specifies the type of credentials generated by this role.
        :param key_bits: Specifies the length of the RSA dynamic key in bits. (default: 1024)
        :param install_script: Specifies the script used to install and uninstall public keys in the target machine.
        :param allowed_users: If only certain usernames are to be allowed, then this list enforces it.
        :param allowed_users_template: If set, allowed_users can be specified using identity template policies.
            (default: false)
        :param allowed_domains: The list of domains for which a client can request a host certificate.
        :param key_option_specs: Specifies a comma separated option specification which will be prefixed to RSA keys in
            the remote host's authorized_keys file.
        :param ttl: Specifies the Time To Live value provided as a string duration with time suffix.
        :param max_ttl: Specifies the Time To Live value provided as a string duration with time suffix.
        :param allowed_critical_options: Specifies a comma-separated list of critical options that certificates can have
            when signed.
        :param allowed_extensions: Specifies a comma-separated list of extensions that certificates can have when
            signed.
        :param default_critical_options: Specifies a map of critical options certificates should have if none are
            provided when signing.
        :param default_extensions: Specifies a map of extensions certificates should have if none are provided when
            signing.
        :param allow_user_certificates: Specifies if certificates are allowed to be signed for use as a 'user'.
            (default: False)
        :param allow_host_certificates: Specifies if certificates are allowed to be signed for use as a 'host'.
            (default: False)
        :param allow_bare_domains: Specifies if host certificates that are requested are allowed to use the base domains
            listed in allowed_domains, e.g. "example.com". (default: False)
        :param allow_subdomains: Specifies if host certificates that are requested are allowed to be subdomains of those
            listed in allowed_domains. (default: False)
        :param allow_user_key_ids: Specifies if users can override the key ID for a signed certificate with the "key_id"
            field. (default: False)
        :param key_id_format: When supplied, this value specifies a custom format for the key id of a signed
            certificate.
        :param allowed_user_key_lengths: Specifies a map of ssh key types and their expected sizes which are allowed to
            be signed by the CA type.
        :param algorithm_signer: Algorithm to sign keys with. (default: "default")
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        params = {
            "key": key,
            "admin_user": admin_user,
            "default_user": default_user,
            "cidr_list": cidr_list,
            "exclude_cidr_list": exclude_cidr_list,
            "port": port,
            "key_type": key_type,
            "key_bits": key_bits,
            "install_script": install_script,
            "allowed_users": allowed_users,
            "allowed_users_template": allowed_users_template,
            "allowed_domains": allowed_domains,
            "key_option_specs": key_option_specs,
            "ttl": ttl,
            "max_ttl": max_ttl,
            "allowed_critical_options": allowed_critical_options,
            "allowed_extensions": allowed_extensions,
            "default_critical_options": default_critical_options,
            "default_extensions": default_extensions,
            "allow_user_certificates": allow_user_certificates,
            "allow_host_certificates": allow_host_certificates,
            "allow_bare_domains": allow_bare_domains,
            "allow_subdomains": allow_subdomains,
            "allow_user_key_ids": allow_user_key_ids,
            "key_id_format": key_id_format,
            "allowed_user_key_lengths": allowed_user_key_lengths,
            "algorithm_signer": algorithm_signer,
        }

        api_path = f"/v1/{mount_point}/roles/{name}"
        return self._adapter.post(url=api_path, json=params)

    def read_role(
        self,
        name: str = "",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint queries a named role.

        :param name: Specifies the name of the role to read.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        return self._adapter.get(url=api_path)

    def list_roles(
        self,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint returns a list of available roles. Only the role names are returned, not any values.

        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        api_path = f"/v1/{mount_point}/roles"
        return self._adapter.list(url=api_path)

    def delete_role(self, name: str = "", mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint deletes a named role.

        :param name:
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        return self._adapter.delete(url=api_path)

    def list_zeroaddress_roles(
        self,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint returns the list of configured zero-address roles.

        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        api_path = f"/v1/{mount_point}/config/zeroaddress"
        return self._adapter.get(url=api_path)

    def configure_zeroaddress_roles(
        self,
        roles: str = "",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint configures zero-address roles.

        :param roles: Specifies a string containing comma separated list of role names which allows credentials
            to be requested for any IP address.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        params = {
            "roles": roles,
        }

        api_path = f"/v1/{mount_point}/config/zeroaddress"

        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def delete_zeroaddress_role(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint deletes the zero-address roles configuration.

        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        api_path = f"/v1/{mount_point}/config/zeroaddress"

        return self._adapter.delete(
            url=api_path,
        )

    def generate_ssh_credentials(
        self,
        name: str = "",
        username: str = "",
        ip: str = "",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint creates credentials for a specific username and IP with the parameters defined in the given role.

        :param name: Specifies the name of the role to create credentials against. This is part of the request URL.
        :param username: Specifies the username on the remote host.
        :param ip: Specifies the IP of the remote host.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        params = {
            "username": username,
            "ip": ip,
        }

        api_path = f"/v1/{mount_point}/creds/{name}"
        return self._adapter.post(url=api_path, json=params)

    def list_roles_by_ip(
        self,
        ip: str = "",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint lists all the roles with which the given IP is associated.

        :param ip: Specifies the IP of the remote host.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        params = {
            "ip": ip,
        }

        api_path = f"/v1/{mount_point}/lookup"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def verify_ssh_otp(
        self,
        otp: str,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint verifies if the given OTP is valid. This is an unauthenticated endpoint.

        :param otp: Specifies the One-Time-Key that needs to be validated.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        params = {
            "otp": otp,
        }

        api_path = f"v1/{mount_point}/verify"

        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def submit_ca_information(
        self,
        private_key: str = "",
        public_key: str = "",
        generate_signing_key: bool = True,
        key_type: str = "ssh-rsa",
        key_bits: int = 0,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint allows submitting the CA information for the secrets engine via an SSH key pair.

        :param private_key: Specifies the private key part the SSH CA key pair.
        :param public_key: Specifies the public key part of the SSH CA key pair.
        :param generate_signing_key: Specifies if Vault should generate the signing key pair internally. (default: True)
        :param key_type: Specifies the desired key type for the generated SSH CA key when generate_signing_key
            is set to true. (default: ssh-rsa)
        :param key_bits: Specifies the desired key bits for the generated SSH CA key when generate_signing_key
            is set to true. (default: 0)
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        params = {
            "private_key": private_key,
            "public_key": public_key,
            "generate_signing_key": generate_signing_key,
            "key_type": key_type,
            "key_bits": key_bits,
        }

        api_path = f"/v1/{mount_point}/config/ca"

        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def delete_ca_information(
        self,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint deletes the CA information for the backend via an SSH key pair.

        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        api_path = f"/v1/{mount_point}/config/ca"

        return self._adapter.delete(url=api_path)

    def read_public_key(
        self,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint reads the configured/generated public key.

        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        api_path = f"/v1/{mount_point}/config/ca"

        return self._adapter.get(url=api_path)

    def sign_ssh_key(
        self,
        name: str = "",
        public_key: str = "",
        ttl: str = "",
        valid_principals: str = "",
        cert_type: str = "user",
        key_id: str = "",
        critical_options: Optional[dict] = None,
        extensions: Optional[dict] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint signs an SSH public key based on the supplied parameters,
        subject to the restrictions contained in the role named in the endpoint.

        :param name: Specifies the name of the role to sign. This is part of the request URL.
        :param public_key: Specifies the SSH public key that should be signed.
        :param ttl: Specifies the Requested Time To Live.
        :param valid_principals: Specifies valid principals that the certificate should be signed for.
        :param cert_type: Specifies the type of certificate to be created; either "user" or "host". (default: user)
        :param key_id: Specifies the key id that the created certificate should have.
        :param critical_options: Specifies a map of the critical options that the certificate should be signed for.
        :param extensions: Specifies a map of the extensions that the certificate should be signed for.
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ssh).
        :return: The VaultxResponse of the request
        """
        params = {
            "public_key": public_key,
            "ttl": ttl,
            "valid_principals": valid_principals,
            "cert_type": cert_type,
            "key_id": key_id,
            "critical_options": critical_options,
            "extensions": extensions,
        }

        api_path = f"/v1/{mount_point}/sign/{name}"

        return self._adapter.post(
            url=api_path,
            json=params,
        )
