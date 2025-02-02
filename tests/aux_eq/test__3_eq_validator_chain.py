import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_types.m0_primitives import *

from base_aux.aux_eq.m2_eq_validator import _EqValidator
from base_aux.aux_eq.m2_eq_validator import *
from base_aux.aux_eq.m3_eq_validator_chains import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, other, _EXPECTED",
    argvalues=[
        ((EqValid_NotRaise(), ), LAMBDA_RAISE, False),
        ((EqValid_NotRaise(), ), 1, True),
        ((EqValid_NotRaise(), EqValid_Raise()), 1, False),

        ((EqValid_NotRaise(), EqValid_LeGe(1)), 1, True),
        ((EqValid_NotRaise(), EqValid_LeGe(100)), 1, False),
        ((EqValid_NotRaise(), EqValid_LeGe(100, reverse=True)), 1, True),
    ]
)
def test___EqValidator(source, other, _EXPECTED):
    ExpectAux(EqValidChain(*source) == other).check_assert(_EXPECTED)


# =====================================================================================================================
