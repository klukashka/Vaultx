import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_auth_methods.oidc import Oidc as AsyncOidc
from vaultx.api.auth_methods.oidc import Oidc


class TestOIDC(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.oidc = Oidc(self.mock_adapter)

    def test_create_role(self):
        # Test successful role creation with default parameters
        self.mock_adapter.post.return_value = Response(204)
        result = self.oidc.create_role(
            name="test_role",
            user_claim="sub",
            allowed_redirect_uris=["https://example.com/callback"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/auth/{self.oidc.DEFAULT_PATH}/role/test_role",
            json={
                "name": "test_role",
                "role_type": "oidc",
                "user_claim": "sub",
                "allowed_redirect_uris": ["https://example.com/callback"],
                "bound_claims_type": "string",
                "verbose_oidc_logging": False,
            },
        )

        # Test with all optional parameters
        self.mock_adapter.post.return_value = Response(204)
        result = self.oidc.create_role(
            name="test_role",
            user_claim="sub",
            allowed_redirect_uris=["https://example.com/callback"],
            role_type="oidc",
            bound_audiences=["aud1", "aud2"],
            clock_skew_leeway=10,
            expiration_leeway=10,
            not_before_leeway=10,
            bound_subject="sub123",
            bound_claims={"claim1": "value1"},
            groups_claim="groups",
            claim_mappings={"claim2": "metadata_field"},
            oidc_scopes=["openid", "profile"],
            bound_claims_type="glob",
            verbose_oidc_logging=True,
            token_ttl="1h",
            token_max_ttl="2h",
            token_policies=["policy1", "policy2"],
            token_bound_cidrs=["192.168.1.0/24"],
            token_explicit_max_ttl="3h",
            token_no_default_policy=True,
            token_num_uses="5",
            token_period="4h",
            token_type="service",
            user_claim_json_pointer=True,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url=f"/v1/auth/{self.oidc.DEFAULT_PATH}/role/test_role",
            json={
                "name": "test_role",
                "user_claim": "sub",
                "allowed_redirect_uris": ["https://example.com/callback"],
                "role_type": "oidc",
                "bound_audiences": ["aud1", "aud2"],
                "clock_skew_leeway": 10,
                "expiration_leeway": 10,
                "not_before_leeway": 10,
                "bound_subject": "sub123",
                "bound_claims": {"claim1": "value1"},
                "groups_claim": "groups",
                "claim_mappings": {"claim2": "metadata_field"},
                "oidc_scopes": ["openid", "profile"],
                "bound_claims_type": "glob",
                "verbose_oidc_logging": True,
                "token_ttl": "1h",
                "token_max_ttl": "2h",
                "token_policies": ["policy1", "policy2"],
                "token_bound_cidrs": ["192.168.1.0/24"],
                "token_explicit_max_ttl": "3h",
                "token_no_default_policy": True,
                "token_num_uses": "5",
                "token_period": "4h",
                "token_type": "service",
                "user_claim_json_pointer": True,
            },
        )

    def test_create_role_with_custom_path(self):
        # Test role creation with a custom mount path
        custom_path = "custom-oidc"
        self.mock_adapter.post.return_value = Response(204)
        result = self.oidc.create_role(
            name="test_role",
            user_claim="sub",
            allowed_redirect_uris=["https://example.com/callback"],
            path=custom_path,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/auth/{custom_path}/role/test_role",
            json={
                "name": "test_role",
                "user_claim": "sub",
                "allowed_redirect_uris": ["https://example.com/callback"],
                "role_type": "oidc",
                "bound_claims_type": "string",
                "verbose_oidc_logging": False,
            },
        )


class TestAsyncOIDC(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.oidc = AsyncOidc(self.mock_adapter)

    async def test_create_role(self):
        # Test successful role creation with default parameters
        self.mock_adapter.post.return_value = Response(204)
        result = await self.oidc.create_role(
            name="test_role",
            user_claim="sub",
            allowed_redirect_uris=["https://example.com/callback"],
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/auth/{self.oidc.DEFAULT_PATH}/role/test_role",
            json={
                "name": "test_role",
                "user_claim": "sub",
                "allowed_redirect_uris": ["https://example.com/callback"],
                "role_type": "oidc",
                "bound_claims_type": "string",
                "verbose_oidc_logging": False,
            },
        )

        # Test with all optional parameters
        self.mock_adapter.post.return_value = Response(204)
        result = await self.oidc.create_role(
            name="test_role",
            user_claim="sub",
            allowed_redirect_uris=["https://example.com/callback"],
            role_type="oidc",
            bound_audiences=["aud1", "aud2"],
            clock_skew_leeway=10,
            expiration_leeway=10,
            not_before_leeway=10,
            bound_subject="sub123",
            bound_claims={"claim1": "value1"},
            groups_claim="groups",
            claim_mappings={"claim2": "metadata_field"},
            oidc_scopes=["openid", "profile"],
            bound_claims_type="glob",
            verbose_oidc_logging=True,
            token_ttl="1h",
            token_max_ttl="2h",
            token_policies=["policy1", "policy2"],
            token_bound_cidrs=["192.168.1.0/24"],
            token_explicit_max_ttl="3h",
            token_no_default_policy=True,
            token_num_uses="5",
            token_period="4h",
            token_type="service",
            user_claim_json_pointer=True,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_with(
            url=f"/v1/auth/{self.oidc.DEFAULT_PATH}/role/test_role",
            json={
                "name": "test_role",
                "user_claim": "sub",
                "allowed_redirect_uris": ["https://example.com/callback"],
                "role_type": "oidc",
                "bound_audiences": ["aud1", "aud2"],
                "clock_skew_leeway": 10,
                "expiration_leeway": 10,
                "not_before_leeway": 10,
                "bound_subject": "sub123",
                "bound_claims": {"claim1": "value1"},
                "groups_claim": "groups",
                "claim_mappings": {"claim2": "metadata_field"},
                "oidc_scopes": ["openid", "profile"],
                "bound_claims_type": "glob",
                "verbose_oidc_logging": True,
                "token_ttl": "1h",
                "token_max_ttl": "2h",
                "token_policies": ["policy1", "policy2"],
                "token_bound_cidrs": ["192.168.1.0/24"],
                "token_explicit_max_ttl": "3h",
                "token_no_default_policy": True,
                "token_num_uses": "5",
                "token_period": "4h",
                "token_type": "service",
                "user_claim_json_pointer": True,
            },
        )

    async def test_create_role_with_custom_path(self):
        # Test role creation with a custom mount path
        custom_path = "custom-oidc"
        self.mock_adapter.post.return_value = Response(204)
        result = await self.oidc.create_role(
            name="test_role",
            user_claim="sub",
            allowed_redirect_uris=["https://example.com/callback"],
            path=custom_path,
        )
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/auth/{custom_path}/role/test_role",
            json={
                "name": "test_role",
                "user_claim": "sub",
                "allowed_redirect_uris": ["https://example.com/callback"],
                "role_type": "oidc",
                "bound_claims_type": "string",
                "verbose_oidc_logging": False,
            },
        )
