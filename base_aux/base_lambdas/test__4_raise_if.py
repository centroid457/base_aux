import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m4_primitives import *

from base_aux.base_lambdas.m5_raise_if import *
from base_aux.base_values.m3_exceptions import Exx__Expected


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        # SINGLE ---
        ((False,), [None, None]),
        ((None,), [None, None]),
        ((True,), [Exx__Expected, Exx__Expected]),

        ((0,), [None, None]),
        ((1,), [Exx__Expected, Exx__Expected]),

        ((Exception, ), [None, None]),

        ((LAMBDA_FALSE,), [None, None]),
        ((LAMBDA_NONE,), [None, None]),
        ((LAMBDA_TRUE,), [Exx__Expected, Exx__Expected]),
        ((LAMBDA_RAISE,), [None, None]),
        ((LAMBDA_EXX,), [None, None]),

        # SEVERAL ---
        ((0, 1,), [None, Exx__Expected]),
        ((LAMBDA_RAISE, 1,), [None, Exx__Expected]),
    ]
)
def test__RaiseIf(args, _EXPECTED):
    Lambda(RaiseIf_All(*args).resolve).expect__check_assert(_EXPECTED[0])
    Lambda(RaiseIf_Any(*args).resolve).expect__check_assert(_EXPECTED[1])


# =====================================================================================================================
