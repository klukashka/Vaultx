import typing as tp
from typing import Optional
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
from parameterized import parameterized  # type: ignore

from vaultx import exceptions
from vaultx.api.async_secrets_engines.kv import Kv as AsyncKv
from vaultx.api.async_secrets_engines.kv_v1 import KvV1 as AsyncKvV1
from vaultx.api.async_secrets_engines.kv_v2 import KvV2 as AsyncKvV2
from vaultx.api.secrets_engines.kv import Kv
from vaultx.api.secrets_engines.kv_v1 import KvV1
from vaultx.api.secrets_engines.kv_v2 import KvV2


class TestKv(TestCase):
    def test_v1_property(self):
        mock_adapter = MagicMock()
        kv = Kv(adapter=mock_adapter)
        self.assertIsInstance(
            obj=kv.v1,
            cls=KvV1,
        )

    def test_v2_property(self):
        mock_adapter = MagicMock()
        kv = Kv(adapter=mock_adapter)
        self.assertIsInstance(
            obj=kv.v2,
            cls=KvV2,
        )

    @parameterized.expand(
        [
            ("v1", "1"),
            ("v2", "2"),
            ("v3", "3", ValueError),
            ("invalid version", "12345", ValueError),
        ]
    )
    def test_default_kv_version_setter(self, test_label, version, raises: Optional[tp.Type[Exception]] = None):
        version_class_map = {
            "1": KvV1,
            "2": KvV2,
        }
        mock_adapter = MagicMock()
        kv = Kv(adapter=mock_adapter)

        if raises:
            with self.assertRaises(raises):
                kv.default_kv_version = version
        else:
            kv.default_kv_version = version
            self.assertIsInstance(
                obj=getattr(kv, "v%s" % version),
                cls=version_class_map.get(version, object),
            )

    def test_getattr(self):
        mock_adapter = MagicMock()
        kv = Kv(adapter=mock_adapter, default_kv_version="1")
        self.assertEqual(
            first=kv.read_secret,
            second=kv.v1.read_secret,
        )
        kv = Kv(adapter=mock_adapter, default_kv_version="2")
        self.assertEqual(
            first=kv.read_secret_version,
            second=kv.v2.read_secret_version,
        )

        with self.assertRaises(AttributeError):
            kv._default_kv_version = "0"
            assert kv.read_secret


class TestKv2:
    @pytest.mark.parametrize("raise_on_del", [True, False])
    def test_kv2_raise_on_deleted(self, raise_on_del):
        def get_error(*args, **kwargs):
            raise exceptions.HTTPError(404)

        mock_adapter = MagicMock(get=get_error)
        kv = Mock(wraps=Kv(adapter=mock_adapter, default_kv_version="2"))

        for method in [
            kv.read_secret,
            kv.read_secret_version,
            kv.v2.read_secret,
            kv.v2.read_secret_version,
        ]:
            path = "secret_path"
            should_raise = raise_on_del

            if should_raise:
                with pytest.raises(exceptions.HTTPError):
                    method(path=path, raise_on_deleted_version=raise_on_del)
            else:
                result = method(path=path, raise_on_deleted_version=raise_on_del)
                assert result is None


class TestAsyncKv(IsolatedAsyncioTestCase):
    def test_v1_property(self):
        mock_adapter = MagicMock()
        kv = AsyncKv(adapter=mock_adapter)
        self.assertIsInstance(
            obj=kv.v1,
            cls=AsyncKvV1,
        )

    def test_v2_property(self):
        mock_adapter = MagicMock()
        kv = AsyncKv(adapter=mock_adapter)
        self.assertIsInstance(
            obj=kv.v2,
            cls=AsyncKvV2,
        )

    @parameterized.expand(
        [
            ("v1", "1"),
            ("v2", "2"),
            ("v3", "3", ValueError),
            ("invalid version", "12345", ValueError),
        ]
    )
    def test_default_kv_version_setter(self, test_label, version, raises: Optional[tp.Type[Exception]] = None):
        version_class_map = {
            "1": AsyncKvV1,
            "2": AsyncKvV2,
        }
        mock_adapter = MagicMock()
        kv = AsyncKv(adapter=mock_adapter)

        if raises:
            with self.assertRaises(raises):
                kv.default_kv_version = version
        else:
            kv.default_kv_version = version
            self.assertIsInstance(
                obj=getattr(kv, "v%s" % version),
                cls=version_class_map.get(version, object),
            )

    def test_getattr(self):
        mock_adapter = MagicMock()
        kv = Kv(adapter=mock_adapter, default_kv_version="1")
        self.assertEqual(
            first=kv.read_secret,
            second=kv.v1.read_secret,
        )
        kv = AsyncKv(adapter=mock_adapter, default_kv_version="2")
        self.assertEqual(
            first=kv.read_secret_version,
            second=kv.v2.read_secret_version,
        )

        with self.assertRaises(AttributeError):
            kv._default_kv_version = "0"
            assert kv.read_secret


class TestAsyncKv2(IsolatedAsyncioTestCase):
    async def test_kv2_raise_on_deleted(self):
        async def get_error(*args, **kwargs):
            raise exceptions.HTTPError(404)

        mock_adapter = AsyncMock(get=get_error)
        kv = AsyncKv(adapter=mock_adapter, default_kv_version="2")

        # Test both True and False for raise_on_del
        for raise_on_del in [True, False]:
            with self.subTest(raise_on_del=raise_on_del):
                if raise_on_del:
                    with self.assertRaises(exceptions.HTTPError):
                        await kv.v2.read_secret(path="secret_path", raise_on_deleted_version=raise_on_del)
                else:
                    result = await kv.v2.read_secret(path="secret_path", raise_on_deleted_version=raise_on_del)
                    self.assertIsNone(result)

                if raise_on_del:
                    with self.assertRaises(exceptions.HTTPError):
                        await kv.v2.read_secret_version(path="secret_path", raise_on_deleted_version=raise_on_del)
                else:
                    result = await kv.v2.read_secret_version(path="secret_path", raise_on_deleted_version=raise_on_del)
                    self.assertIsNone(result)
