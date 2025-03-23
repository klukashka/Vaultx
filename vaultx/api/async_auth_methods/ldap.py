from typing import Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase
from vaultx.exceptions import VaultxError


DEFAULT_MOUNT_POINT = "ldap"


class Ldap(AsyncVaultApiBase):
    """
    LDAP Auth Method (API).

    Reference: https://www.vaultproject.io/api/auth/ldap/index.html
    """

    async def configure(
        self,
        userdn: Optional[str] = None,
        groupdn: Optional[str] = None,
        url: Optional[str] = None,
        case_sensitive_names: Optional[bool] = None,
        starttls: Optional[bool] = None,
        tls_min_version: Optional[str] = None,
        tls_max_version: Optional[str] = None,
        insecure_tls: Optional[bool] = None,
        certificate: Optional[str] = None,
        binddn: Optional[str] = None,
        bindpass: Optional[str] = None,
        userattr: Optional[str] = None,
        discoverdn: Optional[bool] = None,
        deny_null_bind: bool = True,
        upndomain: Optional[str] = None,
        groupfilter: Optional[str] = None,
        groupattr: Optional[str] = None,
        use_token_groups: Optional[bool] = None,
        token_ttl: Optional[str] = None,
        token_max_ttl: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        *,
        anonymous_group_search: Optional[bool] = None,
        client_tls_cert: Optional[str] = None,
        client_tls_key: Optional[str] = None,
        connection_timeout: Optional[int] = None,
        dereference_aliases: Optional[str] = None,
        max_page_size: Optional[int] = None,
        request_timeout: Optional[str] = None,
        token_bound_cidrs: Optional[list[str]] = None,
        token_explicit_max_ttl: Optional[str] = None,
        token_no_default_policy: Optional[bool] = None,
        token_num_uses: Optional[int] = None,
        token_period: Optional[str] = None,
        token_policies: Optional[list[str]] = None,
        token_type: Optional[str] = None,
        userfilter: Optional[str] = None,
        username_as_alias: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Configure the LDAP auth method.

        Supported methods:
            POST: /auth/{mount_point}/config. Produces: 204 (empty body)

        :param anonymous_group_search: Use anonymous binds when performing LDAP group searches (note: even when true,
            the initial credentials will still be used for the initial connection test).
        :param client_tls_cert: Client certificate to provide to the LDAP server, must be x509 PEM encoded.
        :param client_tls_key: Client certificate key to provide to the LDAP server, must be x509 PEM encoded.
        :param connection_timeout: Timeout, in seconds, when attempting to connect to the LDAP server before trying the
            next URL in the configuration.
        :param dereference_aliases: When aliases should be dereferenced on search operations.
            Accepted values are 'never', 'finding', 'searching', 'always'.
        :param max_page_size: If set to a value greater than 0, the LDAP backend will use the LDAP server's paged search
            control to request pages of up to the given size.
        :param request_timeout: Timeout, in seconds, for the connection when making requests against the server before
            returning back an error.
        :param token_bound_cidrs: List of CIDR blocks; if set, specifies blocks of IP addresses which can authenticate
            successfully, and ties the resulting token to these blocks as well.
        :param token_explicit_max_ttl: If set, will encode an explicit max TTL onto the token. This is a hard cap even
            if token_ttl and token_max_ttl would otherwise allow a renewal.
        :param token_no_default_policy: If set, the default policy will not be set on generated tokens; otherwise it
            will be added to the policies set in token_policies.
        :param token_num_uses: The maximum number of times a generated token may be used (within its lifetime); 0 means
            unlimited.
        :param token_period: The maximum allowed period value when a periodic token is requested from this role.
        :param token_policies: List of token policies to encode onto generated tokens.
        :param token_type: The type of token that should be generated.
        :param userfilter: An optional LDAP user search filter.
        :param username_as_alias: If set to true, forces the auth method to use the username passed by the user as the
            alias name.
        :param userdn: Base DN under which to perform user search. Example: ou=Users,dc=example,dc=com
        :param groupdn: LDAP search base to use for group membership search. This can be the root containing either
            groups or users. Example: ou=Groups,dc=example,dc=com
        :param url: The LDAP server to connect to. Examples: ldap://ldap.myorg.com, ldaps://ldap.myorg.com:636.
            Multiple URLs can be specified with commas, e.g. ldap://ldap.myorg.com,ldap://ldap2.myorg.com; these will be
            tried in-order.
        :param case_sensitive_names: If set, user and group names assigned to policies within the backend will be case
            sensitive. Otherwise, names will be normalized to lower case. Case will still be preserved when sending the
            username to the LDAP server at login time; this is only for matching local user/group definitions.
        :param starttls: If true, issues a StartTLS command after establishing an unencrypted connection.
        :param tls_min_version: Minimum TLS version to use. Accepted values are tls10, tls11 or tls12.
        :param tls_max_version: Maximum TLS version to use. Accepted values are tls10, tls11 or tls12.
        :param insecure_tls: If true, skips LDAP server SSL certificate verification - insecure, use with caution!
        :param certificate: CA certificate to use when verifying LDAP server certificate, must be x509 PEM encoded.
        :param binddn: Distinguished name of object to bind when performing user search. Example:
            cn=vault,ou=Users,dc=example,dc=com
        :param bindpass:  Password to use along with binddn when performing user search.
        :param userattr: Attribute on user attribute object matching the username passed when authenticating. Examples:
            sAMAccountName, cn, uid
        :param discoverdn: Use anonymous bind to discover the bind DN of a user.
        :param deny_null_bind: This option prevents users from bypassing authentication
            when providing an empty password.
        :param upndomain: The userPrincipalDomain used to construct the UPN string for the authenticating user. The
            constructed UPN will appear as [username]@UPNDomain. Example: example.com, which will cause vault to bind as
            username@example.com.
        :param groupfilter: Go template used when constructing the group membership query. The template can access the
            following context variables: [UserDN, Username]. The default is
            `(|(memberUid={{.Username}})(member={{.UserDN}})(uniqueMember={{.UserDN}}))`, which is compatible with
            several common directory schemas. To support nested group resolution for Active Directory,
            instead use the following query: (&(objectClass=group)(member:1.2.840.113556.1.4.1941:={{.UserDN}})).
        :param groupattr: LDAP attribute to follow on objects returned by groupfilter in order to enumerate user group
            membership. Examples: for groupfilter queries returning group objects, use: cn. For queries returning user
            objects, use: memberOf. The default is cn.
        :param use_token_groups: If true, groups are resolved through Active Directory tokens. This may speed up nested
            group membership resolution in large directories.
        :param token_ttl: The incremental lifetime for generated tokens.
        :param token_max_ttl: The maximum lifetime for generated tokens.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the configure request.
        """
        params = utils.remove_nones(
            {
                "url": url,
                "anonymous_group_search": anonymous_group_search,
                "binddn": binddn,
                "bindpass": bindpass,
                "case_sensitive_names": case_sensitive_names,
                "certificate": certificate,
                "client_tls_cert": client_tls_cert,
                "client_tls_key": client_tls_key,
                "connection_timeout": connection_timeout,
                "deny_null_bind": deny_null_bind,
                "dereference_aliases": dereference_aliases,
                "discoverdn": discoverdn,
                "groupattr": groupattr,
                "groupdn": groupdn,
                "groupfilter": groupfilter,
                "insecure_tls": insecure_tls,
                "max_page_size": max_page_size,
                "request_timeout": request_timeout,
                "starttls": starttls,
                "tls_max_version": tls_max_version,
                "tls_min_version": tls_min_version,
                "token_bound_cidrs": token_bound_cidrs,
                "token_explicit_max_ttl": token_explicit_max_ttl,
                "token_max_ttl": token_max_ttl,
                "token_no_default_policy": token_no_default_policy,
                "token_num_uses": token_num_uses,
                "token_period": token_period,
                "token_policies": token_policies,
                "token_ttl": token_ttl,
                "token_type": token_type,
                "upndomain": upndomain,
                "use_token_groups": use_token_groups,
                "userattr": userattr,
                "userdn": userdn,
                "userfilter": userfilter,
                "username_as_alias": username_as_alias,
            }
        )

        api_path = f"/v1/auth/{mount_point}/config"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_configuration(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Retrieve the LDAP configuration for the auth method.

        Supported methods:
            GET: /auth/{mount_point}/config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_configuration request.
        """
        api_path = f"/v1/auth/{mount_point}/config"
        return await self._adapter.get(
            url=api_path,
        )

    async def create_or_update_group(
        self, name: str, policies: Optional[list[str]] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Create or update LDAP group policies.

        Supported methods:
            POST: /auth/{mount_point}/groups/{name}. Produces: 204 (empty body)


        :param name: The name of the LDAP group
        :param policies: List of policies associated with the group. This parameter is transformed to a comma-delimited
            string before being passed to Vault.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the create_or_update_group request.
        """
        if policies is not None and not isinstance(policies, list):
            raise VaultxError(f'"policies" argument must be an instance of list or None, "{type(policies)}" provided.')

        params = {}
        if policies is not None:
            params["policies"] = ",".join(policies)
        api_path = f"/v1/auth/{mount_point}/groups/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def list_groups(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List existing LDAP existing groups that have been created in this auth method.

        Supported methods:
            LIST: /auth/{mount_point}/groups. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the list_groups request.
        """
        api_path = f"/v1/auth/{mount_point}/groups"
        return await self._adapter.list(
            url=api_path,
        )

    async def read_group(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read policies associated with an LDAP group.

        Supported methods:
            GET: /auth/{mount_point}/groups/{name}. Produces: 200 application/json

        :param name: The name of the LDAP group
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_group request.
        """
        params = {
            "name": name,
        }
        api_path = f"/v1/auth/{mount_point}/groups/{name}"
        return await self._adapter.get(
            url=api_path,
            json=params,
        )

    async def delete_group(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an LDAP group and policy association.

        Supported methods:
            DELETE: /auth/{mount_point}/groups/{name}. Produces: 204 (empty body)


        :param name: The name of the LDAP group
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the delete_group request.
        """
        api_path = f"/v1/auth/{mount_point}/groups/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def create_or_update_user(
        self,
        username: str,
        policies: Optional[list[str]] = None,
        groups: Optional[list[str]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update LDAP users policies and group associations.

        Supported methods:
            POST: /auth/{mount_point}/users/{username}. Produces: 204 (empty body)

        :param username: The username of the LDAP user
        :param policies: List of policies associated with the user. This parameter is transformed to a comma-delimited
            string before being passed to Vault.
        :param groups: List of groups associated with the user. This parameter is transformed to a comma-delimited
            string before being passed to Vault.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the create_or_update_user request.
        """
        list_required_params = {
            "policies": policies,
            "groups": groups,
        }
        for param_name, param_arg in list_required_params.items():
            if param_arg is not None and not isinstance(param_arg, list):
                raise VaultxError(
                    f'"{param_name}" argument must be an instance of list or None, "{type(param_arg)}" provided.'
                )

        params = {}
        if policies is not None:
            params["policies"] = ",".join(policies)
        if groups is not None:
            params["groups"] = ",".join(groups)
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def list_users(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List existing users in the method.

        Supported methods:
            LIST: /auth/{mount_point}/users. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the list_users request.
        """
        api_path = f"/v1/auth/{mount_point}/users"
        return await self._adapter.list(
            url=api_path,
        )

    async def read_user(self, username: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read policies associated with an LDAP user.

        Supported methods:
            GET: /auth/{mount_point}/users/{username}. Produces: 200 application/json

        :param username: The username of the LDAP user
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the read_user request.
        """
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return await self._adapter.get(
            url=api_path,
        )

    async def delete_user(self, username: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an LDAP user and policy association.

        Supported methods:
            DELETE: /auth/{mount_point}/users/{username}. Produces: 204 (empty body)

        :param username: The username of the LDAP user
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the delete_user request.
        """
        api_path = f"/v1/auth/{mount_point}/users/{username}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def login(
        self, username: str, password: str, use_token: bool = True, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Log in with LDAP credentials.

        Supported methods:
            POST: /auth/{mount_point}/login/{username}. Produces: 200 application/json

        :param username: The username of the LDAP user
        :param password: The password for the LDAP user
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.Adapter` instance under the _adapter Client attribute.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the login_with_user request.
        """
        params = {
            "password": password,
        }
        api_path = f"/v1/auth/{mount_point}/login/{username}"
        return await self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )
