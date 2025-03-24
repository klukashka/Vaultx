import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.identity import Identity as AsyncIdentity
from vaultx.api.secrets_engines.identity import Identity


class TestIdentity(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.identity = Identity(self.mock_adapter)

    def test_create_or_update_entity(self):
        mock_response = Response(200, json={"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.create_or_update_entity(name="entity-name")
        self.assertEqual(result.json(), {"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity",
            json={"name": "entity-name"},
        )

    def test_create_or_update_entity_by_name(self):
        mock_response = Response(200, json={"data": {"name": "entity-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.create_or_update_entity_by_name(name="entity-name")
        self.assertEqual(result.json(), {"data": {"name": "entity-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity/name/entity-name",
            json={},
        )

    def test_read_entity(self):
        mock_response = Response(200, json={"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_entity(entity_id="entity-id")
        self.assertEqual(result.json(), {"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/entity/id/entity-id",
        )

    def test_read_entity_by_name(self):
        mock_response = Response(200, json={"data": {"name": "entity-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_entity_by_name(name="entity-name")
        self.assertEqual(result.json(), {"data": {"name": "entity-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/entity/name/entity-name",
        )

    def test_update_entity(self):
        mock_response = Response(200, json={"data": {"id": "entity-id", "name": "updated-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.update_entity(entity_id="entity-id", name="updated-name")
        self.assertEqual(result.json(), {"data": {"id": "entity-id", "name": "updated-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity/id/entity-id",
            json={"name": "updated-name"},
        )

    def test_delete_entity(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.identity.delete_entity(entity_id="entity-id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/entity/id/entity-id",
        )

    def test_delete_entity_by_name(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.identity.delete_entity_by_name(name="entity-name")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/entity/name/entity-name",
        )

    def test_list_entities(self):
        mock_response = Response(200, json={"data": {"keys": ["entity1", "entity2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.identity.list_entities(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["entity1", "entity2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/entity/id",
        )

    def test_list_entities_by_name(self):
        mock_response = Response(200, json={"data": {"keys": ["entity1", "entity2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.identity.list_entities_by_name(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["entity1", "entity2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/entity/name",
        )

    def test_merge_entities(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.merge_entities(from_entity_ids=["entity1", "entity2"], to_entity_id="entity3")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity/merge",
            json={"from_entity_ids": ["entity1", "entity2"], "to_entity_id": "entity3"},
        )

    def test_create_or_update_entity_alias(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.create_or_update_entity_alias(
            name="alias-name", canonical_id="entity-id", mount_accessor="accessor"
        )
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity-alias",
            json={"name": "alias-name", "canonical_id": "entity-id", "mount_accessor": "accessor"},
        )

    def test_read_entity_alias(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_entity_alias(alias_id="alias-id")
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/entity-alias/id/alias-id",
        )

    def test_update_entity_alias(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "updated-alias-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.update_entity_alias(
            alias_id="alias-id", name="updated-alias-name", canonical_id="entity-id", mount_accessor="accessor"
        )
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "updated-alias-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity-alias/id/alias-id",
            json={"name": "updated-alias-name", "canonical_id": "entity-id", "mount_accessor": "accessor"},
        )

    def test_list_entity_aliases(self):
        mock_response = Response(200, json={"data": {"keys": ["alias1", "alias2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.identity.list_entity_aliases(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["alias1", "alias2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/entity-alias/id",
        )

    def test_delete_entity_alias(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.identity.delete_entity_alias(alias_id="alias-id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/entity-alias/id/alias-id",
        )

    def test_create_or_update_group(self):
        mock_response = Response(200, json={"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.create_or_update_group(name="group-name")
        self.assertEqual(result.json(), {"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/group",
            json={"name": "group-name", "type": "internal", "member_entity_ids": None, "member_group_ids": None},
        )

    def test_read_group(self):
        mock_response = Response(200, json={"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_group(group_id="group-id")
        self.assertEqual(result.json(), {"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/group/id/group-id",
        )

    def test_update_group(self):
        mock_response = Response(200, json={"data": {"id": "group-id", "name": "updated-group-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.update_group(group_id="group-id", name="updated-group-name")
        self.assertEqual(result.json(), {"data": {"id": "group-id", "name": "updated-group-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/group/id/group-id",
            json={
                "name": "updated-group-name",
                "type": "internal",
                "member_entity_ids": None,
                "member_group_ids": None,
            },
        )

    def test_delete_group(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.identity.delete_group(group_id="group-id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/group/id/group-id",
        )

    def test_list_groups(self):
        mock_response = Response(200, json={"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.identity.list_groups(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/group/id",
        )

    def test_list_groups_by_name(self):
        mock_response = Response(200, json={"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.identity.list_groups_by_name(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/group/name",
        )

    def test_create_or_update_group_by_name(self):
        mock_response = Response(200, json={"data": {"name": "group-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.create_or_update_group_by_name(name="group-name")
        self.assertEqual(result.json(), {"data": {"name": "group-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/group/name/group-name",
            json={"type": "internal"},
        )

    def test_read_group_by_name(self):
        mock_response = Response(200, json={"data": {"name": "group-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_group_by_name(name="group-name")
        self.assertEqual(result.json(), {"data": {"name": "group-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/group/name/group-name",
        )

    def test_delete_group_by_name(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.identity.delete_group_by_name(name="group-name")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/group/name/group-name",
        )

    def test_create_or_update_group_alias(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.create_or_update_group_alias(
            name="alias-name", mount_accessor="accessor", canonical_id="group-id"
        )
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/group-alias",
            json={"name": "alias-name", "mount_accessor": "accessor", "canonical_id": "group-id"},
        )

    def test_update_group_alias(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "updated-alias-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.update_group_alias(
            entity_id="alias-id", name="updated-alias-name", mount_accessor="accessor", canonical_id="group-id"
        )
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "updated-alias-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/group-alias/id/alias-id",
            json={"name": "updated-alias-name", "mount_accessor": "accessor", "canonical_id": "group-id"},
        )

    def test_read_group_alias(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_group_alias(alias_id="alias-id")
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/group-alias/id/alias-id",
        )

    def test_delete_group_alias(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.identity.delete_group_alias(entity_id="alias-id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/group-alias/id/alias-id",
        )

    def test_list_group_aliases(self):
        mock_response = Response(200, json={"data": {"keys": ["alias1", "alias2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.identity.list_group_aliases(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["alias1", "alias2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/group-alias/id",
        )

    def test_lookup_entity(self):
        mock_response = Response(200, json={"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.lookup_entity(name="entity-name")
        self.assertEqual(result.json(), {"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/lookup/entity",
            json={"name": "entity-name"},
        )

    def test_lookup_group(self):
        mock_response = Response(200, json={"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.lookup_group(name="group-name")
        self.assertEqual(result.json(), {"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/lookup/group",
            json={"name": "group-name"},
        )

    def test_configure_tokens_backend(self):
        mock_response = Response(200, json={"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.configure_tokens_backend(issuer="https://vault.example.com")
        self.assertEqual(result.json(), {"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/oidc/config",
            json={"issuer": "https://vault.example.com"},
        )

    def test_read_tokens_backend_configuration(self):
        mock_response = Response(200, json={"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_tokens_backend_configuration()
        self.assertEqual(result.json(), {"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/config",
        )

    def test_create_named_key(self):
        mock_response = Response(200, json={"data": {"name": "key-name", "algorithm": "RS256"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.create_named_key(name="key-name", algorithm="RS256")
        self.assertEqual(result.json(), {"data": {"name": "key-name", "algorithm": "RS256"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/oidc/key/key-name",
            json={
                "name": "key-name",
                "rotation_period": "24h",
                "verification_ttl": "24h",
                "allowed_client_ids": None,
                "algorithm": "RS256",
            },
        )

    def test_read_named_key(self):
        mock_response = Response(200, json={"data": {"name": "key-name", "algorithm": "RS256"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_named_key(name="key-name")
        self.assertEqual(result.json(), {"data": {"name": "key-name", "algorithm": "RS256"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/key/key-name",
        )

    def test_delete_named_key(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.identity.delete_named_key(name="key-name")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/oidc/key/key-name",
        )

    def test_list_named_keys(self):
        mock_response = Response(200, json={"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.identity.list_named_keys()
        self.assertEqual(result.json(), {"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/oidc/key",
        )

    def test_rotate_named_key(self):
        mock_response = Response(200, json={"data": {"name": "key-name", "verification_ttl": "24h"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.rotate_named_key(name="key-name", verification_ttl="24h")
        self.assertEqual(result.json(), {"data": {"name": "key-name", "verification_ttl": "24h"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/oidc/key/key-name",
            json={"verification_ttl": "24h"},
        )

    def test_create_or_update_role(self):
        mock_response = Response(200, json={"data": {"name": "role-name", "key": "key-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.create_or_update_role(name="role-name", key="key-name")
        self.assertEqual(result.json(), {"data": {"name": "role-name", "key": "key-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/oidc/role/role-name",
            json={"key": "key-name", "ttl": "24h"},
        )

    def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "role-name", "key": "key-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_role(name="role-name")
        self.assertEqual(result.json(), {"data": {"name": "role-name", "key": "key-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/role/role-name",
        )

    def test_delete_role(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.identity.delete_role(name="role-name")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/oidc/role/role-name",
        )

    def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.identity.list_roles()
        self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/oidc/role",
        )

    def test_generate_signed_id_token(self):
        mock_response = Response(200, json={"data": {"token": "signed-token"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.generate_signed_id_token(name="role-name")
        self.assertEqual(result.json(), {"data": {"token": "signed-token"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/token/role-name",
        )

    def test_introspect_signed_id_token(self):
        mock_response = Response(200, json={"data": {"active": True}})
        self.mock_adapter.post.return_value = mock_response

        result = self.identity.introspect_signed_id_token(token="signed-token")
        self.assertEqual(result.json(), {"data": {"active": True}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/oidc/introspect",
            json={"token": "signed-token"},
        )

    def test_read_well_known_configurations(self):
        mock_response = Response(200, json={"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_well_known_configurations()
        self.assertEqual(result.json(), {"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/.well-known/openid-configuration",
        )

    def test_read_active_public_keys(self):
        mock_response = Response(200, json={"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.get.return_value = mock_response

        result = self.identity.read_active_public_keys()
        self.assertEqual(result.json(), {"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/.well-known/keys",
        )


class TestAsyncIdentity(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.identity = AsyncIdentity(self.mock_adapter)

    async def test_create_or_update_entity_async(self):
        mock_response = Response(200, json={"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.create_or_update_entity(name="entity-name")
        self.assertEqual(result.json(), {"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity",
            json={"name": "entity-name"},
        )

    async def test_create_or_update_entity_by_name_async(self):
        mock_response = Response(200, json={"data": {"name": "entity-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.create_or_update_entity_by_name(name="entity-name")
        self.assertEqual(result.json(), {"data": {"name": "entity-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity/name/entity-name",
            json={},
        )

    async def test_read_entity_async(self):
        mock_response = Response(200, json={"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_entity(entity_id="entity-id")
        self.assertEqual(result.json(), {"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/entity/id/entity-id",
        )

    async def test_read_entity_by_name_async(self):
        mock_response = Response(200, json={"data": {"name": "entity-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_entity_by_name(name="entity-name")
        self.assertEqual(result.json(), {"data": {"name": "entity-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/entity/name/entity-name",
        )

    async def test_update_entity_async(self):
        mock_response = Response(200, json={"data": {"id": "entity-id", "name": "updated-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.update_entity(entity_id="entity-id", name="updated-name")
        self.assertEqual(result.json(), {"data": {"id": "entity-id", "name": "updated-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity/id/entity-id",
            json={"name": "updated-name"},
        )

    async def test_delete_entity_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.identity.delete_entity(entity_id="entity-id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/entity/id/entity-id",
        )

    async def test_delete_entity_by_name_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.identity.delete_entity_by_name(name="entity-name")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/entity/name/entity-name",
        )

    async def test_list_entities_async(self):
        mock_response = Response(200, json={"data": {"keys": ["entity1", "entity2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.identity.list_entities(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["entity1", "entity2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/entity/id",
        )

    async def test_list_entities_by_name_async(self):
        mock_response = Response(200, json={"data": {"keys": ["entity1", "entity2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.identity.list_entities_by_name(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["entity1", "entity2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/entity/name",
        )

    async def test_merge_entities_async(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.merge_entities(from_entity_ids=["entity1", "entity2"], to_entity_id="entity3")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity/merge",
            json={"from_entity_ids": ["entity1", "entity2"], "to_entity_id": "entity3"},
        )

    async def test_create_or_update_entity_alias_async(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.create_or_update_entity_alias(
            name="alias-name", canonical_id="entity-id", mount_accessor="accessor"
        )
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity-alias",
            json={"name": "alias-name", "canonical_id": "entity-id", "mount_accessor": "accessor"},
        )

    async def test_read_entity_alias_async(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_entity_alias(alias_id="alias-id")
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/entity-alias/id/alias-id",
        )

    async def test_update_entity_alias_async(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "updated-alias-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.update_entity_alias(
            alias_id="alias-id", name="updated-alias-name", canonical_id="entity-id", mount_accessor="accessor"
        )
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "updated-alias-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/entity-alias/id/alias-id",
            json={"name": "updated-alias-name", "canonical_id": "entity-id", "mount_accessor": "accessor"},
        )

    async def test_list_entity_aliases_async(self):
        mock_response = Response(200, json={"data": {"keys": ["alias1", "alias2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.identity.list_entity_aliases(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["alias1", "alias2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/entity-alias/id",
        )

    async def test_delete_entity_alias_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.identity.delete_entity_alias(alias_id="alias-id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/entity-alias/id/alias-id",
        )

    async def test_create_or_update_group_async(self):
        mock_response = Response(200, json={"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.create_or_update_group(name="group-name")
        self.assertEqual(result.json(), {"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/group",
            json={"name": "group-name", "type": "internal", "member_entity_ids": None, "member_group_ids": None},
        )

    async def test_read_group_async(self):
        mock_response = Response(200, json={"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_group(group_id="group-id")
        self.assertEqual(result.json(), {"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/group/id/group-id",
        )

    async def test_update_group_async(self):
        mock_response = Response(200, json={"data": {"id": "group-id", "name": "updated-group-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.update_group(group_id="group-id", name="updated-group-name")
        self.assertEqual(result.json(), {"data": {"id": "group-id", "name": "updated-group-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/group/id/group-id",
            json={
                "name": "updated-group-name",
                "type": "internal",
                "member_entity_ids": None,
                "member_group_ids": None,
            },
        )

    async def test_delete_group_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.identity.delete_group(group_id="group-id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/group/id/group-id",
        )

    async def test_list_groups_async(self):
        mock_response = Response(200, json={"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.identity.list_groups(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/group/id",
        )

    async def test_list_groups_by_name_async(self):
        mock_response = Response(200, json={"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.identity.list_groups_by_name(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["group1", "group2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/group/name",
        )

    async def test_create_or_update_group_by_name_async(self):
        mock_response = Response(200, json={"data": {"name": "group-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.create_or_update_group_by_name(name="group-name")
        self.assertEqual(result.json(), {"data": {"name": "group-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/group/name/group-name",
            json={"type": "internal"},
        )

    async def test_read_group_by_name_async(self):
        mock_response = Response(200, json={"data": {"name": "group-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_group_by_name(name="group-name")
        self.assertEqual(result.json(), {"data": {"name": "group-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/group/name/group-name",
        )

    async def test_delete_group_by_name_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.identity.delete_group_by_name(name="group-name")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/group/name/group-name",
        )

    async def test_create_or_update_group_alias_async(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.create_or_update_group_alias(
            name="alias-name", mount_accessor="accessor", canonical_id="group-id"
        )
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/group-alias",
            json={"name": "alias-name", "mount_accessor": "accessor", "canonical_id": "group-id"},
        )

    async def test_update_group_alias_async(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "updated-alias-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.update_group_alias(
            entity_id="alias-id", name="updated-alias-name", mount_accessor="accessor", canonical_id="group-id"
        )
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "updated-alias-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/group-alias/id/alias-id",
            json={"name": "updated-alias-name", "mount_accessor": "accessor", "canonical_id": "group-id"},
        )

    async def test_read_group_alias_async(self):
        mock_response = Response(200, json={"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_group_alias(alias_id="alias-id")
        self.assertEqual(result.json(), {"data": {"id": "alias-id", "name": "alias-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/group-alias/id/alias-id",
        )

    async def test_delete_group_alias_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.identity.delete_group_alias(entity_id="alias-id")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/group-alias/id/alias-id",
        )

    async def test_list_group_aliases_async(self):
        mock_response = Response(200, json={"data": {"keys": ["alias1", "alias2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.identity.list_group_aliases(method="LIST")
        self.assertEqual(result.json(), {"data": {"keys": ["alias1", "alias2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/group-alias/id",
        )

    async def test_lookup_entity_async(self):
        mock_response = Response(200, json={"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.lookup_entity(name="entity-name")
        self.assertEqual(result.json(), {"data": {"id": "entity-id", "name": "entity-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/lookup/entity",
            json={"name": "entity-name"},
        )

    async def test_lookup_group_async(self):
        mock_response = Response(200, json={"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.lookup_group(name="group-name")
        self.assertEqual(result.json(), {"data": {"id": "group-id", "name": "group-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/lookup/group",
            json={"name": "group-name"},
        )

    async def test_configure_tokens_backend_async(self):
        mock_response = Response(200, json={"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.configure_tokens_backend(issuer="https://vault.example.com")
        self.assertEqual(result.json(), {"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/oidc/config",
            json={"issuer": "https://vault.example.com"},
        )

    async def test_read_tokens_backend_configuration_async(self):
        mock_response = Response(200, json={"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_tokens_backend_configuration()
        self.assertEqual(result.json(), {"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/config",
        )

    async def test_create_named_key_async(self):
        mock_response = Response(200, json={"data": {"name": "key-name", "algorithm": "RS256"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.create_named_key(name="key-name", algorithm="RS256")
        self.assertEqual(result.json(), {"data": {"name": "key-name", "algorithm": "RS256"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/oidc/key/key-name",
            json={
                "name": "key-name",
                "rotation_period": "24h",
                "verification_ttl": "24h",
                "allowed_client_ids": None,
                "algorithm": "RS256",
            },
        )

    async def test_read_named_key_async(self):
        mock_response = Response(200, json={"data": {"name": "key-name", "algorithm": "RS256"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_named_key(name="key-name")
        self.assertEqual(result.json(), {"data": {"name": "key-name", "algorithm": "RS256"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/key/key-name",
        )

    async def test_delete_named_key_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.identity.delete_named_key(name="key-name")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/oidc/key/key-name",
        )

    async def test_list_named_keys_async(self):
        mock_response = Response(200, json={"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.identity.list_named_keys()
        self.assertEqual(result.json(), {"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/oidc/key",
        )

    async def test_rotate_named_key_async(self):
        mock_response = Response(200, json={"data": {"name": "key-name", "verification_ttl": "24h"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.rotate_named_key(name="key-name", verification_ttl="24h")
        self.assertEqual(result.json(), {"data": {"name": "key-name", "verification_ttl": "24h"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/oidc/key/key-name",
            json={"verification_ttl": "24h"},
        )

    async def test_create_or_update_role_async(self):
        mock_response = Response(200, json={"data": {"name": "role-name", "key": "key-name"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.create_or_update_role(name="role-name", key="key-name")
        self.assertEqual(result.json(), {"data": {"name": "role-name", "key": "key-name"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/oidc/role/role-name",
            json={"key": "key-name", "ttl": "24h"},
        )

    async def test_read_role_async(self):
        mock_response = Response(200, json={"data": {"name": "role-name", "key": "key-name"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_role(name="role-name")
        self.assertEqual(result.json(), {"data": {"name": "role-name", "key": "key-name"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/role/role-name",
        )

    async def test_delete_role_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.identity.delete_role(name="role-name")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/identity/oidc/role/role-name",
        )

    async def test_list_roles_async(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.identity.list_roles()
        self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/identity/oidc/role",
        )

    async def test_generate_signed_id_token_async(self):
        mock_response = Response(200, json={"data": {"token": "signed-token"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.generate_signed_id_token(name="role-name")
        self.assertEqual(result.json(), {"data": {"token": "signed-token"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/token/role-name",
        )

    async def test_introspect_signed_id_token_async(self):
        mock_response = Response(200, json={"data": {"active": True}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.identity.introspect_signed_id_token(token="signed-token")
        self.assertEqual(result.json(), {"data": {"active": True}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/identity/oidc/introspect",
            json={"token": "signed-token"},
        )

    async def test_read_well_known_configurations_async(self):
        mock_response = Response(200, json={"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_well_known_configurations()
        self.assertEqual(result.json(), {"data": {"issuer": "https://vault.example.com"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/.well-known/openid-configuration",
        )

    async def test_read_active_public_keys_async(self):
        mock_response = Response(200, json={"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.identity.read_active_public_keys()
        self.assertEqual(result.json(), {"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/identity/oidc/.well-known/keys",
        )
