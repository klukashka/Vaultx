from typing import Optional, Union

from vaultx.adapters import VaultxResponse
from vaultx.api.async_auth_methods.jwt import Jwt


class Oidc(Jwt):
    """
    OIDC auth method which can be used to authenticate with Vault using OIDC.

    The OIDC method allows authentication via a configured OIDC provider using the user's web browser.
    This method may be initiated from the Vault UI or the command line. Alternatively, a JWT can be provided directly.
    The JWT is cryptographically verified using locally-provided keys, or, if configured, an OIDC Discovery service can
    be used to fetch the appropriate keys. The choice of method is configured per role.

    Note: this class is duplicative of the JWT class (as both JWT and OIDC share the same family of Vault API routes).

    Reference: https://www.vaultproject.io/api/auth/jwt
    """

    DEFAULT_PATH: str = "oidc"

    async def create_role(
        self,
        name: str,
        user_claim: str,
        allowed_redirect_uris: list[str],
        role_type: str = "oidc",
        bound_audiences: Optional[list[str]] = None,
        clock_skew_leeway: Optional[int] = None,
        expiration_leeway: Optional[int] = None,
        not_before_leeway: Optional[int] = None,
        bound_subject: Optional[str] = None,
        bound_claims: Optional[dict] = None,
        groups_claim: Optional[str] = None,
        claim_mappings: Optional[dict] = None,
        oidc_scopes: Optional[list[str]] = None,
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
        Register a role in the OIDC method.

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
            is configured with ``user_claim_json_pointer``. If set to ``True``, ``user_claim`` supports JSON pointer
            syntax for referencing a claim. The claim value must be a string.
        :param clock_skew_leeway: Only applicable with "jwt" roles.
        :param expiration_leeway: Only applicable with "jwt" roles.
        :param not_before_leeway: Only applicable with "jwt" roles.
        :param bound_subject:  If set, requires that the sub claim matches this value.
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
        :param allowed_redirect_uris: The list of allowed values for redirect_uri during OIDC logins.
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
        :param path: The "path" the method/backend was mounted on.
        :param user_claim_json_pointer: Specifies if the ``user_claim`` value uses JSON pointer syntax for
            referencing claims. By default, the ``user_claim`` value will not use JSON pointer.
        :return: The response of the create_role request.
        """

        return await super().create_role(
            name=name,
            user_claim=user_claim,
            allowed_redirect_uris=allowed_redirect_uris,
            role_type=role_type,
            bound_audiences=bound_audiences,
            clock_skew_leeway=clock_skew_leeway,
            expiration_leeway=expiration_leeway,
            not_before_leeway=not_before_leeway,
            bound_subject=bound_subject,
            bound_claims=bound_claims,
            groups_claim=groups_claim,
            claim_mappings=claim_mappings,
            oidc_scopes=oidc_scopes,
            bound_claims_type=bound_claims_type,
            verbose_oidc_logging=verbose_oidc_logging,
            token_ttl=token_ttl,
            token_max_ttl=token_max_ttl,
            token_policies=token_policies,
            token_bound_cidrs=token_bound_cidrs,
            token_explicit_max_ttl=token_explicit_max_ttl,
            token_no_default_policy=token_no_default_policy,
            token_num_uses=token_num_uses,
            token_period=token_period,
            token_type=token_type,
            path=path,
            user_claim_json_pointer=user_claim_json_pointer,
        )
