import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m4_primitives import *

from base_aux.aux_eq.m4_eq_valid2_derivatives import *
from base_aux.base_values.m3_exceptions import Exc__ExpectedAnother


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ((1,), LAMBDA_RAISE, [False, False]),
        ((1,), 1, [True, True]),
        ((1, 2), 1, [False, True]),
        ((1, 2), 0, [False, False]),

        # ((EqValid_Raised(), EqValid_NotRaised(), ), LAMBDA_RAISE, [False, True]),
        # ((EqValid_NotRaised(), EqValid_Raised(), ), LAMBDA_RAISE, [False, True]),

        ((EqValid_Raised(),), LAMBDA_RAISE, [True, True]),
        ((EqValid_Raised(),), LAMBDA_1, [False, False]),
        ((EqValid_Raised(),), 1, [False, False]),
        ((EqValid_Raised(), EqValid_NotRaised()), 1, [False, True]),

        ((EqValid_NotRaised(),), LAMBDA_RAISE, [False, False]),
        ((EqValid_NotRaised(),), 1, [True, True]),
        ((EqValid_NotRaised(), EqValid_Raised()), 1, [False, True]),

        ((EqValid_NotRaised(), EqValid_GE(1)), 1, [True, True]),
        ((EqValid_NotRaised(), EqValid_GE(100)), 1, [False, True]),
    ]
)
def test___EqValidator(args, other, _EXPECTED):
    Lambda(lambda: EqValid_EQ_AllTrue(*args) == other).check_expected__assert(_EXPECTED[0])
    Lambda(lambda: EqValid_EQ_AnyTrue(*args) == other).check_expected__assert(_EXPECTED[1])


# =====================================================================================================================
