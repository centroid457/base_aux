import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_values.m4_primitives import *

from base_aux.aux_callable.m4_raise_if import *
from base_aux.aux_values.m3_exceptions import Exx__Expected


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



        # ((EqValid_Raise(), EqValid_NotRaise(), ), LAMBDA_RAISE, [False, True]),
        # ((EqValid_NotRaise(), EqValid_Raise(), ), LAMBDA_RAISE, [False, True]),
        #
        # ((EqValid_NotRaise(), ), LAMBDA_RAISE, [False, False]),
        # ((EqValid_NotRaise(), ), 1, [True, True]),
        # ((EqValid_NotRaise(), EqValid_Raise()), 1, [False, True]),
        #
        # ((EqValid_NotRaise(), EqValid_GE(1)), 1, [True, True]),
        # ((EqValid_NotRaise(), EqValid_GE(100)), 1, [False, True]),
        # ((EqValid_NotRaise(), EqValid_GE(100, _iresult_reverse=True)), 1, [True, True]),
    ]
)
def test__RaiseIf(args, _EXPECTED):
    ExpectAux(RaiseIf_All(*args).resolve).check_assert(_EXPECTED[0])
    ExpectAux(RaiseIf_Any(*args).resolve).check_assert(_EXPECTED[1])


# =====================================================================================================================
