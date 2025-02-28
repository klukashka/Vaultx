from unittest import mock

import pytest

from vaultx.adapters import Adapter
from vaultx.api.system_backend.init import Init
from vaultx.exceptions import VaultxError


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
def sys_init(mock_adapter):
    return Init(mock_adapter)


INIT_SECRET_PGP_ERROR_MSG = r"length of pgp_keys list argument must equal secret_shares value"
INIT_RECOVERY_PGP_ERROR_MSG = r"length of recovery_pgp_keys list argument must equal recovery_shares value"
INIT_RECOVERY_SHARES_ERROR_MSG = (
    r"value for recovery_threshold argument must be less than or equal to recovery_shares argument"
)
INIT_STORED_SHARES_ERROR_MSG = r"value for stored_shares argument must equal secret_shares argument"


class TestInit:
    @pytest.mark.parametrize(
        [
            "secret_shares",
            "pgp_keys",
            "stored_shares",
            "recovery_shares",
            "recovery_pgp_keys",
            "recovery_threshold",
            "exc_msg",
        ],
        [
            (
                2,
                [1, 2, 3],
                2,
                None,
                None,
                None,
                INIT_SECRET_PGP_ERROR_MSG,
            ),
            (
                2,
                [1, 2, 3],
                3,
                None,
                None,
                None,
                INIT_SECRET_PGP_ERROR_MSG,
            ),
            (
                2,
                [1, 2],
                3,
                None,
                None,
                None,
                INIT_STORED_SHARES_ERROR_MSG,
            ),
            (2, [1, 2], 2, 3, [1, 2], None, INIT_RECOVERY_PGP_ERROR_MSG),
            (2, [1, 2], 2, 3, [1, 2], 1, INIT_RECOVERY_PGP_ERROR_MSG),
            (2, [1, 2], 2, 3, [1, 2], 9, INIT_RECOVERY_SHARES_ERROR_MSG),
        ],
    )
    def test_initialize_errors(
        self,
        sys_init,
        mock_adapter,
        secret_shares,
        pgp_keys,
        stored_shares,
        recovery_shares,
        recovery_pgp_keys,
        recovery_threshold,
        exc_msg,
    ):
        with pytest.raises(VaultxError, match=exc_msg):
            sys_init.initialize(
                secret_shares=secret_shares,
                pgp_keys=pgp_keys,
                stored_shares=stored_shares,
                recovery_shares=recovery_shares,
                recovery_pgp_keys=recovery_pgp_keys,
                recovery_threshold=recovery_threshold,
            )

        # mock_adapter.request.assert_not_called()

    def test_initialize_value_pass(self, sys_init):
        (_, r_kwargs) = sys_init.initialize(
            secret_threshold=0,
            secret_shares=2,
            root_token_pgp_key="abc",
            pgp_keys=[1, 2],
            stored_shares=2,
            recovery_shares=3,
            recovery_pgp_keys=[1, 2, 3],
            recovery_threshold=3,
        )
        params = r_kwargs["json"]

        assert params["secret_threshold"] == 0
        assert params["secret_shares"] == 2
        assert params["root_token_pgp_key"] == "abc"
        assert params["pgp_keys"] == [1, 2]
        assert params["stored_shares"] == 2
        assert params["recovery_shares"] == 3
        assert params["recovery_pgp_keys"] == [1, 2, 3]
        assert params["recovery_threshold"] == 3
