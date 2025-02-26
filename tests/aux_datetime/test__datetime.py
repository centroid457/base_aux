import pytest
from base_aux.aux_expect.m1_expect_aux import ExpectAux

from base_aux.aux_datetime.m1_datetime import *


# =====================================================================================================================
class Test__DateTime:
    @pytest.mark.parametrize(
        argnames="source, other, _EXPECTED",
        argvalues=[
            # NONE --------
            (True, None, (False, True)),

        ]
    )
    def test__1(self, source, other, _EXPECTED):
        ExpectAux(source == other).check_assert(_EXPECTED[0])

        func_link = lambda x: x in source
        ExpectAux(func_link, other).check_assert(_EXPECTED[1])


# =====================================================================================================================
def _examples() -> None:
    pass


# =====================================================================================================================
