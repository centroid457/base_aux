import pytest
from base_aux.aux_expect.m1_expect_aux import ExpectAux

from base_aux.aux_datetime.m1_datetime import *


# =====================================================================================================================
class Test__DateTime:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # NONE --------
            (True, True),

        ]
    )
    def test__1(self, source, _EXPECTED):
        func_link = lambda: source
        ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
def _examples() -> None:
    pass


# =====================================================================================================================
