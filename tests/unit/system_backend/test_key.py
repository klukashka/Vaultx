import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_system_backend.key import Key as AsyncKey
from vaultx.api.system_backend.key import Key
from vaultx.exceptions import VaultxError


class TestKey(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.key = Key(self.mock_adapter)

    def test_read_root_generation_progress(self):
        self.mock_adapter.get.return_value = {"nonce": "test_nonce"}
        result = self.key.read_root_generation_progress()
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/generate-root/attempt")

    def test_start_root_token_generation_with_otp(self):
        self.mock_adapter.put.return_value = {"nonce": "test_nonce"}
        result = self.key.start_root_token_generation(otp="test_otp")
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/generate-root/attempt",
            json={"otp": "test_otp"},
        )

    def test_start_root_token_generation_with_pgp_key(self):
        self.mock_adapter.put.return_value = {"nonce": "test_nonce"}
        result = self.key.start_root_token_generation(pgp_key="test_pgp_key")
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/generate-root/attempt",
            json={"pgp_key": "test_pgp_key"},
        )

    def test_start_root_token_generation_with_both_otp_and_pgp_key(self):
        with self.assertRaises(VaultxError) as context:
            self.key.start_root_token_generation(otp="test_otp", pgp_key="test_pgp_key")
        self.assertEqual(
            str(context.exception),
            "one (and only one) of otp or pgp_key arguments are required",
        )

    def test_generate_root(self):
        self.mock_adapter.put.return_value = {"complete": True}
        result = self.key.generate_root(key="test_key", nonce="test_nonce")
        self.assertEqual(result, {"complete": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/generate-root/update",
            json={"key": "test_key", "nonce": "test_nonce"},
        )

    def test_cancel_root_generation(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.key.cancel_root_generation()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/generate-root/attempt")

    def test_get_encryption_key_status(self):
        self.mock_adapter.get.return_value = {"key": "test_key"}
        result = self.key.get_encryption_key_status()
        self.assertEqual(result, {"key": "test_key"})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/key-status")

    def test_rotate_encryption_key(self):
        self.mock_adapter.put.return_value = Response(204)
        result = self.key.rotate_encryption_key()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(url="/v1/sys/rotate")

    def test_read_rekey_progress(self):
        self.mock_adapter.get.return_value = {"nonce": "test_nonce"}
        result = self.key.read_rekey_progress()
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/rekey/init")

    def test_read_rekey_progress_recovery_key(self):
        self.mock_adapter.get.return_value = {"nonce": "test_nonce"}
        result = self.key.read_rekey_progress(recovery_key=True)
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/rekey-recovery-key/init")

    def test_start_rekey(self):
        self.mock_adapter.put.return_value = {"nonce": "test_nonce"}
        result = self.key.start_rekey(secret_shares=5, secret_threshold=3)
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/rekey/init",
            json={
                "secret_shares": 5,
                "secret_threshold": 3,
                "require_verification": False,
            },
        )

    def test_start_rekey_with_pgp_keys(self):
        self.mock_adapter.put.return_value = {"nonce": "test_nonce"}
        result = self.key.start_rekey(
            secret_shares=2,
            secret_threshold=2,
            pgp_keys=[123, 1234],
            backup=True,
        )
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/rekey/init",
            json={
                "secret_shares": 2,
                "secret_threshold": 2,
                "pgp_keys": [123, 1234],
                "backup": True,
                "require_verification": False,
            },
        )

    def test_start_rekey_invalid_pgp_keys(self):
        with self.assertRaises(VaultxError) as context:
            self.key.start_rekey(
                secret_shares=3,
                secret_threshold=2,
                pgp_keys=[12345],
            )
        self.assertEqual(
            str(context.exception),
            "length of pgp_keys argument must equal secret shares value",
        )

    def test_cancel_rekey(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.key.cancel_rekey()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/rekey/init")

    def test_cancel_rekey_recovery_key(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.key.cancel_rekey(recovery_key=True)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/rekey-recovery-key/init")

    def test_rekey(self):
        self.mock_adapter.put.return_value = {"complete": True}
        result = self.key.rekey(key="test_key", nonce="test_nonce")
        self.assertEqual(result, {"complete": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/rekey/update",
            json={"key": "test_key", "nonce": "test_nonce"},
        )

    def test_rekey_recovery_key(self):
        self.mock_adapter.put.return_value = {"complete": True}
        result = self.key.rekey(key="test_key", nonce="test_nonce", recovery_key=True)
        self.assertEqual(result, {"complete": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/rekey-recovery-key/update",
            json={"key": "test_key", "nonce": "test_nonce"},
        )

    def test_rekey_multi(self):
        self.mock_adapter.put.side_effect = [
            {"complete": False},
            {"complete": True},
        ]
        result = self.key.rekey_multi(keys=["key1", "key2"], nonce="test_nonce")
        self.assertEqual(result, {"complete": True})
        self.assertEqual(self.mock_adapter.put.call_count, 2)

    def test_read_backup_keys(self):
        self.mock_adapter.get.return_value = {"keys": ["key1", "key2"]}
        result = self.key.read_backup_keys()
        self.assertEqual(result, {"keys": ["key1", "key2"]})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/rekey/backup")

    def test_cancel_rekey_verify(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = self.key.cancel_rekey_verify()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/rekey/verify")

    def test_rekey_verify(self):
        self.mock_adapter.put.return_value = {"complete": True}
        result = self.key.rekey_verify(key="test_key", nonce="test_nonce")
        self.assertEqual(result, {"complete": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/rekey/verify",
            json={"key": "test_key", "nonce": "test_nonce"},
        )

    def test_rekey_verify_multi(self):
        self.mock_adapter.put.side_effect = [
            {"complete": False},
            {"complete": True},
        ]
        result = self.key.rekey_verify_multi(keys=["key1", "key2"], nonce="test_nonce")
        self.assertEqual(result, {"complete": True})
        self.assertEqual(self.mock_adapter.put.call_count, 2)

    def test_read_rekey_verify_progress(self):
        self.mock_adapter.get.return_value = {"nonce": "test_nonce"}
        result = self.key.read_rekey_verify_progress()
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/rekey/verify")


class TestAsyncKey(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.key = AsyncKey(self.mock_adapter)

    async def test_read_root_generation_progress(self):
        self.mock_adapter.get.return_value = {"nonce": "test_nonce"}
        result = await self.key.read_root_generation_progress()
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/generate-root/attempt")

    async def test_start_root_token_generation_with_otp(self):
        self.mock_adapter.put.return_value = {"nonce": "test_nonce"}
        result = await self.key.start_root_token_generation(otp="test_otp")
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.put.assert_called_once_with(url="/v1/sys/generate-root/attempt", json={"otp": "test_otp"})

    async def test_start_root_token_generation_with_pgp_key(self):
        self.mock_adapter.put.return_value = {"nonce": "test_nonce"}
        result = await self.key.start_root_token_generation(pgp_key="test_pgp_key")
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/generate-root/attempt", json={"pgp_key": "test_pgp_key"}
        )

    async def test_start_root_token_generation_with_both_otp_and_pgp_key(self):
        with self.assertRaises(VaultxError) as context:
            await self.key.start_root_token_generation(otp="test_otp", pgp_key="test_pgp_key")
        self.assertEqual(str(context.exception), "one (and only one) of otp or pgp_key arguments are required")

    async def test_generate_root(self):
        self.mock_adapter.put.return_value = {"complete": True}
        result = await self.key.generate_root(key="test_key", nonce="test_nonce")
        self.assertEqual(result, {"complete": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/generate-root/update", json={"key": "test_key", "nonce": "test_nonce"}
        )

    async def test_cancel_root_generation(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.key.cancel_root_generation()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/generate-root/attempt")

    async def test_get_encryption_key_status(self):
        self.mock_adapter.get.return_value = {"key": "test_key"}
        result = await self.key.get_encryption_key_status()
        self.assertEqual(result, {"key": "test_key"})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/key-status")

    async def test_rotate_encryption_key(self):
        self.mock_adapter.put.return_value = Response(204)
        result = await self.key.rotate_encryption_key()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.put.assert_called_once_with(url="/v1/sys/rotate")

    async def test_read_rekey_progress(self):
        self.mock_adapter.get.return_value = {"nonce": "test_nonce"}
        result = await self.key.read_rekey_progress()
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/rekey/init")

    async def test_read_rekey_progress_recovery_key(self):
        self.mock_adapter.get.return_value = {"nonce": "test_nonce"}
        result = await self.key.read_rekey_progress(recovery_key=True)
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/rekey-recovery-key/init")

    async def test_start_rekey(self):
        self.mock_adapter.put.return_value = {"nonce": "test_nonce"}
        result = await self.key.start_rekey(secret_shares=5, secret_threshold=3)
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/rekey/init", json={"secret_shares": 5, "secret_threshold": 3, "require_verification": False}
        )

    async def test_start_rekey_with_pgp_keys(self):
        self.mock_adapter.put.return_value = {"nonce": "test_nonce"}
        result = await self.key.start_rekey(secret_shares=2, secret_threshold=2, pgp_keys=[123, 1234], backup=True)
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/rekey/init",
            json={
                "secret_shares": 2,
                "secret_threshold": 2,
                "pgp_keys": [123, 1234],
                "backup": True,
                "require_verification": False,
            },
        )

    async def test_start_rekey_invalid_pgp_keys(self):
        with self.assertRaises(VaultxError) as context:
            await self.key.start_rekey(secret_shares=3, secret_threshold=2, pgp_keys=[12345])
        self.assertEqual(str(context.exception), "length of pgp_keys argument must equal secret shares value")

    async def test_cancel_rekey(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.key.cancel_rekey()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/rekey/init")

    async def test_cancel_rekey_recovery_key(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.key.cancel_rekey(recovery_key=True)
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/rekey-recovery-key/init")

    async def test_rekey(self):
        self.mock_adapter.put.return_value = {"complete": True}
        result = await self.key.rekey(key="test_key", nonce="test_nonce")
        self.assertEqual(result, {"complete": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/rekey/update", json={"key": "test_key", "nonce": "test_nonce"}
        )

    async def test_rekey_recovery_key(self):
        self.mock_adapter.put.return_value = {"complete": True}
        result = await self.key.rekey(key="test_key", nonce="test_nonce", recovery_key=True)
        self.assertEqual(result, {"complete": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/rekey-recovery-key/update", json={"key": "test_key", "nonce": "test_nonce"}
        )

    async def test_rekey_multi(self):
        self.mock_adapter.put.side_effect = [{"complete": False}, {"complete": True}]
        result = await self.key.rekey_multi(keys=["key1", "key2"], nonce="test_nonce")
        self.assertEqual(result, {"complete": True})
        self.assertEqual(self.mock_adapter.put.call_count, 2)

    async def test_read_backup_keys(self):
        self.mock_adapter.get.return_value = {"keys": ["key1", "key2"]}
        result = await self.key.read_backup_keys()
        self.assertEqual(result, {"keys": ["key1", "key2"]})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/rekey/backup")

    async def test_cancel_rekey_verify(self):
        self.mock_adapter.delete.return_value = Response(204)
        result = await self.key.cancel_rekey_verify()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(url="/v1/sys/rekey/verify")

    async def test_rekey_verify(self):
        self.mock_adapter.put.return_value = {"complete": True}
        result = await self.key.rekey_verify(key="test_key", nonce="test_nonce")
        self.assertEqual(result, {"complete": True})
        self.mock_adapter.put.assert_called_once_with(
            url="/v1/sys/rekey/verify", json={"key": "test_key", "nonce": "test_nonce"}
        )

    async def test_rekey_verify_multi(self):
        self.mock_adapter.put.side_effect = [{"complete": False}, {"complete": True}]
        result = await self.key.rekey_verify_multi(keys=["key1", "key2"], nonce="test_nonce")
        self.assertEqual(result, {"complete": True})
        self.assertEqual(self.mock_adapter.put.call_count, 2)

    async def test_read_rekey_verify_progress(self):
        self.mock_adapter.get.return_value = {"nonce": "test_nonce"}
        result = await self.key.read_rekey_verify_progress()
        self.assertEqual(result, {"nonce": "test_nonce"})
        self.mock_adapter.get.assert_called_once_with(url="/v1/sys/rekey/verify")
