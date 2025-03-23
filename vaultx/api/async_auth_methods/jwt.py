from typing import Optional, Union

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


class Jwt(AsyncVaultApiBase):
    """
    JWT auth method which can be used to authenticate with Vault by providing a JWT.

    The OIDC method allows authentication via a configured OIDC provider using the user's web browser.
    This method may be initiated from the Vault UI or the command line. Alternatively, a JWT can be provided directly.
    The JWT is cryptographically verified using locally-provided keys, or, if configured, an OIDC Discovery service can
    be used to fetch the appropriate keys. The choice of method is configured per role.

    Reference: https://www.vaultproject.io/api/auth/jwt
    """

    DEFAULT_PATH: str = "jwt"

    def resolve_path(self, path: Optional[str]) -> str:
        """
        Return the class's default path if no explicit path is specified.

        :param path: The "path" the method/backend was mounted on.
        :return: The default path for this auth method if no explicit path is specified.
        """
        return path if path is not None else self.DEFAULT_PATH

    async def configure(
        self,
        oidc_discovery_url: Optional[str] = None,
        oidc_discovery_ca_pem: Optional[str] = None,
        oidc_client_id: Optional[str] = None,
        oidc_client_secret: Optional[str] = None,
        oidc_response_mode: Optional[str] = None,
        oidc_response_types: Optional[str] = None,
        jwks_url: Optional[str] = None,
        jwks_ca_pem: Optional[str] = None,
        jwt_validation_pubkeys: Optional[str] = None,
        bound_issuer: Optional[str] = None,
        jwt_supported_algs: Optional[str] = None,
        default_role: Optional[str] = None,
        provider_config: Optional[dict] = None,
        path: Optional[str] = None,
        namespace_in_state: Optional[bool] = None,
    ) -> VaultxResponse:
        """
        Configure the validation information to be used globally across all roles.

        One (and only one) of oidc_discovery_url and jwt_validation_pubkeys must be set.

        Supported methods:
            POST: /auth/{path}/config.

        :param oidc_discovery_url: The OIDC Discovery URL, without any .well-known component (base path). Cannot be
            used with "jwks_url" or "jwt_validation_pubkeys".
        :param oidc_discovery_ca_pem: The CA certificate or chain of certificates, in PEM format, to use to validate
            connections to the OIDC Discovery URL. If not set, system certificates are used.
        :param oidc_client_id: The OAuth Client ID from the provider for OIDC roles.
        :param oidc_client_secret: The OAuth Client Secret from the provider for OIDC roles.
        :param oidc_response_mode: The response mode to be used in the OAuth2 request. Allowed values are "query" and
            form_post". Defaults to "query".
        :param oidc_response_types: The response types to request. Allowed values are "code" and "id_token". Defaults
            to "code". Note: "id_token" may only be used if "oidc_response_mode" is set to "form_post".
        :param jwks_url: JWKS URL to use to authenticate signatures. Cannot be used with "oidc_discovery_url" or
            "jwt_validation_pubkeys".
        :param jwks_ca_pem: The CA certificate or chain of certificates, in PEM format, to use to validate connections
            to the JWKS URL. If not set, system certificates are used.
        :param jwt_validation_pubkeys: A list of PEM-encoded public keys to use to authenticate signatures locally.
            Cannot be used with "jwks_url" or "oidc_discovery_url".
        :param bound_issuer: in a JWT.
        :param jwt_supported_algs: A list of supported signing algorithms. Defaults to [RS256].
        :param default_role: The default role to use if none is provided during login.
        :param provider_config: TypeError
        :type provider_config: map
        :param path: The "path" the method/backend was mounted on.
        :param namespace_in_state: With this setting, the allowed redirect URL(s) in Vault and on the provider side
            should not contain a namespace query parameter.
        :return: The response of the configure request.
        """
        params = utils.remove_nones(
            {
                "oidc_discovery_url": oidc_discovery_url,
                "oidc_discovery_ca_pem": oidc_discovery_ca_pem,
                "oidc_client_id": oidc_client_id,
                "oidc_client_secret": oidc_client_secret,
                "oidc_response_mode": oidc_response_mode,
                "oidc_response_types": oidc_response_types,
                "jwks_url": jwks_url,
                "jwks_ca_pem": jwks_ca_pem,
                "jwt_validation_pubkeys": jwt_validation_pubkeys,
                "bound_issuer": bound_issuer,
                "jwt_supported_algs": jwt_supported_algs,
                "default_role": default_role,
                "provider_config": provider_config,
                "namespace_in_state": namespace_in_state,
            }
        )
        api_path = f"/v1/auth/{self.resolve_path(path)}/config"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_config(self, path: Optional[str] = None) -> VaultxResponse:
        """
        Read the previously configured config.

        Supported methods:
            GET: /auth/{path}/config.

        :return: The response of the read_config request.
        """
        api_path = f"/v1/auth/{self.resolve_path(path)}/config"
        return await self._adapter.get(
            url=api_path,
        )

    async def create_role(
        self,
        name: str,
        user_claim: str,
        allowed_redirect_uris: list,
        role_type: str = "jwt",
        bound_audiences: Optional[list] = None,
        clock_skew_leeway: Optional[int] = None,
        expiration_leeway: Optional[int] = None,
        not_before_leeway: Optional[int] = None,
        bound_subject: Optional[str] = None,
        bound_claims: Optional[dict] = None,
        groups_claim: Optional[str] = None,
        claim_mappings: Optional[dict] = None,
        oidc_scopes: Optional[list] = None,
        bound_claims_type: str = "string",
        verbose_oidc_logging: bool = False,
        token_ttl: Optional[Union[str, int]] = None,
        token_max_ttl: Optional[Union[str, int]] = None,
        token_policies: Optional[list[str]] = None,
        token_bound_cidrs: Optional[list[str]] = None,
        token_explicit_max_ttl: Optional[Union[str, int]] = None,
        token_no_default_policy: Optional[bool] = None,
        token_num_uses: Optional[str] = None,
        token_period: Optional[Union[str, int]] = None,
        token_type: Optional[str] = None,
        path: Optional[str] = None,
        user_claim_json_pointer: Optional[bool] = None,
    ) -> VaultxResponse:
        """
        Register a role in the JWT method.

        Role types have specific entities that can perform login operations against this endpoint. Constraints
        specific to the role type must be set on the role. These are applied to the authenticated entities
        attempting to log in. At least one of the bound values must be set.

        Supported methods:
            POST: /auth/{path}/role/:name.

        :param name: Name of the role.
        :param role_type: Type of role, either "oidc" or "jwt" (default).
        :param bound_audiences: List of aud claims to match against. Any match is sufficient.
            Required for "jwt" roles, optional for "oidc" roles.
        :param user_claim: The claim to use to uniquely identify the user; this will be used as the name for the
            Identity entity alias created due to a successful login. The interpretation of the user claim
            is configured with ``user_claim_json_pointer``. If set to ``True``, ``user_claim`` supports
            JSON pointer syntax for referencing a claim. The claim value must be a string.
        :param clock_skew_leeway: Only applicable with "jwt" roles.
        :param expiration_leeway: Only applicable with "jwt" roles.
        :param not_before_leeway: Only applicable with "jwt" roles.
        :param bound_subject:  If set, requires that the subclaim matches this value.
        :param bound_claims: If set, a dict of claims (keys) to match against respective claim values (values).
            The expected value may be a single string or a list of strings. The interpretation of the bound claim
            values is configured with bound_claims_type. Keys support JSON pointer syntax for referencing claims.
        :param groups_claim: The claim to use to uniquely identify the set of groups to which the user belongs; this
            will be used as the names for the Identity group aliases created due to a successful login. The claim value
            must be a list of strings. Supports JSON pointer syntax for referencing claims.
        :param claim_mappings: If set, a map of claims (keys) to be copied to specified metadata fields (values). Keys
            support JSON pointer syntax for referencing claims.
        :param oidc_scopes: If set, a list of OIDC scopes to be used with an OIDC role.
            The standard scope "openid" is automatically included and need not be specified.
        :param allowed_redirect_uris: The list of allowed values for redirect_uri
            during OIDC logins.
        :param bound_claims_type: Configures the interpretation of the bound_claims values. If "string" (the default),
            the values will be treated as string literals and must match exactly. If set to "glob", the values will be
            interpreted as globs, with * matching any number of characters.
        :param verbose_oidc_logging: Log received OIDC tokens and claims when debug-level
            logging is active. Not recommended in production since sensitive information may be present
            in OIDC responses.
        :param token_ttl: The incremental lifetime for generated tokens. This current value of this will be referenced
            at renewal time.
        :param token_max_ttl: The maximum lifetime for generated tokens. This current value of this will be referenced
            at renewal time.
        :param token_policies: List of policies to encode onto generated tokens. Depending on the auth method, this
            list may be supplemented by user/group/other values.
        :param token_bound_cidrs:  List of CIDR blocks; if set, specifies blocks of IP addresses which can authenticate
            successfully, and ties the resulting token to these blocks as well.
        :param token_explicit_max_ttl:  If set, will encode an explicit max TTL onto the token. This is a hard cap
            even if token_ttl and token_max_ttl would otherwise allow a renewal.
        :param token_no_default_policy: If set, the default policy will not be set on generated tokens; otherwise it
            will be added to the policies set in token_policies.
        :param token_num_uses: The maximum number of times a generated token may be used (within its lifetime); 0 means
            unlimited. If you require the token to have the ability to create child tokens, you will need to set this
            value to 0.
        :param token_period: The period, if any, to set on the token.
        :param token_type: The type of token that should be generated. Can be service, batch, or default.
        :type token_type: str
        :param path: The "path" the method/backend was mounted on.
        :param user_claim_json_pointer: Specifies if the ``user_claim`` value uses
            JSON pointer syntax for referencing claims. By default, the ``user_claim`` value will not use JSON pointer.
        :return: The response of the create_role request.
        """
        params = utils.remove_nones(
            {
                "name": name,
                "role_type": role_type,
                "bound_audiences": bound_audiences,
                "user_claim": user_claim,
                "clock_skew_leeway": clock_skew_leeway,
                "expiration_leeway": expiration_leeway,
                "not_before_leeway": not_before_leeway,
                "bound_subject": bound_subject,
                "bound_claims": bound_claims,
                "groups_claim": groups_claim,
                "claim_mappings": claim_mappings,
                "oidc_scopes": oidc_scopes,
                "allowed_redirect_uris": allowed_redirect_uris,
                "bound_claims_type": bound_claims_type,
                "verbose_oidc_logging": verbose_oidc_logging,
                "token_ttl": token_ttl,
                "token_max_ttl": token_max_ttl,
                "token_policies": token_policies,
                "token_bound_cidrs": token_bound_cidrs,
                "token_explicit_max_ttl": token_explicit_max_ttl,
                "token_no_default_policy": token_no_default_policy,
                "token_num_uses": token_num_uses,
                "token_period": token_period,
                "token_type": token_type,
                "user_claim_json_pointer": user_claim_json_pointer,
            }
        )
        api_path = f"/v1/auth/{self.resolve_path(path)}/role/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_role(self, name: str, path: Optional[str] = None) -> VaultxResponse:
        """
        Read the previously registered role configuration.

        Supported methods:
            GET: /auth/{path}/role/:name.

        :param name: Name of the role.
        :param path: The "path" the method/backend was mounted on.
        :return: The response of the read_role request.
        """
        api_path = f"/v1/auth/{self.resolve_path(path)}/role/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_roles(self, path: Optional[str] = None) -> VaultxResponse:
        """
        List all the roles that are registered with the plugin.

        Supported methods:
            LIST: /auth/{path}/role.

        :param path: The "path" the method/backend was mounted on.
        :return: The response of the list_roles request.
        """
        api_path = f"/v1/auth/{self.resolve_path(path)}/role"
        return await self._adapter.list(
            url=api_path,
        )

    async def delete_role(self, name: str, path: Optional[str] = None) -> VaultxResponse:
        """
        Delete the previously registered role.

        Supported methods:
            DELETE: /auth/{path}/role/:name.

        :param name: Name of the role.
        :param path: The "path" the method/backend was mounted on.
        :return: The response of the delete_role request.
        """
        api_path = f"/v1/auth/{self.resolve_path(path)}/role/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def oidc_authorization_url_request(
        self, role: str, redirect_uri: str, path: Optional[str] = None
    ) -> VaultxResponse:
        """
        Obtain an authorization URL from Vault to start an OIDC login flow.

        Supported methods:
            POST: /auth/{path}/auth_url.

        :param role: not provided.
        :param redirect_uri: more information.
        :param path: The "path" the method/backend was mounted on.
        :return: The response of the _authorization_url_request request.
        """
        params = {
            "role": role,
            "redirect_uri": redirect_uri,
        }
        api_path = f"/v1/auth/{self.resolve_path(path)}/oidc/auth_url"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def oidc_callback(self, state: str, nonce: str, code: str, path: Optional[str] = None) -> VaultxResponse:
        """
        Exchange an authorization code for an OIDC ID Token.

        The ID token will be further validated against any bound claims, and if valid a Vault token will be returned.

        Supported methods:
            GET: /auth/{path}/callback.

        :param state: Opaque state ID that is part of the Authorization URL and will
            be included in the redirect following successful authentication on the provider.
        :param nonce: Opaque nonce that is part of the Authorization URL and will
            be included in the redirect following successful authentication on the provider.
        :param code: Provider-generated authorization code that Vault will exchange for
            an ID token.
        :param path: The "path" the method/backend was mounted on.
        :return: The response of the _callback request.
        """
        params = {
            "state": state,
            "nonce": nonce,
            "code": code,
        }
        api_path = f"/v1/auth/{self.resolve_path(path)}/oidc/callback?state={state}&nonce={nonce}&code={code}"
        return await self._adapter.get(
            url=api_path,
            json=params,
        )

    async def jwt_login(
        self, role: str, jwt: str, use_token: bool = True, path: Optional[str] = None
    ) -> VaultxResponse:
        """
        Fetch a token.

        This endpoint takes a signed JSON Web Token (JWT) and a role name for some entity.
        It verifies the JWT signature to authenticate that entity and then authorizes the
        entity for the given role.

        Supported methods:
            POST: /auth/{path}/login.

        :param role: not provided.
        :param jwt: Signed JSON Web Token (JWT).
        :param use_token: whether to use a token or not.
        :param path: The "path" the method/backend was mounted on.
        :return: The response of the jwt_login request.
        """
        params = {
            "role": role,
            "jwt": jwt,
        }
        api_path = f"/v1/auth/{self.resolve_path(path)}/login"
        return await self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )
