import pytest

from base_aux.aux_argskwargs.m4_kwargs_eq_expect import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m3_exceptions import *
from base_aux.base_values.m4_primitives import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="other_draft, eq_kwargs, eq_expects, _EXPECTED",
    argvalues=[
        # SINGLE =============================================
        # no expected -------
        (1, dict(eq1=1), dict(), [True, True, False, False]),
        (1, dict(eq1=EqValid_EQ(1)), dict(), [True, True, False, False]),
        (1, dict(eq1=11), dict(), [False, False, True, True]),
        (1, dict(eq1=EqValid_EQ(11)), dict(), [False, False, True, True]),
        (lambda: 1, dict(eq1=1), dict(), [True, True, False, False]),

        # expected -------
        (1, dict(eq1=1), dict(eq1=True), [True, True, False, False]),
        (1, dict(eq1=1), dict(eq1=False), [False, False, True, True]),

        # RAISED --------
        (1, dict(eq1=1), dict(eq111=True), [Exx__WrongUsage, Exx__WrongUsage, Exx__WrongUsage, Exx__WrongUsage]),

        (1, dict(eq1=ClsEqRaise()), dict(), [False, False, True, True]),
        (1, dict(eq1=ClsEqRaise()), dict(eq1=Exception), [True, True, False, False]),
        (LAMBDA_RAISE, dict(eq1=1), dict(), [False, False, True, True]),
        (LAMBDA_RAISE, dict(eq1=1), dict(eq1=Exception), [False, False, True, True]),  # FIXME: CAREFUL!!! INCORRECT!!!!
        (LAMBDA_RAISE, dict(eq1=Exception), dict(eq1=Exception), [False, False, True, True]),   # FIXME: CAREFUL!!! INCORRECT!!!!

        # MULTY =============================================
        (1, dict(eq1=1, eq2=11), dict(), [False, True, False, True]),
        (1, dict(eq1=1, eq2=11), dict(eq1=True, eq2=True), [False, True, False, True]),

        (1, dict(eq1=1, eq2=11), dict(eq1=True), [True, True, False, False]),
        (1, dict(eq1=1, eq2=11), dict(eq1=True, eq2=False), [True, True, False, False]),
    ]
)
def test__base_eq_kwargs(other_draft, eq_kwargs, eq_expects, _EXPECTED):
    Victim = Base_KwargsEqExpect
    Lambda(Victim(other_draft, **eq_kwargs).bool_if__all_true, **eq_expects).expect__check_assert(_EXPECTED[0])
    Lambda(Victim(other_draft, **eq_kwargs).bool_if__any_true, **eq_expects).expect__check_assert(_EXPECTED[1])
    Lambda(Victim(other_draft, **eq_kwargs).bool_if__all_false, **eq_expects).expect__check_assert(_EXPECTED[2])
    Lambda(Victim(other_draft, **eq_kwargs).bool_if__any_false, **eq_expects).expect__check_assert(_EXPECTED[3])

    Lambda(Victim(other_draft, **eq_kwargs).raise_if__all_true, **eq_expects).expect__check_assert(Exception if _EXPECTED[0] else False)
    Lambda(Victim(other_draft, **eq_kwargs).raise_if__any_true, **eq_expects).expect__check_assert(Exception if _EXPECTED[1] else False)
    Lambda(Victim(other_draft, **eq_kwargs).raise_if__all_false, **eq_expects).expect__check_assert(Exception if _EXPECTED[2] else False)
    Lambda(Victim(other_draft, **eq_kwargs).raise_if__any_false, **eq_expects).expect__check_assert(Exception if _EXPECTED[3] else False)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="other_draft, eq_expects, _EXP_checkIf, _EXP_ga",
    argvalues=[
        ("linux", dict(linux=True), [True, True, False, False], [True, False]),
        ("LINux", dict(linUX=True), [True, True, False, False], [True, False]),
        (lambda: "LINux", dict(linUX=True), [True, True, False, False], [True, False]),

        ("windows", dict(linux=True), [False, False, True, True], [False, True]),
        ("windows", dict(linux=True, windows=True), [False, True, False, True], [False, True]),
        ("Windows", dict(linux=True, windows=True), [False, True, False, True], [False, True]),

    ]
)
def test__OS(other_draft, eq_expects, _EXP_checkIf, _EXP_ga):
    Victim = KwargsEqExpect_OS
    Lambda(Victim(other_draft).bool_if__all_true, **eq_expects).expect__check_assert(_EXP_checkIf[0])
    Lambda(Victim(other_draft).bool_if__any_true, **eq_expects).expect__check_assert(_EXP_checkIf[1])
    Lambda(Victim(other_draft).bool_if__all_false, **eq_expects).expect__check_assert(_EXP_checkIf[2])
    Lambda(Victim(other_draft).bool_if__any_false, **eq_expects).expect__check_assert(_EXP_checkIf[3])

    Lambda(Victim(other_draft).raise_if__all_true, **eq_expects).expect__check_assert(Exx__Expected if _EXP_checkIf[0] else False)
    Lambda(Victim(other_draft).raise_if__any_true, **eq_expects).expect__check_assert(Exx__Expected if _EXP_checkIf[1] else False)
    Lambda(Victim(other_draft).raise_if__all_false, **eq_expects).expect__check_assert(Exx__Expected if _EXP_checkIf[2] else False)
    Lambda(Victim(other_draft).raise_if__any_false, **eq_expects).expect__check_assert(Exx__Expected if _EXP_checkIf[3] else False)

    # GA
    Lambda(lambda: Victim(other_draft).linux).expect__check_assert(_EXP_ga[0])
    Lambda(lambda: Victim(other_draft).LINUX).expect__check_assert(_EXP_ga[0])
    Lambda(lambda: Victim(other_draft).windows).expect__check_assert(_EXP_ga[1])
    Lambda(lambda: Victim(other_draft).WINDOWS).expect__check_assert(_EXP_ga[1])
    Lambda(lambda: Victim(other_draft).HELLO).expect__check_assert(Exception)


def test__os_2():
    if platform.system().lower() == "windows":
        assert KwargsEqExpect_OS().bool_if__any_true(windows=True)
    else:
        assert not KwargsEqExpect_OS().bool_if__any_true(windows=True)


# =====================================================================================================================
