from typing import Optional, Union

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase


DEFAULT_MOUNT_POINT = "ldap"


class Ldap(VaultApiBase):
    """
    LDAP Secrets Engine (API).
    Reference: https://www.vaultproject.io/api/secret/ldap/index.html
    """

    def configure(
        self,
        binddn: Optional[str] = None,
        bindpass: Optional[str] = None,
        url: Optional[str] = None,
        password_policy: Optional[str] = None,
        schema: Optional[str] = None,
        userdn: Optional[str] = None,
        userattr: Optional[str] = None,
        upndomain: Optional[str] = None,
        connection_timeout: Optional[Union[str, int]] = None,
        request_timeout: Optional[Union[str, int]] = None,
        starttls: Optional[bool] = None,
        insecure_tls: Optional[bool] = None,
        certificate: Optional[str] = None,
        client_tls_cert: Optional[str] = None,
        client_tls_key: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure shared information for the ldap secrets engine.

        Supported methods:
            POST: /{mount_point}/config. Produces: 204 (empty body)

        :param binddn: Distinguished name of object to bind when performing user and group search.
        :param bindpass: Password to use along with binddn when performing user search.
        :param url: Base DN under which to perform user search.
        :param userdn: Base DN under which to perform user search.
        :param userattr: The attribute field name used to perform user search in library management and static roles.
        :param upndomain: userPrincipalDomain used to construct the UPN string for the authenticating user.
        :param password_policy: The name of the password policy to use to generate passwords.
        :param schema: The LDAP schema to use when storing entry passwords.
            Valid schemas include ``openldap``, ``ad``, and ``racf``.
        :param connection_timeout: Timeout, in seconds, when attempting to connect to the LDAP server before
            trying the next URL in the configuration.
        :param request_timeout: Timeout, in seconds, for the connection when making requests against the server before
            returning back an error.
        :param starttls: If true, issues a StartTLS command after establishing an unencrypted connection.
        :param insecure_tls: If true, skips LDAP server SSL certificate verification - insecure, use with caution!
        :param certificate: CA certificate to use when verifying LDAP server certificate, must be x509 PEM encoded.
        :param client_tls_cert: Client certificate to provide to the LDAP server, must be x509 PEM encoded.
        :param client_tls_key: Client key to provide to the LDAP server, must be x509 PEM encoded.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = utils.remove_nones(
            {
                "binddn": binddn,
                "bindpass": bindpass,
                "url": url,
                "userdn": userdn,
                "userattr": userattr,
                "upndomain": upndomain,
                "password_policy": password_policy,
                "schema": schema,
                "connection_timeout": connection_timeout,
                "request_timeout": request_timeout,
                "starttls": starttls,
                "insecure_tls": insecure_tls,
                "certificate": certificate,
                "client_tls_cert": client_tls_cert,
                "client_tls_key": client_tls_key,
            }
        )

        api_path = f"/v1/{mount_point}/config"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the configured shared information for the ldap secrets engine.
        Credentials will be omitted from returned data.

        Supported methods:
            GET: /{mount_point}/config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config"
        return self._adapter.get(
            url=api_path,
        )

    def rotate_root(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Rotate the root password for the binddn entry used to manage the ldap secrets engine.

        Supported methods:
            POST: /{mount_point}/rotate root. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/rotate-root"
        return self._adapter.post(url=api_path)

    def create_or_update_static_role(
        self,
        name: str,
        username: Optional[str] = None,
        dn: Optional[str] = None,
        rotation_period: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint creates or updates the ldap static role definition.

        :param name: Specifies the name of an existing static role against which to create this ldap credential.
        :param username: The name of a pre-existing service account in LDAP that maps to this static role.
            This value is required on create and cannot be updated.
        :param dn: Distinguished name of the existing LDAP entry to manage password rotation
            for (takes precedence over username). Optional but cannot be modified after creation.
        :param rotation_period: How often Vault should rotate the password.
            This is provided as a string duration with a time suffix like "30s" or "1h" or as seconds.
            If not provided, the default Vault rotation_period is used.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/static-role/{name}"
        params = {"username": username, "rotation_period": rotation_period}
        params.update(utils.remove_nones({"dn": dn}))
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_static_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint queries for information about a ldap static role with the given name.
        If no role exists with that name, a 404 is returned.
        :param name: Specifies the name of the static role to query.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/static-role/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def list_static_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint lists all existing static roles in the secrets engine.
        :return: The response of the request.
        :rtype: requests.Response
        """
        api_path = f"/v1/{mount_point}/static-role"
        return self._adapter.list(
            url=api_path,
        )

    def delete_static_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint deletes a ldap static role with the given name.
        Even if the role does not exist, this endpoint will still return a successful response.
        :param name: Specifies the name of the role to delete.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/static-role/{name}"
        return self._adapter.delete(
            url=api_path,
        )

    def generate_static_credentials(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint retrieves the previous and current LDAP password for
        the associated account (or rotate if required)

        :param name: Specifies the name of the static role to request credentials from.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/static-cred/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def rotate_static_credentials(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint rotates the password of an existing static role.

        :param name: Specifies the name of the static role to rotate credentials for.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/rotate-role/{name}"
        return self._adapter.post(
            url=api_path,
        )
