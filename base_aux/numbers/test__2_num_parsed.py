import pytest

from base_aux.aux_expect.m1_expect_aux import *
from base_aux.numbers.m2_num_single_parsed import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        # TRASH ----
        (None, (None, None, None, )),
        (True, (None, None, None, )),
        (False, (None, None, None, )),
        ("", (None, None, None, )),

        ("a1.2.3a", (None, None, None,)),

        # int ----
        (123, (123, 123, None, )),
        ("123", (123, 123, None, )),
        ("a123a", (123, 123, None, )),

        # float ----
        ("a1.00a", (1.0, None, 1.0, )),
    ]
)
def test__NumParsedSingle(source, _EXPECTED):
    ExpectAux(NumParsedSingle(source).resolve).check_assert(_EXPECTED[0])
    ExpectAux(NumParsedSingleInt(source).resolve).check_assert(_EXPECTED[1])
    ExpectAux(NumParsedSingleFloat(source).resolve).check_assert(_EXPECTED[2])


# =====================================================================================================================
