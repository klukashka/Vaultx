import typing as tp
from typing import Optional
from unittest import TestCase
from unittest.mock import MagicMock, Mock

import pytest
from parameterized import parameterized  # type: ignore

from vaultx import exceptions
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
    @pytest.mark.parametrize(
        "recoverable",
        [
            False,
            False,
            False,
            True,
        ],
    )
    @pytest.mark.parametrize("raise_on_del", [True, False])
    def test_kv2_raise_on_deleted(self, raise_on_del, recoverable):
        def get_error():
            raise exceptions.VaultxError()

        mock_adapter = MagicMock(get=get_error)
        kv = Mock(wraps=Kv(adapter=mock_adapter, default_kv_version="2"))

        for method in [
            kv.read_secret,
            kv.read_secret_version,
            kv.v2.read_secret,
            kv.v2.read_secret_version,
        ]:
            path = "secret_path"
            should_raise = raise_on_del or not recoverable

            if should_raise:
                with pytest.raises(exceptions.VaultxError):
                    method(path, raise_on_deleted_version=raise_on_del)
