import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_values.m4_primitives import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.aux_eq.m4_eq_valid_chain import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, other, _EXPECTED",
    argvalues=[
        ((EqValid_NotRaise(), ), LAMBDA_RAISE, False),
        ((EqValid_NotRaise(), ), 1, True),
        ((EqValid_NotRaise(), EqValid_Raise()), 1, False),

        ((EqValid_NotRaise(), EqValid_LeGe_Obj(1)), 1, True),
        ((EqValid_NotRaise(), EqValid_LeGe_Obj(100)), 1, False),
        ((EqValid_NotRaise(), EqValid_LeGe_Obj(100, _iresult_reverse=True)), 1, True),
    ]
)
def test___EqValidator(source, other, _EXPECTED):
    ExpectAux(EqValidChain(*source) == other).check_assert(_EXPECTED)


# =====================================================================================================================
