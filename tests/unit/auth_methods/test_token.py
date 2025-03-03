import unittest
from unittest import mock

import pytest
from httpx import Response

from vaultx.adapters import Adapter
from vaultx.api.async_auth_methods.token import Token as AsyncToken
from vaultx.api.auth_methods.token import Token


class TestToken(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.token = Token(self.mock_adapter)

    def test_create(self):
        self.mock_adapter.post.return_value = {"auth": {"client_token": "test_token"}}
        result = self.token.create(
            id_="test_id",
            policies=["policy1", "policy2"],
            ttl="1h",
        )
        self.assertEqual(result, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.post.assert_called_once()

    def test_create_orphan(self):
        self.mock_adapter.post.return_value = {"auth": {"client_token": "test_token"}}
        result = self.token.create_orphan(
            id_="test_id",
            policies=["policy1", "policy2"],
            ttl="1h",
        )
        self.assertEqual(result, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.post.assert_called_once()

    def test_list_accessors(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["accessor1", "accessor2"]}}
        result = self.token.list_accessors()
        self.assertEqual(result, {"data": {"keys": ["accessor1", "accessor2"]}})
        self.mock_adapter.list.assert_called_once()

    def test_lookup(self):
        self.mock_adapter.post.return_value = {"data": {"id": "test_token"}}
        result = self.token.lookup(token="test_token")
        self.assertEqual(result, {"data": {"id": "test_token"}})
        self.mock_adapter.post.assert_called_once()

    def test_lookup_self(self):
        self.mock_adapter.get.return_value = {"data": {"id": "test_token"}}
        result = self.token.lookup_self()
        self.assertEqual(result, {"data": {"id": "test_token"}})
        self.mock_adapter.get.assert_called_once()

    def test_lookup_accessor(self):
        self.mock_adapter.post.return_value = {"data": {"id": "test_token"}}
        result = self.token.lookup_accessor(accessor="test_accessor")
        self.assertEqual(result, {"data": {"id": "test_token"}})
        self.mock_adapter.post.assert_called_once()

    def test_renew(self):
        self.mock_adapter.post.return_value = {"auth": {"client_token": "test_token"}}
        result = self.token.renew(token="test_token", increment="1h")
        self.assertEqual(result, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.post.assert_called_once()

    def test_renew_self(self):
        self.mock_adapter.post.return_value = {"auth": {"client_token": "test_token"}}
        result = self.token.renew_self(increment="1h")
        self.assertEqual(result, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.post.assert_called_once()

    def test_renew_accessor(self):
        self.mock_adapter.post.return_value = {"auth": {"client_token": "test_token"}}
        result = self.token.renew_accessor(accessor="test_accessor", increment="1h")
        self.assertEqual(result, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.post.assert_called_once()

    def test_revoke(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.token.revoke(token="test_token")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_revoke_self(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.token.revoke_self()
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_revoke_accessor(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.token.revoke_accessor(accessor="test_accessor")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_revoke_and_orphan_children(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.token.revoke_and_orphan_children(token="test_token")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    def test_read_role(self):
        self.mock_adapter.get.return_value = {"data": {"role_name": "test_role"}}
        result = self.token.read_role(role_name="test_role")
        self.assertEqual(result, {"data": {"role_name": "test_role"}})
        self.mock_adapter.get.assert_called_once()

    def test_list_roles(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["role1", "role2"]}}
        result = self.token.list_roles()
        self.assertEqual(result, {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once()

    def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.token.delete_role(role_name="test_role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    def test_tidy(self):
        self.mock_adapter.post.return_value = Response(204)
        result = self.token.tidy()
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()


class MockAdapter(Adapter):
    def __init__(self, *args, **kwargs):
        if "client" not in kwargs:
            kwargs["client"] = mock.MagicMock()
        super().__init__(*args, **kwargs)

    def request(self, *args, **kwargs):  # pyright: ignore
        return args, kwargs

    def get_login_token(self, response):
        raise NotImplementedError()


@pytest.fixture
def mock_adapter():
    adapter = MockAdapter()
    with mock.patch.object(adapter, "request", mock.Mock(wraps=MockAdapter.request)):
        yield adapter


@pytest.fixture
def token_auth(mock_adapter):
    return Token(mock_adapter)


@pytest.mark.parametrize("allowed_policies", ["allowed_policies", None])
@pytest.mark.parametrize("disallowed_policies", ["disallowed_policies", None])
@pytest.mark.parametrize("orphan", ["orphan", None])
@pytest.mark.parametrize("renewable", ["renewable", None])
@pytest.mark.parametrize("path_suffix", ["path_suffix", None])
@pytest.mark.parametrize("allowed_entity_aliases", ["allowed_entity_aliases", None])
@pytest.mark.parametrize("token_period", ["token_period", None])
@pytest.mark.parametrize("token_explicit_max_ttl", ["token_explicit_max_ttl", None])
def test_create_or_update_role_optional_parameters(
    token_auth,
    allowed_policies,
    disallowed_policies,
    orphan,
    renewable,
    path_suffix,
    allowed_entity_aliases,
    token_period,
    token_explicit_max_ttl,
):
    params = {
        "allowed_policies": allowed_policies,
        "disallowed_policies": disallowed_policies,
        "orphan": orphan,
        "renewable": renewable,
        "path_suffix": path_suffix,
        "allowed_entity_aliases": allowed_entity_aliases,
        "token_period": token_period,
        "token_explicit_max_ttl": token_explicit_max_ttl,
    }
    expected = params.copy()

    _, rkwargs = token_auth.create_or_update_role("role_name", **params)

    assert "json" in rkwargs
    for key, value in expected.items():
        assert value is None or rkwargs["json"][key] == value


class TestAsyncToken(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.token = AsyncToken(self.mock_adapter)

    async def test_create(self):
        self.mock_adapter.post.return_value = {"auth": {"client_token": "test_token"}}
        result = await self.token.create(
            id_="test_id",
            policies=["policy1", "policy2"],
            meta={"key": "value"},
            no_parent=True,
            no_default_policy=True,
            renewable=False,
            ttl="1h",
            type_="service",
            explicit_max_ttl="2h",
            display_name="test_token",
            num_uses=1,
            period="3h",
            entity_alias="test_alias",
            wrap_ttl="15s",
        )
        self.assertEqual(result, {"auth": {"client_token": "test_token"}})
        self.mock_adapter.post.assert_called_once()

    async def test_create_orphan(self):
        self.mock_adapter.post.return_value = {"auth": {"client_token": "test_orphan_token"}}
        result = await self.token.create_orphan(
            id_="test_id",
            policies=["policy1", "policy2"],
            meta={"key": "value"},
            no_default_policy=True,
            renewable=False,
            ttl="1h",
            type_="service",
            explicit_max_ttl="2h",
            display_name="test_orphan_token",
            num_uses=1,
            period="3h",
            entity_alias="test_alias",
            wrap_ttl="15s",
        )
        self.assertEqual(result, {"auth": {"client_token": "test_orphan_token"}})
        self.mock_adapter.post.assert_called_once()

    async def test_list_accessors(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["accessor1", "accessor2"]}}
        result = await self.token.list_accessors()
        self.assertEqual(result, {"data": {"keys": ["accessor1", "accessor2"]}})
        self.mock_adapter.list.assert_called_once()

    async def test_lookup(self):
        self.mock_adapter.post.return_value = {"data": {"id": "test_token"}}
        result = await self.token.lookup(token="test_token")
        self.assertEqual(result, {"data": {"id": "test_token"}})
        self.mock_adapter.post.assert_called_once()

    async def test_lookup_self(self):
        self.mock_adapter.get.return_value = {"data": {"id": "self_token"}}
        result = await self.token.lookup_self()
        self.assertEqual(result, {"data": {"id": "self_token"}})
        self.mock_adapter.get.assert_called_once()

    async def test_lookup_accessor(self):
        self.mock_adapter.post.return_value = {"data": {"id": "test_accessor_token"}}
        result = await self.token.lookup_accessor(accessor="test_accessor")
        self.assertEqual(result, {"data": {"id": "test_accessor_token"}})
        self.mock_adapter.post.assert_called_once()

    async def test_renew(self):
        self.mock_adapter.post.return_value = {"auth": {"client_token": "renewed_token"}}
        result = await self.token.renew(token="test_token", increment="1h")
        self.assertEqual(result, {"auth": {"client_token": "renewed_token"}})
        self.mock_adapter.post.assert_called_once()

    async def test_renew_self(self):
        self.mock_adapter.post.return_value = {"auth": {"client_token": "renewed_self_token"}}
        result = await self.token.renew_self(increment="1h")
        self.assertEqual(result, {"auth": {"client_token": "renewed_self_token"}})
        self.mock_adapter.post.assert_called_once()

    async def test_renew_accessor(self):
        self.mock_adapter.post.return_value = {"auth": {"client_token": "renewed_accessor_token"}}
        result = await self.token.renew_accessor(accessor="test_accessor", increment="1h")
        self.assertEqual(result, {"auth": {"client_token": "renewed_accessor_token"}})
        self.mock_adapter.post.assert_called_once()

    async def test_revoke(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.token.revoke(token="test_token")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_revoke_self(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.token.revoke_self()
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_revoke_accessor(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.token.revoke_accessor(accessor="test_accessor")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_revoke_and_orphan_children(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.token.revoke_and_orphan_children(token="test_token")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()

    async def test_read_role(self):
        self.mock_adapter.get.return_value = {"data": {"role_name": "test_role"}}
        result = await self.token.read_role(role_name="test_role")
        self.assertEqual(result, {"data": {"role_name": "test_role"}})
        self.mock_adapter.get.assert_called_once()

    async def test_list_roles(self):
        self.mock_adapter.list.return_value = {"data": {"keys": ["role1", "role2"]}}
        result = await self.token.list_roles()
        self.assertEqual(result, {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once()

    async def test_create_or_update_role(self):
        self.mock_adapter.post.return_value = {"data": {"role_name": "test_role"}}
        result = await self.token.create_or_update_role(
            role_name="test_role",
            allowed_policies=["policy1", "policy2"],
            disallowed_policies=["policy3"],
            orphan=True,
            renewable=False,
            path_suffix="test_suffix",
            allowed_entity_aliases="test_alias",
            token_period="1h",
            token_explicit_max_ttl="2h",
        )
        self.assertEqual(result, {"data": {"role_name": "test_role"}})
        self.mock_adapter.post.assert_called_once()

    async def test_delete_role(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.token.delete_role(role_name="test_role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once()

    async def test_tidy(self):
        self.mock_adapter.post.return_value = Response(204)
        result = await self.token.tidy()
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once()
