from contextlib import asynccontextmanager, contextmanager
from unittest import IsolatedAsyncioTestCase, TestCase

from tests.utils.vaultx_integration_test_case import AsyncVaultxIntegrationTestCase, VaultxIntegrationTestCase
from vaultx import exceptions


class TestToken(VaultxIntegrationTestCase, TestCase):
    # would rather these be pytest fixtures
    @contextmanager
    def prep_policy(self, name):  # type: ignore
        try:
            yield name, self.prep_policy(name)  # type: ignore
        finally:
            self.client.sys.delete_policy(name)

    @contextmanager
    def prep_role(self, name, policies=None):
        role = self.client.auth.token.create_or_update_role(name, allowed_policies=policies)
        assert role.status == 204
        try:
            yield name, role, policies
        finally:
            self.client.auth.token.delete_role(name)

    @contextmanager
    def test_policy(self):
        with self.prep_policy(["testpolicy"]) as p:  # type: ignore
            yield p

    @contextmanager
    def test_role(self):
        with self.test_policy() as p, self.prep_role(name="testrole", policies=p[0]) as r:
            yield r

    def test_auth_token_manipulation(self):
        result = self.client.auth.token.create(ttl="1h", renewable=True)
        assert result["auth"]["client_token"]

        lookup = self.client.auth.token.lookup(result["auth"]["client_token"])
        assert result["auth"]["client_token"] == lookup["data"]["id"]

        renew = self.client.auth.token.renew(lookup["data"]["id"])
        assert result["auth"]["client_token"] == renew["auth"]["client_token"]

        self.client.auth.token.revoke(lookup["data"]["id"])

        try:
            self.client.auth.token.lookup(result["auth"]["client_token"])
            raise AssertionError()
        except exceptions.HTTPError as e:
            if e.status_code in {400, 403, 404}:
                assert True

    def test_self_auth_token_manipulation(self):
        result = self.client.auth.token.create(ttl="1h", renewable=True)
        assert result["auth"]["client_token"]
        self.client.token = result["auth"]["client_token"]

        lookup = self.client.auth.token.lookup_self()
        assert result["auth"]["client_token"] == lookup["data"]["id"]

        renew = self.client.auth.token.renew_self()
        assert result["auth"]["client_token"] == renew["auth"]["client_token"]

        self.client.auth.token.revoke_self()

        try:
            self.client.auth.token.lookup(result["auth"]["client_token"])
            raise AssertionError()
        except exceptions.HTTPError as e:
            if e.status_code in {400, 403, 404}:
                assert True

    def test_auth_orphaned_token_manipulation(self):
        result = self.client.auth.token.create_orphan(ttl="1h", renewable=True)
        assert result["auth"]["client_token"]

        lookup = self.client.auth.token.lookup(result["auth"]["client_token"])
        assert result["auth"]["client_token"] == lookup["data"]["id"]

        renew = self.client.auth.token.renew(lookup["data"]["id"])
        assert result["auth"]["client_token"] == renew["auth"]["client_token"]

        self.client.auth.token.revoke(lookup["data"]["id"])

        try:
            self.client.auth.token.lookup(result["auth"]["client_token"])
            raise AssertionError()
        except exceptions.HTTPError as e:
            if e.status_code in {400, 403, 404}:
                assert True

    def test_token_accessor(self):
        # Create token, check accessor is provided
        result = self.client.auth.token.create(ttl="1h")
        token_accessor = result["auth"].get("accessor", None)
        assert token_accessor

        # Look up token by accessor, make sure token is excluded from results
        lookup = self.client.auth.token.lookup_accessor(token_accessor)
        assert lookup["data"]["accessor"] == token_accessor
        assert not lookup["data"]["id"]

        # Revoke token using the accessor
        self.client.auth.token.revoke_accessor(token_accessor)

        # Look up by accessor should fail
        with self.assertRaises(exceptions.HTTPError):
            self.client.auth.token.lookup_accessor(token_accessor)

        # # As should regular lookup
        # with self.assertRaises(exceptions.Forbidden):
        #     self.client.auth.token.lookup(result["auth"]["client_token"])

    def test_create_token_explicit_max_ttl(self):

        token = self.client.auth.token.create(ttl="30m", explicit_max_ttl="5m")

        assert token["auth"]["client_token"]

        assert token["auth"]["lease_duration"] == 300

        # Validate token
        lookup = self.client.auth.token.lookup(token["auth"]["client_token"])
        assert token["auth"]["client_token"] == lookup["data"]["id"]

    def test_create_token_max_ttl(self):

        token = self.client.auth.token.create(ttl="5m")

        assert token["auth"]["client_token"]

        assert token["auth"]["lease_duration"] == 300

        # Validate token
        lookup = self.client.auth.token.lookup(token["auth"]["client_token"])
        assert token["auth"]["client_token"] == lookup["data"]["id"]

    def test_create_token_periodic(self):

        token = self.client.auth.token.create(period="30m")

        assert token["auth"]["client_token"]

        assert token["auth"]["lease_duration"] == 1800

        # Validate token
        lookup = self.client.auth.token.lookup(token["auth"]["client_token"])
        assert token["auth"]["client_token"] == lookup["data"]["id"]
        assert lookup["data"]["period"] == 1800

    def test_create_wrapped_token_periodic(self):

        response = self.client.auth.token.create(period="30m", wrap_ttl="15m")

        assert "wrap_info" in response, repr(response)
        assert response["wrap_info"] is not None, repr(response)
        assert response["auth"] is None, repr(response)
        assert response["wrap_info"]["ttl"] == 900
        assert "token" in response["wrap_info"]

        # unwrap
        token = self.client.sys.unwrap(token=response["wrap_info"]["token"])

        assert token["auth"]["client_token"]
        assert token["auth"]["lease_duration"] == 1800

        # Validate token
        lookup = self.client.auth.token.lookup(token["auth"]["client_token"])
        assert token["auth"]["client_token"] == lookup["data"]["id"]
        assert lookup["data"]["period"] == 1800

    def test_token_roles(self):
        # No roles, list_token_roles == None
        with self.assertRaises(exceptions.HTTPError):
            self.client.auth.token.list_roles()

        try:
            # Create token role
            assert self.client.auth.token.create_or_update_role("testrole").status == 204

            # List token roles
            during = self.client.auth.token.list_roles()["data"]["keys"]
            assert len(during) == 1
            assert during[0] == "testrole"

        finally:
            # Delete token role
            self.client.auth.token.delete_role("testrole")

        # No roles, list_token_roles == None
        with self.assertRaises(exceptions.HTTPError):
            self.client.auth.token.list_roles()

    def test_create_token_w_role(self):
        with self.test_role() as test_role:
            role_name, _, policies = test_role
            expected_policies = ["default"] + policies  # type: ignore

            # Create token against role
            token = self.client.auth.token.create(ttl="1h", role_name=role_name)
            assert token["auth"]["client_token"]
            assert token["auth"]["policies"] == expected_policies

    def test_create_wrapped_token_w_role(self):
        with self.test_role() as test_role:
            role_name, _, policies = test_role
            expected_policies = ["default"] + policies  # type: ignore

            # Create token against role
            response = self.client.auth.token.create(ttl="1h", role_name=role_name, wrap_ttl="15m")

            assert "wrap_info" in response, repr(response)
            assert response["wrap_info"] is not None, repr(response)
            assert response["auth"] is None, repr(response)
            assert response["wrap_info"]["ttl"] == 900
            assert "token" in response["wrap_info"]

            # unwrap
            token = self.client.sys.unwrap(token=response["wrap_info"]["token"])
            assert token["auth"]["client_token"]
            assert token["auth"]["policies"] == expected_policies


