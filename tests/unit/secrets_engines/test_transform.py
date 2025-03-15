import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.transform import Transform as AsyncTransform
from vaultx.api.secrets_engines.transform import DEFAULT_MOUNT_POINT, Transform


class TestTransform(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.transform = Transform(self.mock_adapter)

    def test_create_or_update_role(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.create_or_update_role(name="test-role", transformations=["transformation1"])
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/role/test-role",
            json={"transformations": ["transformation1"]},
        )

    def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.transform.read_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/role/test-role",
        )

    def test_list_roles(self):
        mock_response = Response(200, json={"data": {"roles": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.transform.list_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"roles": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/role",
        )

    def test_delete_role(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.transform.delete_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/role/test-role",
        )

    def test_create_or_update_transformation(self):
        mock_response = Response(200, json={"data": {"name": "test-transformation"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.create_or_update_transformation(
            name="test-transformation",
            transform_type="fpe",
            template="template1",
            tweak_source="supplied",
            masking_character="*",
            allowed_roles=["role1"],
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-transformation"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformation/test-transformation",
            json={
                "type": "fpe",
                "template": "template1",
                "tweak_source": "supplied",
                "masking_character": "*",
                "allowed_roles": ["role1"],
            },
        )

    def test_read_transformation(self):
        mock_response = Response(200, json={"data": {"name": "test-transformation"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.transform.read_transformation(name="test-transformation")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-transformation"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformation/test-transformation",
        )

    def test_list_transformations(self):
        mock_response = Response(200, json={"data": {"transformations": ["trans1", "trans2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.transform.list_transformations()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"transformations": ["trans1", "trans2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformation",
        )

    def test_delete_transformation(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.transform.delete_transformation(name="test-transformation")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformation/test-transformation",
        )

    def test_create_or_update_template(self):
        mock_response = Response(200, json={"data": {"name": "test-template"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.create_or_update_template(
            name="test-template",
            template_type="regex",
            pattern="pattern1",
            alphabet="alphabet1",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-template"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/template/test-template",
            json={
                "type": "regex",
                "pattern": "pattern1",
                "alphabet": "alphabet1",
            },
        )

    def test_read_template(self):
        mock_response = Response(200, json={"data": {"name": "test-template"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.transform.read_template(name="test-template")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-template"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/template/test-template",
        )

    def test_list_templates(self):
        mock_response = Response(200, json={"data": {"templates": ["template1", "template2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.transform.list_templates()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"templates": ["template1", "template2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/template",
        )

    def test_delete_template(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.transform.delete_template(name="test-template")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/template/test-template",
            json={"name": "test-template"},
        )

    def test_create_or_update_alphabet(self):
        mock_response = Response(200, json={"data": {"name": "test-alphabet"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.create_or_update_alphabet(name="test-alphabet", alphabet="alphabet1")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-alphabet"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/alphabet/test-alphabet",
            json={"alphabet": "alphabet1"},
        )

    def test_read_alphabet(self):
        mock_response = Response(200, json={"data": {"name": "test-alphabet"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.transform.read_alphabet(name="test-alphabet")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-alphabet"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/alphabet/test-alphabet",
        )

    def test_list_alphabets(self):
        mock_response = Response(200, json={"data": {"alphabets": ["alphabet1", "alphabet2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.transform.list_alphabets()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"alphabets": ["alphabet1", "alphabet2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/alphabet",
        )

    def test_delete_alphabet(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.transform.delete_alphabet(name="test-alphabet")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/alphabet/test-alphabet",
        )

    def test_encode(self):
        mock_response = Response(200, json={"data": {"encoded_value": "encoded"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.encode(role_name="test-role", value="value1", transformation="transformation1")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"encoded_value": "encoded"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/encode/test-role",
            json={"value": "value1", "transformation": "transformation1"},
        )

    def test_decode(self):
        mock_response = Response(200, json={"data": {"decoded_value": "decoded"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.decode(role_name="test-role", value="value1", transformation="transformation1")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"decoded_value": "decoded"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/decode/test-role",
            json={"value": "value1", "transformation": "transformation1"},
        )

    def test_create_or_update_fpe_transformation(self):
        mock_response = Response(200, json={"data": {"name": "test-fpe-transformation"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.create_or_update_fpe_transformation(
            name="test-fpe-transformation",
            template="template1",
            tweak_source="supplied",
            allowed_roles=["role1"],
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-fpe-transformation"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/fpe/test-fpe-transformation",
            json={
                "template": "template1",
                "tweak_source": "supplied",
                "allowed_roles": ["role1"],
            },
        )

    def test_create_or_update_masking_transformation(self):
        mock_response = Response(200, json={"data": {"name": "test-masking-transformation"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.create_or_update_masking_transformation(
            name="test-masking-transformation",
            template="template1",
            masking_character="*",
            allowed_roles=["role1"],
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-masking-transformation"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/masking/test-masking-transformation",
            json={
                "template": "template1",
                "masking_character": "*",
                "allowed_roles": ["role1"],
            },
        )

    def test_create_or_update_tokenization_transformation(self):
        mock_response = Response(200, json={"data": {"name": "test-tokenization-transformation"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.create_or_update_tokenization_transformation(
            name="test-tokenization-transformation",
            max_ttl=3600,
            mapping_mode="default",
            allowed_roles=["role1"],
            stores=["store1"],
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-tokenization-transformation"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/tokenization/test-tokenization-transformation",
            json={
                "max_ttl": 3600,
                "mapping_mode": "default",
                "allowed_roles": ["role1"],
                "stores": ["store1"],
            },
        )

    def test_validate_token(self):
        mock_response = Response(200, json={"data": {"valid": True}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.validate_token(
            role_name="test-role",
            value="token-value",
            transformation="transformation1",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"valid": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/validate/test-role",
            json={
                "value": "token-value",
                "transformation": "transformation1",
            },
        )

    def test_check_tokenization(self):
        mock_response = Response(200, json={"data": {"exists": True}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.check_tokenization(
            role_name="test-role",
            value="token-value",
            transformation="transformation1",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"exists": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenized/test-role",
            json={
                "value": "token-value",
                "transformation": "transformation1",
            },
        )

    def test_retrieve_token_metadata(self):
        mock_response = Response(200, json={"data": {"metadata": {"key": "value"}}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.retrieve_token_metadata(
            role_name="test-role",
            value="token-value",
            transformation="transformation1",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"metadata": {"key": "value"}}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/metadata/test-role",
            json={
                "value": "token-value",
                "transformation": "transformation1",
            },
        )

    def test_snapshot_tokenization_state(self):
        mock_response = Response(200, json={"data": {"snapshot": "snapshot-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.snapshot_tokenization_state(
            name="test-transformation",
            limit=1000,
            continuation="continuation-token",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"snapshot": "snapshot-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/tokenization/snapshot/test-transformation",
            json={
                "limit": 1000,
                "continuation": "continuation-token",
            },
        )

    def test_restore_tokenization_state(self):
        mock_response = Response(200, json={"data": {"restored": True}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.restore_tokenization_state(
            name="test-transformation",
            values="snapshot-data",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"restored": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/tokenization/restore/test-transformation",
            json={
                "values": "snapshot-data",
            },
        )

    def test_export_decoded_tokenization_state(self):
        mock_response = Response(200, json={"data": {"export": "export-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.export_decoded_tokenization_state(
            name="test-transformation",
            limit=1000,
            continuation="continuation-token",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"export": "export-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/tokenization/export-decoded/test-transformation",
            json={
                "limit": 1000,
                "continuation": "continuation-token",
            },
        )

    def test_rotate_tokenization_key(self):
        mock_response = Response(200, json={"data": {"rotated": True}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.rotate_tokenization_key(
            transform_name="test-transformation",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"rotated": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenization/keys/test-transformation/rotate",
        )

    def test_update_tokenization_key_config(self):
        mock_response = Response(200, json={"data": {"updated": True}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.update_tokenization_key_config(
            transform_name="test-transformation",
            min_decryption_version=1,
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"updated": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenization/keys/test-transformation/config",
            json={
                "transform_name": "test-transformation",
                "min_decryption_version": 1,
            },
        )

    def test_list_tokenization_key_configuration(self):
        mock_response = Response(200, json={"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.transform.list_tokenization_key_configuration()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenization/keys/",
        )

    def test_read_tokenization_key_configuration(self):
        mock_response = Response(200, json={"data": {"key": "key1"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.transform.read_tokenization_key_configuration(
            transform_name="test-transformation",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"key": "key1"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenization/keys/test-transformation",
        )

    def test_trim_tokenization_key_version(self):
        mock_response = Response(200, json={"data": {"trimmed": True}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transform.trim_tokenization_key_version(
            transform_name="test-transformation",
            min_available_version=1,
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"trimmed": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenization/keys/test-transformation/trim",
            json={
                "min_available_version": 1,
            },
        )


class TestAsyncTransform(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.transform = AsyncTransform(self.mock_adapter)

    async def test_create_or_update_role_async(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.create_or_update_role(name="test-role", transformations=["transformation1"])
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/role/test-role",
            json={"transformations": ["transformation1"]},
        )

    async def test_read_role_async(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.transform.read_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/role/test-role",
        )

    async def test_list_roles_async(self):
        mock_response = Response(200, json={"data": {"roles": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.transform.list_roles()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"roles": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/role",
        )

    async def test_delete_role_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.transform.delete_role(name="test-role")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/role/test-role",
        )

    async def test_create_or_update_transformation_async(self):
        mock_response = Response(200, json={"data": {"name": "test-transformation"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.create_or_update_transformation(
            name="test-transformation",
            transform_type="fpe",
            template="template1",
            tweak_source="supplied",
            masking_character="*",
            allowed_roles=["role1"],
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-transformation"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformation/test-transformation",
            json={
                "type": "fpe",
                "template": "template1",
                "tweak_source": "supplied",
                "masking_character": "*",
                "allowed_roles": ["role1"],
            },
        )

    async def test_read_transformation_async(self):
        mock_response = Response(200, json={"data": {"name": "test-transformation"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.transform.read_transformation(name="test-transformation")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-transformation"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformation/test-transformation",
        )

    async def test_list_transformations_async(self):
        mock_response = Response(200, json={"data": {"transformations": ["trans1", "trans2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.transform.list_transformations()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"transformations": ["trans1", "trans2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformation",
        )

    async def test_delete_transformation_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.transform.delete_transformation(name="test-transformation")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformation/test-transformation",
        )

    async def test_create_or_update_template_async(self):
        mock_response = Response(200, json={"data": {"name": "test-template"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.create_or_update_template(
            name="test-template",
            template_type="regex",
            pattern="pattern1",
            alphabet="alphabet1",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-template"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/template/test-template",
            json={
                "type": "regex",
                "pattern": "pattern1",
                "alphabet": "alphabet1",
            },
        )

    async def test_read_template_async(self):
        mock_response = Response(200, json={"data": {"name": "test-template"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.transform.read_template(name="test-template")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-template"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/template/test-template",
        )

    async def test_list_templates_async(self):
        mock_response = Response(200, json={"data": {"templates": ["template1", "template2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.transform.list_templates()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"templates": ["template1", "template2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/template",
        )

    async def test_delete_template_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.transform.delete_template(name="test-template")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/template/test-template",
            json={"name": "test-template"},
        )

    async def test_create_or_update_alphabet_async(self):
        mock_response = Response(200, json={"data": {"name": "test-alphabet"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.create_or_update_alphabet(name="test-alphabet", alphabet="alphabet1")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-alphabet"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/alphabet/test-alphabet",
            json={"alphabet": "alphabet1"},
        )

    async def test_read_alphabet_async(self):
        mock_response = Response(200, json={"data": {"name": "test-alphabet"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.transform.read_alphabet(name="test-alphabet")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-alphabet"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/alphabet/test-alphabet",
        )

    async def test_list_alphabets_async(self):
        mock_response = Response(200, json={"data": {"alphabets": ["alphabet1", "alphabet2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.transform.list_alphabets()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"alphabets": ["alphabet1", "alphabet2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/alphabet",
        )

    async def test_delete_alphabet_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.transform.delete_alphabet(name="test-alphabet")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/alphabet/test-alphabet",
        )

    async def test_encode_async(self):
        mock_response = Response(200, json={"data": {"encoded_value": "encoded"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.encode(role_name="test-role", value="value1", transformation="transformation1")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"encoded_value": "encoded"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/encode/test-role",
            json={"value": "value1", "transformation": "transformation1"},
        )

    async def test_decode_async(self):
        mock_response = Response(200, json={"data": {"decoded_value": "decoded"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.decode(role_name="test-role", value="value1", transformation="transformation1")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"decoded_value": "decoded"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/decode/test-role",
            json={"value": "value1", "transformation": "transformation1"},
        )

    async def test_create_or_update_fpe_transformation_async(self):
        mock_response = Response(200, json={"data": {"name": "test-fpe-transformation"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.create_or_update_fpe_transformation(
            name="test-fpe-transformation",
            template="template1",
            tweak_source="supplied",
            allowed_roles=["role1"],
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-fpe-transformation"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/fpe/test-fpe-transformation",
            json={
                "template": "template1",
                "tweak_source": "supplied",
                "allowed_roles": ["role1"],
            },
        )

    async def test_create_or_update_masking_transformation_async(self):
        mock_response = Response(200, json={"data": {"name": "test-masking-transformation"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.create_or_update_masking_transformation(
            name="test-masking-transformation",
            template="template1",
            masking_character="*",
            allowed_roles=["role1"],
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-masking-transformation"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/masking/test-masking-transformation",
            json={
                "template": "template1",
                "masking_character": "*",
                "allowed_roles": ["role1"],
            },
        )

    async def test_create_or_update_tokenization_transformation_async(self):
        mock_response = Response(200, json={"data": {"name": "test-tokenization-transformation"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.create_or_update_tokenization_transformation(
            name="test-tokenization-transformation",
            max_ttl=3600,
            mapping_mode="default",
            allowed_roles=["role1"],
            stores=["store1"],
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-tokenization-transformation"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/tokenization/test-tokenization-transformation",
            json={
                "max_ttl": 3600,
                "mapping_mode": "default",
                "allowed_roles": ["role1"],
                "stores": ["store1"],
            },
        )

    async def test_validate_token_async(self):
        mock_response = Response(200, json={"data": {"valid": True}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.validate_token(
            role_name="test-role",
            value="token-value",
            transformation="transformation1",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"valid": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/validate/test-role",
            json={
                "value": "token-value",
                "transformation": "transformation1",
            },
        )

    async def test_check_tokenization_async(self):
        mock_response = Response(200, json={"data": {"exists": True}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.check_tokenization(
            role_name="test-role",
            value="token-value",
            transformation="transformation1",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"exists": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenized/test-role",
            json={
                "value": "token-value",
                "transformation": "transformation1",
            },
        )

    async def test_retrieve_token_metadata_async(self):
        mock_response = Response(200, json={"data": {"metadata": {"key": "value"}}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.retrieve_token_metadata(
            role_name="test-role",
            value="token-value",
            transformation="transformation1",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"metadata": {"key": "value"}}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/metadata/test-role",
            json={
                "value": "token-value",
                "transformation": "transformation1",
            },
        )

    async def test_snapshot_tokenization_state_async(self):
        mock_response = Response(200, json={"data": {"snapshot": "snapshot-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.snapshot_tokenization_state(
            name="test-transformation",
            limit=1000,
            continuation="continuation-token",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"snapshot": "snapshot-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/tokenization/snapshot/test-transformation",
            json={
                "limit": 1000,
                "continuation": "continuation-token",
            },
        )

    async def test_restore_tokenization_state_async(self):
        mock_response = Response(200, json={"data": {"restored": True}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.restore_tokenization_state(
            name="test-transformation",
            values="snapshot-data",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"restored": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/tokenization/restore/test-transformation",
            json={
                "values": "snapshot-data",
            },
        )

    async def test_export_decoded_tokenization_state_async(self):
        mock_response = Response(200, json={"data": {"export": "export-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.export_decoded_tokenization_state(
            name="test-transformation",
            limit=1000,
            continuation="continuation-token",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"export": "export-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/transformations/tokenization/export-decoded/test-transformation",
            json={
                "limit": 1000,
                "continuation": "continuation-token",
            },
        )

    async def test_rotate_tokenization_key_async(self):
        mock_response = Response(200, json={"data": {"rotated": True}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.rotate_tokenization_key(
            transform_name="test-transformation",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"rotated": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenization/keys/test-transformation/rotate",
        )

    async def test_update_tokenization_key_config_async(self):
        mock_response = Response(200, json={"data": {"updated": True}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.update_tokenization_key_config(
            transform_name="test-transformation",
            min_decryption_version=1,
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"updated": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenization/keys/test-transformation/config",
            json={
                "transform_name": "test-transformation",
                "min_decryption_version": 1,
            },
        )

    async def test_list_tokenization_key_configuration_async(self):
        mock_response = Response(200, json={"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.transform.list_tokenization_key_configuration()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenization/keys/",
        )

    async def test_read_tokenization_key_configuration_async(self):
        mock_response = Response(200, json={"data": {"key": "key1"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.transform.read_tokenization_key_configuration(
            transform_name="test-transformation",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"key": "key1"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenization/keys/test-transformation",
        )

    async def test_trim_tokenization_key_version_async(self):
        mock_response = Response(200, json={"data": {"trimmed": True}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transform.trim_tokenization_key_version(
            transform_name="test-transformation",
            min_available_version=1,
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"trimmed": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/tokenization/keys/test-transformation/trim",
            json={
                "min_available_version": 1,
            },
        )
