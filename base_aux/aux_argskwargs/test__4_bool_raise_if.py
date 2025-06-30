from base_aux.base_values.m4_primitives import *

from base_aux.aux_argskwargs.m5_bool_raise_if import *
from base_aux.base_values.m3_exceptions import Exx__Expected


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        # SINGLE ---
        ((False,), [False, False, True, True]),
        ((None,), [False, False, True, True]),
        ((True,), [True, True, False, False]),

        ((0,), [False, False, True, True]),
        ((1,), [True, True, False, False]),

        ((Exception, ), [False, False, True, True]),

        ((LAMBDA_FALSE,), [False, False, True, True]),
        ((LAMBDA_NONE,), [False, False, True, True]),
        ((LAMBDA_TRUE,), [True, True, False, False]),
        ((LAMBDA_RAISE,), [False, False, True, True]),
        ((LAMBDA_EXX,), [False, False, True, True]),

        # SEVERAL ---
        ((0, 1,), [False, True, False, True]),
        ((LAMBDA_RAISE, 1,), [False, True, False, True]),
    ]
)
def test__RaiseIf(args, _EXPECTED):
    Lambda(ArgsBoolIf_AllTrue(*args).resolve).expect__check_assert(_EXPECTED[0])
    Lambda(ArgsBoolIf_AnyTrue(*args).resolve).expect__check_assert(_EXPECTED[1])
    Lambda(ArgsBoolIf_AllFalse(*args).resolve).expect__check_assert(_EXPECTED[2])
    Lambda(ArgsBoolIf_AnyFalse(*args).resolve).expect__check_assert(_EXPECTED[3])

    Lambda(ArgsRaiseIf_AllTrue(*args).resolve).expect__check_assert(Exx__Expected if _EXPECTED[0] else False)
    Lambda(ArgsRaiseIf_AnyTrue(*args).resolve).expect__check_assert(Exx__Expected if _EXPECTED[1] else False)
    Lambda(ArgsRaiseIf_AllFalse(*args).resolve).expect__check_assert(Exx__Expected if _EXPECTED[2] else False)
    Lambda(ArgsRaiseIf_AnyFalse(*args).resolve).expect__check_assert(Exx__Expected if _EXPECTED[3] else False)


# =====================================================================================================================