class TestAsyncToken(AsyncVaultxIntegrationTestCase, IsolatedAsyncioTestCase):
    # would rather these be pytest fixtures
    @asynccontextmanager
    async def prep_policy(self, name):  # type: ignore
        try:
            yield name, self.prep_policy(name)  # type: ignore
        finally:
            await self.client.sys.delete_policy(name)

    @asynccontextmanager
    async def prep_role(self, name, policies=None):
        role = await self.client.auth.token.create_or_update_role(name, allowed_policies=policies)
        assert role.status == 204
        try:
            yield name, role, policies
        finally:
            await self.client.auth.token.delete_role(name)

    @asynccontextmanager
    async def test_policy(self):
        async with self.prep_policy(["testpolicy"]) as p:  # type: ignore
            yield p

    @asynccontextmanager
    async def test_role(self):
        async with self.test_policy() as p, self.prep_role(name="testrole", policies=p[0]) as r:
            yield r

    async def test_auth_token_manipulation(self):
        result = await self.client.auth.token.create(ttl="1h", renewable=True)
        assert result["auth"]["client_token"]

        lookup = await self.client.auth.token.lookup(result["auth"]["client_token"])
        assert result["auth"]["client_token"] == lookup["data"]["id"]

        renew = await self.client.auth.token.renew(lookup["data"]["id"])
        assert result["auth"]["client_token"] == renew["auth"]["client_token"]

        await self.client.auth.token.revoke(lookup["data"]["id"])

        try:
            await self.client.auth.token.lookup(result["auth"]["client_token"])
            raise AssertionError()
        except exceptions.HTTPError as e:
            if e.status_code in {400, 403, 404}:
                assert True

    async def test_self_auth_token_manipulation(self):
        result = await self.client.auth.token.create(ttl="1h", renewable=True)
        assert result["auth"]["client_token"]
        self.client.token = result["auth"]["client_token"]

        lookup = await self.client.auth.token.lookup_self()
        assert result["auth"]["client_token"] == lookup["data"]["id"]

        renew = await self.client.auth.token.renew_self()
        assert result["auth"]["client_token"] == renew["auth"]["client_token"]

        await self.client.auth.token.revoke_self()

        try:
            await self.client.auth.token.lookup(result["auth"]["client_token"])
            raise AssertionError()
        except exceptions.HTTPError as e:
            if e.status_code in {400, 403, 404}:
                assert True

    async def test_auth_orphaned_token_manipulation(self):
        result = await self.client.auth.token.create_orphan(ttl="1h", renewable=True)
        assert result["auth"]["client_token"]

        lookup = await self.client.auth.token.lookup(result["auth"]["client_token"])
        assert result["auth"]["client_token"] == lookup["data"]["id"]

        renew = await self.client.auth.token.renew(lookup["data"]["id"])
        assert result["auth"]["client_token"] == renew["auth"]["client_token"]

        await self.client.auth.token.revoke(lookup["data"]["id"])

        try:
            await self.client.auth.token.lookup(result["auth"]["client_token"])
            raise AssertionError()
        except exceptions.HTTPError as e:
            if e.status_code in {400, 403, 404}:
                assert True

    async def test_token_accessor(self):
        # Create token, check accessor is provided
        result = await self.client.auth.token.create(ttl="1h")
        token_accessor = result["auth"].get("accessor", None)
        assert token_accessor

        # Look up token by accessor, make sure token is excluded from results
        lookup = await self.client.auth.token.lookup_accessor(token_accessor)
        assert lookup["data"]["accessor"] == token_accessor
        assert not lookup["data"]["id"]

        # Revoke token using the accessor
        await self.client.auth.token.revoke_accessor(token_accessor)

        # Look up by accessor should fail
        with self.assertRaises(exceptions.HTTPError):
            await self.client.auth.token.lookup_accessor(token_accessor)

        # # As should regular lookup
        # with self.assertRaises(exceptions.Forbidden):
        #     self.client.auth.token.lookup(result["auth"]["client_token"])

    async def test_create_token_explicit_max_ttl(self):

        token = await self.client.auth.token.create(ttl="30m", explicit_max_ttl="5m")

        assert token["auth"]["client_token"]

        assert token["auth"]["lease_duration"] == 300

        # Validate token
        lookup = await self.client.auth.token.lookup(token["auth"]["client_token"])
        assert token["auth"]["client_token"] == lookup["data"]["id"]

    async def test_create_token_max_ttl(self):

        token = await self.client.auth.token.create(ttl="5m")

        assert token["auth"]["client_token"]

        assert token["auth"]["lease_duration"] == 300

        # Validate token
        lookup = await self.client.auth.token.lookup(token["auth"]["client_token"])
        assert token["auth"]["client_token"] == lookup["data"]["id"]

    async def test_create_token_periodic(self):

        token = await self.client.auth.token.create(period="30m")

        assert token["auth"]["client_token"]

        assert token["auth"]["lease_duration"] == 1800

        # Validate token
        lookup = await self.client.auth.token.lookup(token["auth"]["client_token"])
        assert token["auth"]["client_token"] == lookup["data"]["id"]
        assert lookup["data"]["period"] == 1800

    async def test_create_wrapped_token_periodic(self):

        response = await self.client.auth.token.create(period="30m", wrap_ttl="15m")

        assert "wrap_info" in response, repr(response)
        assert response["wrap_info"] is not None, repr(response)
        assert response["auth"] is None, repr(response)
        assert response["wrap_info"]["ttl"] == 900
        assert "token" in response["wrap_info"]

        # unwrap
        token = await self.client.sys.unwrap(token=response["wrap_info"]["token"])

        assert token["auth"]["client_token"]
        assert token["auth"]["lease_duration"] == 1800

        # Validate token
        lookup = await self.client.auth.token.lookup(token["auth"]["client_token"])
        assert token["auth"]["client_token"] == lookup["data"]["id"]
        assert lookup["data"]["period"] == 1800

    async def test_token_roles(self):
        # No roles, list_token_roles == None
        with self.assertRaises(exceptions.HTTPError):
            await self.client.auth.token.list_roles()

        try:
            # Create token role
            assert (await self.client.auth.token.create_or_update_role("testrole")).status == 204

            # List token roles
            during = (await self.client.auth.token.list_roles())["data"]["keys"]
            assert len(during) == 1
            assert during[0] == "testrole"

        finally:
            # Delete token role
            await self.client.auth.token.delete_role("testrole")

        # No roles, list_token_roles == None
        with self.assertRaises(exceptions.HTTPError):
            await self.client.auth.token.list_roles()

    async def test_create_token_w_role(self):
        async with self.test_role() as test_role:
            role_name, _, policies = test_role
            expected_policies = ["default"] + policies  # type: ignore

            # Create token against role
            token = await self.client.auth.token.create(ttl="1h", role_name=role_name)
            assert token["auth"]["client_token"]
            assert token["auth"]["policies"] == expected_policies

    async def test_create_wrapped_token_w_role(self):
        async with self.test_role() as test_role:
            role_name, _, policies = test_role
            expected_policies = ["default"] + policies  # type: ignore

            # Create token against role
            response = await self.client.auth.token.create(ttl="1h", role_name=role_name, wrap_ttl="15m")

            assert "wrap_info" in response, repr(response)
            assert response["wrap_info"] is not None, repr(response)
            assert response["auth"] is None, repr(response)
            assert response["wrap_info"]["ttl"] == 900
            assert "token" in response["wrap_info"]

            # unwrap
            token = await self.client.sys.unwrap(token=response["wrap_info"]["token"])
            assert token["auth"]["client_token"]
            assert token["auth"]["policies"] == expected_policies
