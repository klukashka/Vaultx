import unittest
from unittest import mock
from httpx import Response
from vaultx.api.async_secrets_engines.transit import Transit as AsyncTransit
from vaultx.api.secrets_engines.transit import Transit, DEFAULT_MOUNT_POINT
from vaultx import exceptions


class TestTransit(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.transit = Transit(self.mock_adapter)

    def test_create_key(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.create_key(
            name="test-key",
            convergent_encryption=True,
            derived=True,
            exportable=True,
            allow_plaintext_backup=True,
            key_type="aes256-gcm96",
            auto_rotate_period="24h",
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key",
            json={
                "convergent_encryption": True,
                "derived": True,
                "exportable": True,
                "allow_plaintext_backup": True,
                "type": "aes256-gcm96",
                "auto_rotate_period": "24h",
            },
        )

    def test_create_key_invalid_key_type(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.create_key(name="test-key", key_type="invalid-type")
        self.assertIn("invalid key_type argument provided", str(context.exception))

    def test_read_key(self):
        mock_response = Response(200, json={"data": {"name": "test-key"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.transit.read_key(name="test-key")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-key"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key",
        )

    def test_list_keys(self):
        mock_response = Response(200, json={"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.transit.list_keys()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys",
        )

    def test_delete_key(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.transit.delete_key(name="test-key")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key",
        )

    def test_update_key_configuration(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.update_key_configuration(
            name="test-key",
            min_decryption_version=1,
            min_encryption_version=2,
            deletion_allowed=True,
            exportable=True,
            allow_plaintext_backup=True,
            auto_rotate_period="24h",
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key/config",
            json={
                "min_decryption_version": 1,
                "min_encryption_version": 2,
                "deletion_allowed": True,
                "exportable": True,
                "allow_plaintext_backup": True,
                "auto_rotate_period": "24h",
            },
        )

    def test_rotate_key(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.rotate_key(name="test-key")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key/rotate",
        )

    def test_export_key(self):
        mock_response = Response(200, json={"data": {"key": "test-key"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.transit.export_key(name="test-key", key_type="encryption-key", version="latest")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"key": "test-key"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"v1/{DEFAULT_MOUNT_POINT}/export/encryption-key/test-key/latest",
        )

    def test_export_key_invalid_key_type(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.export_key(name="test-key", key_type="invalid-type")
        self.assertIn("invalid key_type argument provided", str(context.exception))

    def test_encrypt_data(self):
        mock_response = Response(200, json={"data": {"ciphertext": "encrypted-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.encrypt_data(
            name="test-key",
            plaintext="plaintext-data",
            context="context-data",
            key_version=1,
            nonce="nonce-data",
            _type="aes256-gcm96",
            convergent_encryption="convergent-data",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"ciphertext": "encrypted-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/encrypt/test-key",
            json={
                "plaintext": "plaintext-data",
                "context": "context-data",
                "key_version": 1,
                "nonce": "nonce-data",
                "type": "aes256-gcm96",
                "convergent_encryption": "convergent-data",
            },
        )

    def test_decrypt_data(self):
        mock_response = Response(200, json={"data": {"plaintext": "decrypted-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.decrypt_data(
            name="test-key",
            ciphertext="ciphertext-data",
            context="context-data",
            nonce="nonce-data",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"plaintext": "decrypted-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/decrypt/test-key",
            json={
                "ciphertext": "ciphertext-data",
                "context": "context-data",
                "nonce": "nonce-data",
            },
        )

    def test_rewrap_data(self):
        mock_response = Response(200, json={"data": {"ciphertext": "rewrapped-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.rewrap_data(
            name="test-key",
            ciphertext="ciphertext-data",
            context="context-data",
            key_version=1,
            nonce="nonce-data",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"ciphertext": "rewrapped-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/rewrap/test-key",
            json={
                "ciphertext": "ciphertext-data",
                "context": "context-data",
                "key_version": 1,
                "nonce": "nonce-data",
            },
        )

    def test_generate_data_key(self):
        mock_response = Response(200, json={"data": {"plaintext": "plaintext-key"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.generate_data_key(
            name="test-key",
            key_type="plaintext",
            context="context-data",
            nonce="nonce-data",
            bits=256,
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"plaintext": "plaintext-key"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/datakey/plaintext/test-key",
            json={
                "context": "context-data",
                "nonce": "nonce-data",
                "bits": 256,
            },
        )

    def test_generate_data_key_invalid_key_type(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.generate_data_key(name="test-key", key_type="invalid-type")
        self.assertIn("invalid key_type argument provided", str(context.exception))

    def test_generate_data_key_invalid_bits(self):
        bits = 1024
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.generate_data_key(name="test-key", key_type="plaintext", bits=bits)
        self.assertIn(
            f'invalid bits argument provided "{bits}"',
            str(context.exception)
        )

    def test_generate_random_bytes(self):
        mock_response = Response(200, json={"data": {"random_bytes": "random-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.generate_random_bytes(n_bytes=32, output_format="base64")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"random_bytes": "random-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/random",
            json={
                "bytes": 32,
                "format": "base64",
            },
        )

    def test_hash_data(self):
        mock_response = Response(200, json={"data": {"hash": "hashed-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.hash_data(
            hash_input="input-data",
            algorithm="sha2-256",
            output_format="base64",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"hash": "hashed-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/hash",
            json={
                "input": "input-data",
                "algorithm": "sha2-256",
                "format": "base64",
            },
        )

    def test_hash_data_invalid_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.hash_data(hash_input="input-data", algorithm="invalid-algorithm")
        self.assertIn("invalid algorithm argument provided", str(context.exception))

    def test_hash_data_invalid_output_format(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.hash_data(hash_input="input-data", output_format="invalid-format")
        self.assertIn("invalid output_format argument provided", str(context.exception))

    def test_generate_hmac(self):
        mock_response = Response(200, json={"data": {"hmac": "hmac-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.generate_hmac(
            name="test-key",
            hash_input="input-data",
            key_version=1,
            algorithm="sha2-256",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"hmac": "hmac-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/hmac/test-key",
            json={
                "input": "input-data",
                "key_version": 1,
                "algorithm": "sha2-256",
            },
        )

    def test_generate_hmac_invalid_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.generate_hmac(name="test-key", hash_input="input-data", algorithm="invalid-algorithm")
        self.assertIn("invalid algorithm argument provided", str(context.exception))

    def test_sign_data(self):
        mock_response = Response(200, json={"data": {"signature": "signature-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.sign_data(
            name="test-key",
            hash_input="input-data",
            key_version=1,
            hash_algorithm="sha2-256",
            context="context-data",
            prehashed=True,
            signature_algorithm="pss",
            marshaling_algorithm="asn1",
            salt_length="auto",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"signature": "signature-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/sign/test-key",
            json={
                "input": "input-data",
                "key_version": 1,
                "hash_algorithm": "sha2-256",
                "context": "context-data",
                "prehashed": True,
                "signature_algorithm": "pss",
                "marshaling_algorithm": "asn1",
                "salt_length": "auto",
            },
        )

    def test_sign_data_invalid_hash_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.sign_data(name="test-key", hash_input="input-data", hash_algorithm="invalid-algorithm")
        self.assertIn("invalid hash_algorithm argument provided", str(context.exception))

    def test_sign_data_invalid_signature_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.sign_data(name="test-key", hash_input="input-data", signature_algorithm="invalid-algorithm")
        self.assertIn("invalid signature_algorithm argument provided", str(context.exception))

    def test_sign_data_invalid_marshaling_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.sign_data(name="test-key", hash_input="input-data", marshaling_algorithm="invalid-algorithm")
        self.assertIn("invalid marshaling_algorithm argument provided", str(context.exception))

    def test_sign_data_invalid_salt_length(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.sign_data(name="test-key", hash_input="input-data", salt_length="invalid-length")
        self.assertIn("invalid salt_length argument provided", str(context.exception))

    def test_verify_signed_data(self):
        mock_response = Response(200, json={"data": {"valid": True}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.verify_signed_data(
            name="test-key",
            hash_input="input-data",
            signature="signature-data",
            hash_algorithm="sha2-256",
            context="context-data",
            prehashed=True,
            signature_algorithm="pss",
            marshaling_algorithm="asn1",
            salt_length="auto",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"valid": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/verify/test-key",
            json={
                "name": "test-key",
                "input": "input-data",
                "signature": "signature-data",
                "hash_algorithm": "sha2-256",
                "context": "context-data",
                "prehashed": True,
                "signature_algorithm": "pss",
                "marshaling_algorithm": "asn1",
                "salt_length": "auto",
            },
        )

    def test_verify_signed_data_invalid_hash_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.verify_signed_data(
                name="test-key",
                hash_input="input-data",
                signature="signature-data",
                hash_algorithm="invalid-algorithm",
            )
        self.assertIn("invalid hash_algorithm argument provided", str(context.exception))

    def test_verify_signed_data_invalid_signature_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.verify_signed_data(
                name="test-key",
                hash_input="input-data",
                signature="signature-data",
                signature_algorithm="invalid-algorithm",
            )
        self.assertIn("invalid signature_algorithm argument provided", str(context.exception))

    def test_verify_signed_data_invalid_marshaling_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.verify_signed_data(
                name="test-key",
                hash_input="input-data",
                signature="signature-data",
                marshaling_algorithm="invalid-algorithm",
            )
        self.assertIn("invalid marshaling_algorithm argument provided", str(context.exception))

    def test_verify_signed_data_invalid_salt_length(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            self.transit.verify_signed_data(
                name="test-key",
                hash_input="input-data",
                signature="signature-data",
                salt_length="invalid-length",
            )
        self.assertIn("invalid salt_length argument provided", str(context.exception))

    def test_backup_key(self):
        mock_response = Response(200, json={"data": {"backup": "backup-data"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.transit.backup_key(name="test-key")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"backup": "backup-data"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/backup/test-key",
        )

    def test_restore_key(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.restore_key(backup="backup-data", name="test-key", force=True)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"v1/{DEFAULT_MOUNT_POINT}/restore/test-key",
            json={
                "backup": "backup-data",
                "force": True,
            },
        )

    def test_trim_key(self):
        mock_response = Response(200, json={"data": {"trimmed": True}})
        self.mock_adapter.post.return_value = mock_response

        result = self.transit.trim_key(name="test-key", min_version=1)
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"trimmed": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key/trim",
            json={
                "min_available_version": 1,
            },
        )


class TestAsyncTransit(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.transit = AsyncTransit(self.mock_adapter)

    async def test_create_key(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.create_key(
            name="test-key",
            convergent_encryption=True,
            derived=True,
            exportable=True,
            allow_plaintext_backup=True,
            key_type="aes256-gcm96",
            auto_rotate_period="24h",
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key",
            json={
                "convergent_encryption": True,
                "derived": True,
                "exportable": True,
                "allow_plaintext_backup": True,
                "type": "aes256-gcm96",
                "auto_rotate_period": "24h",
            },
        )

    async def test_create_key_invalid_key_type(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.create_key(name="test-key", key_type="invalid-type")
        self.assertIn("invalid key_type argument provided", str(context.exception))

    async def test_read_key(self):
        mock_response = Response(200, json={"data": {"name": "test-key"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.transit.read_key(name="test-key")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"name": "test-key"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key",
        )

    async def test_list_keys(self):
        mock_response = Response(200, json={"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.transit.list_keys()
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"keys": ["key1", "key2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys",
        )

    async def test_delete_key(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.transit.delete_key(name="test-key")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key",
        )

    async def test_update_key_configuration(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.update_key_configuration(
            name="test-key",
            min_decryption_version=1,
            min_encryption_version=2,
            deletion_allowed=True,
            exportable=True,
            allow_plaintext_backup=True,
            auto_rotate_period="24h",
        )
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key/config",
            json={
                "min_decryption_version": 1,
                "min_encryption_version": 2,
                "deletion_allowed": True,
                "exportable": True,
                "allow_plaintext_backup": True,
                "auto_rotate_period": "24h",
            },
        )

    async def test_rotate_key(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.rotate_key(name="test-key")
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key/rotate",
        )

    async def test_export_key(self):
        mock_response = Response(200, json={"data": {"key": "test-key"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.transit.export_key(name="test-key", key_type="encryption-key", version="latest")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"key": "test-key"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"v1/{DEFAULT_MOUNT_POINT}/export/encryption-key/test-key/latest",
        )

    async def test_export_key_invalid_key_type(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.export_key(name="test-key", key_type="invalid-type")
        self.assertIn("invalid key_type argument provided", str(context.exception))

    async def test_encrypt_data(self):
        mock_response = Response(200, json={"data": {"ciphertext": "encrypted-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.encrypt_data(
            name="test-key",
            plaintext="plaintext-data",
            context="context-data",
            key_version=1,
            nonce="nonce-data",
            _type="aes256-gcm96",
            convergent_encryption="convergent-data",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"ciphertext": "encrypted-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/encrypt/test-key",
            json={
                "plaintext": "plaintext-data",
                "context": "context-data",
                "key_version": 1,
                "nonce": "nonce-data",
                "type": "aes256-gcm96",
                "convergent_encryption": "convergent-data",
            },
        )

    async def test_decrypt_data(self):
        mock_response = Response(200, json={"data": {"plaintext": "decrypted-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.decrypt_data(
            name="test-key",
            ciphertext="ciphertext-data",
            context="context-data",
            nonce="nonce-data",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"plaintext": "decrypted-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/decrypt/test-key",
            json={
                "ciphertext": "ciphertext-data",
                "context": "context-data",
                "nonce": "nonce-data",
            },
        )

    async def test_rewrap_data(self):
        mock_response = Response(200, json={"data": {"ciphertext": "rewrapped-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.rewrap_data(
            name="test-key",
            ciphertext="ciphertext-data",
            context="context-data",
            key_version=1,
            nonce="nonce-data",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"ciphertext": "rewrapped-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/rewrap/test-key",
            json={
                "ciphertext": "ciphertext-data",
                "context": "context-data",
                "key_version": 1,
                "nonce": "nonce-data",
            },
        )

    async def test_generate_data_key(self):
        mock_response = Response(200, json={"data": {"plaintext": "plaintext-key"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.generate_data_key(
            name="test-key",
            key_type="plaintext",
            context="context-data",
            nonce="nonce-data",
            bits=256,
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"plaintext": "plaintext-key"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/datakey/plaintext/test-key",
            json={
                "context": "context-data",
                "nonce": "nonce-data",
                "bits": 256,
            },
        )

    async def test_generate_data_key_invalid_key_type(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.generate_data_key(name="test-key", key_type="invalid-type")
        self.assertIn("invalid key_type argument provided", str(context.exception))

    async def test_generate_data_key_invalid_bits(self):
        bits = 1024
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.generate_data_key(name="test-key", key_type="plaintext", bits=bits)
        self.assertIn(
            f'invalid bits argument provided "{bits}"',
            str(context.exception)
        )

    async def test_generate_random_bytes(self):
        mock_response = Response(200, json={"data": {"random_bytes": "random-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.generate_random_bytes(n_bytes=32, output_format="base64")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"random_bytes": "random-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/random",
            json={
                "bytes": 32,
                "format": "base64",
            },
        )

    async def test_hash_data(self):
        mock_response = Response(200, json={"data": {"hash": "hashed-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.hash_data(
            hash_input="input-data",
            algorithm="sha2-256",
            output_format="base64",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"hash": "hashed-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/hash",
            json={
                "input": "input-data",
                "algorithm": "sha2-256",
                "format": "base64",
            },
        )

    async def test_hash_data_invalid_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.hash_data(hash_input="input-data", algorithm="invalid-algorithm")
        self.assertIn("invalid algorithm argument provided", str(context.exception))

    async def test_hash_data_invalid_output_format(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.hash_data(hash_input="input-data", output_format="invalid-format")
        self.assertIn("invalid output_format argument provided", str(context.exception))

    async def test_generate_hmac(self):
        mock_response = Response(200, json={"data": {"hmac": "hmac-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.generate_hmac(
            name="test-key",
            hash_input="input-data",
            key_version=1,
            algorithm="sha2-256",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"hmac": "hmac-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/hmac/test-key",
            json={
                "input": "input-data",
                "key_version": 1,
                "algorithm": "sha2-256",
            },
        )

    async def test_generate_hmac_invalid_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.generate_hmac(name="test-key", hash_input="input-data", algorithm="invalid-algorithm")
        self.assertIn("invalid algorithm argument provided", str(context.exception))

    async def test_sign_data(self):
        mock_response = Response(200, json={"data": {"signature": "signature-data"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.sign_data(
            name="test-key",
            hash_input="input-data",
            key_version=1,
            hash_algorithm="sha2-256",
            context="context-data",
            prehashed=True,
            signature_algorithm="pss",
            marshaling_algorithm="asn1",
            salt_length="auto",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"signature": "signature-data"}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/sign/test-key",
            json={
                "input": "input-data",
                "key_version": 1,
                "hash_algorithm": "sha2-256",
                "context": "context-data",
                "prehashed": True,
                "signature_algorithm": "pss",
                "marshaling_algorithm": "asn1",
                "salt_length": "auto",
            },
        )

    async def test_sign_data_invalid_hash_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.sign_data(name="test-key", hash_input="input-data", hash_algorithm="invalid-algorithm")
        self.assertIn("invalid hash_algorithm argument provided", str(context.exception))

    async def test_sign_data_invalid_signature_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.sign_data(name="test-key", hash_input="input-data", signature_algorithm="invalid-algorithm")
        self.assertIn("invalid signature_algorithm argument provided", str(context.exception))

    async def test_sign_data_invalid_marshaling_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.sign_data(name="test-key", hash_input="input-data", marshaling_algorithm="invalid-algorithm")
        self.assertIn("invalid marshaling_algorithm argument provided", str(context.exception))

    async def test_sign_data_invalid_salt_length(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.sign_data(name="test-key", hash_input="input-data", salt_length="invalid-length")
        self.assertIn("invalid salt_length argument provided", str(context.exception))

    async def test_verify_signed_data(self):
        mock_response = Response(200, json={"data": {"valid": True}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.verify_signed_data(
            name="test-key",
            hash_input="input-data",
            signature="signature-data",
            hash_algorithm="sha2-256",
            context="context-data",
            prehashed=True,
            signature_algorithm="pss",
            marshaling_algorithm="asn1",
            salt_length="auto",
        )
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"valid": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/verify/test-key",
            json={
                "name": "test-key",
                "input": "input-data",
                "signature": "signature-data",
                "hash_algorithm": "sha2-256",
                "context": "context-data",
                "prehashed": True,
                "signature_algorithm": "pss",
                "marshaling_algorithm": "asn1",
                "salt_length": "auto",
            },
        )

    async def test_verify_signed_data_invalid_hash_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.verify_signed_data(
                name="test-key",
                hash_input="input-data",
                signature="signature-data",
                hash_algorithm="invalid-algorithm",
            )
        self.assertIn("invalid hash_algorithm argument provided", str(context.exception))

    async def test_verify_signed_data_invalid_signature_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.verify_signed_data(
                name="test-key",
                hash_input="input-data",
                signature="signature-data",
                signature_algorithm="invalid-algorithm",
            )
        self.assertIn("invalid signature_algorithm argument provided", str(context.exception))

    async def test_verify_signed_data_invalid_marshaling_algorithm(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.verify_signed_data(
                name="test-key",
                hash_input="input-data",
                signature="signature-data",
                marshaling_algorithm="invalid-algorithm",
            )
        self.assertIn("invalid marshaling_algorithm argument provided", str(context.exception))

    async def test_verify_signed_data_invalid_salt_length(self):
        with self.assertRaises(exceptions.VaultxError) as context:
            await self.transit.verify_signed_data(
                name="test-key",
                hash_input="input-data",
                signature="signature-data",
                salt_length="invalid-length",
            )
        self.assertIn("invalid salt_length argument provided", str(context.exception))

    async def test_backup_key(self):
        mock_response = Response(200, json={"data": {"backup": "backup-data"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.transit.backup_key(name="test-key")
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"backup": "backup-data"}})
        self.mock_adapter.get.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/backup/test-key",
        )

    async def test_restore_key(self):
        mock_response = Response(204)
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.restore_key(backup="backup-data", name="test-key", force=True)
        if isinstance(result, Response):
            self.assertEqual(result.status_code, 204)
        self.mock_adapter.post.assert_called_once_with(
            url=f"v1/{DEFAULT_MOUNT_POINT}/restore/test-key",
            json={
                "backup": "backup-data",
                "force": True,
            },
        )

    async def test_trim_key(self):
        mock_response = Response(200, json={"data": {"trimmed": True}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.transit.trim_key(name="test-key", min_version=1)
        if isinstance(result, Response):
            self.assertEqual(result.json(), {"data": {"trimmed": True}})
        self.mock_adapter.post.assert_called_once_with(
            url=f"/v1/{DEFAULT_MOUNT_POINT}/keys/test-key/trim",
            json={
                "min_available_version": 1,
            },
        )
