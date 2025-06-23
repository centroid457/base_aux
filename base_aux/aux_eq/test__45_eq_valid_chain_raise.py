import pytest

from base_aux.aux_callable.m2_lambda import *
from base_aux.aux_values.m4_primitives import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.aux_eq.m4_eq_valid_chain import *

from base_aux.aux_eq.m5_eq_raise_if import *
from base_aux.aux_values.m3_exceptions import Exx__Expected


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ((1,), LAMBDA_RAISE, [False, False]),
        ((1,), 1, [True, True]),
        ((1, 2), 1, [False, True]),
        ((1, 2), 0, [False, False]),

        ((EqValid_Raise(), EqValid_NotRaise(), ), LAMBDA_RAISE, [False, True]),
        ((EqValid_NotRaise(), EqValid_Raise(), ), LAMBDA_RAISE, [False, True]),

        ((EqValid_NotRaise(), ), LAMBDA_RAISE, [False, False]),
        ((EqValid_NotRaise(), ), 1, [True, True]),
        ((EqValid_NotRaise(), EqValid_Raise()), 1, [False, True]),

        ((EqValid_NotRaise(), EqValid_GE(1)), 1, [True, True]),
        ((EqValid_NotRaise(), EqValid_GE(100)), 1, [False, True]),
        ((EqValid_NotRaise(), EqValid_GE(100, _iresult_reverse=True)), 1, [True, True]),
    ]
)
def test___EqValidator(args, other, _EXPECTED):
    Lambda(EqValidChain_All(*args) == other).expect__check_assert(_EXPECTED[0])
    Lambda(EqValidChain_Any(*args) == other).expect__check_assert(_EXPECTED[1])

    Lambda(lambda: EqRaiseIf_All(*args) == other).expect__check_assert(Exx__Expected if _EXPECTED[0] else None)
    Lambda(lambda: EqRaiseIf_Any(*args) == other).expect__check_assert(Exx__Expected if _EXPECTED[1] else None)


# =====================================================================================================================
