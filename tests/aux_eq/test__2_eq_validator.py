import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_types.m0_primitives import *

from base_aux.aux_eq.m2_eq_validator import _EqValidator
from base_aux.aux_eq.m2_eq_validator import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, other, _EXPECTED",
    argvalues=[
        (bool, None, False),
        (bool, 0, False),
        (bool, 1, True),
        (bool, 2, True),
        (bool, LAMBDA_TRUE, True),
        (bool, LAMBDA_FALSE, False),
    ]
)
def test___EqValidator(source, other, _EXPECTED):
    ExpectAux(_EqValidator(source) == other).check_assert(_EXPECTED)
    ExpectAux(_EqValidator(source, reverse=True) == other).check_assert(not _EXPECTED)

    ExpectAux(other in _EqValidator(source)).check_assert(_EXPECTED)
    ExpectAux(other in _EqValidator(source, reverse=True)).check_assert(not _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ([1,2], 1, (True, True)),
        ([1,2], "1", (False, True)),
        ([1,2], 10, (False, False)),
        ([*"12"], "1", (True, True)),
        ([*"12"], "10", (False, False)),
        ([*"12"], "hello", (False, False)),

        ([*"ABC"], "A", (True, True)),
        ([*"ABC"], "a", (False, True)),
        ([*"ABC"], "f", (False, False)),
    ]
)
def test__variants(args, other, _EXPECTED):
    ExpectAux(EqValid_Variants(*args) == other).check_assert(_EXPECTED[0])
    ExpectAux(EqValid_VariantsStrLow(*args) == other).check_assert(_EXPECTED[1])

    ExpectAux(EqValid_Variants(*args, reverse=True) == other).check_assert(not _EXPECTED[0])
    ExpectAux(EqValid_VariantsStrLow(*args, reverse=True) == other).check_assert(not _EXPECTED[1])


    ExpectAux(other in EqValid_Variants(*args)).check_assert(_EXPECTED[0])
    ExpectAux(other in EqValid_VariantsStrLow(*args)).check_assert(_EXPECTED[1])

    ExpectAux(other in EqValid_Variants(*args, reverse=True)).check_assert(not _EXPECTED[0])
    ExpectAux(other in EqValid_VariantsStrLow(*args, reverse=True)).check_assert(not _EXPECTED[1])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, ic, _EXPECTED",
    argvalues=[
        ([*"ABC"], "A1", True, True),
        ([*"ABC"], "A1", False, True),

        ([*"ABC"], "a1", True, True),
        ([*"ABC"], "a1", False, False),

        ([*"ABC"], "f1", True, False),
        ([*"ABC"], "f1", False, False),
    ]
)
def test__startswith(args, other, ic, _EXPECTED):
    ExpectAux(EqValid_Startswith(*args, ignorecase=ic) == other).check_assert(_EXPECTED)
    ExpectAux(EqValid_Startswith(*args, reverse=True, ignorecase=ic) == other).check_assert(not _EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, other, ic, _EXPECTED",
    argvalues=[
        ([*"ABC"], "1A", True, True),
        ([*"ABC"], "1A", False, True),

        ([*"ABC"], "1a", True, True),
        ([*"ABC"], "1a", False, False),

        ([*"ABC"], "1f", True, False),
        ([*"ABC"], "1f", False, False),
    ]
)
def test__endswith(args, other, ic, _EXPECTED):
    ExpectAux(EqValid_Endswith(*args, ignorecase=ic) == other).check_assert(_EXPECTED)
    ExpectAux(EqValid_Endswith(*args, reverse=True, ignorecase=ic) == other).check_assert(not _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="other, _EXPECTED",
    argvalues=[
        (False, (False, False, True, False)),
        (True, (False, False, True, False)),
        (1, (False, False, True, False)),
        (Exception, (True, False, True, True)),
        (Exception(), (True, False, True, True)),
        (LAMBDA_EXX, (True, False, True, True)),
        (LAMBDA_RAISE, (False, True, False, True)),
    ]
)
def test__exx_raise(other, _EXPECTED):
    ExpectAux(EqValid_Exx() == other).check_assert(_EXPECTED[0])
    ExpectAux(EqValid_Raise() == other).check_assert(_EXPECTED[1])
    ExpectAux(EqValid_NotRaise() == other).check_assert(_EXPECTED[2])
    ExpectAux(EqValid_ExxRaised() == other).check_assert(_EXPECTED[3])

    ExpectAux(EqValid_Exx(reverse=True) == other).check_assert(not _EXPECTED[0])
    ExpectAux(EqValid_Raise(reverse=True) == other).check_assert(not _EXPECTED[1])
    ExpectAux(EqValid_NotRaise(reverse=True) == other).check_assert(not _EXPECTED[2])
    ExpectAux(EqValid_ExxRaised(reverse=True) == other).check_assert(not _EXPECTED[3])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ((1,2), False, (False, False, False, False)),
        ((1,2), Exception, (False, False, False, False)),
        ((Exception,2), 1, (False, False, False, False)),

        ((1,2), 0, (False, False, False, False)),
        ((1,2), 1, (False, False, True, True)),
        ((1,2), 2, (False, True, False, True)),
        ((1,2), 3, (False, False, False, False)),
    ]
)
def test__lg(args, other, _EXPECTED):
    ExpectAux(EqValid_LtGt(*args) == other).check_assert(_EXPECTED[0])
    ExpectAux(EqValid_LtGe(*args) == other).check_assert(_EXPECTED[1])
    ExpectAux(EqValid_LeGt(*args) == other).check_assert(_EXPECTED[2])
    ExpectAux(EqValid_LeGe(*args) == other).check_assert(_EXPECTED[3])

    ExpectAux(EqValid_LtGt(*args, reverse=True) == other).check_assert(not _EXPECTED[0])
    ExpectAux(EqValid_LtGe(*args, reverse=True) == other).check_assert(not _EXPECTED[1])
    ExpectAux(EqValid_LeGt(*args, reverse=True) == other).check_assert(not _EXPECTED[2])
    ExpectAux(EqValid_LeGe(*args, reverse=True) == other).check_assert(not _EXPECTED[3])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ((r"\d", ), 1, (True, True, False, False)),
        ((r"\d\d", ), 1, (False, False, True, True)),
        ((r"\d", r"\d\d", ), 1, (False, True, False, True)),

        ((r"\d\d",), LAMBDA_RAISE, (False, False, True, True)),
        ((r"\d\d",), LAMBDA_EXX, (False, False, True, True)),

        ((r"true",), "Tr", (False, False, True, True)),
        ((r"true",), "True", (True, True, False, False)),
        ((r"true",), LAMBDA_TRUE, (True, True, False, False)),
    ]
)
def test__regexp(args, other, _EXPECTED):
    ExpectAux(EqValid_Regexp(*args, bool_collect=BoolCollect.ALL_TRUE) == other).check_assert(_EXPECTED[0])
    ExpectAux(EqValid_Regexp(*args, bool_collect=BoolCollect.ANY_TRUE) == other).check_assert(_EXPECTED[1])
    ExpectAux(EqValid_Regexp(*args, bool_collect=BoolCollect.ALL_FALSE) == other).check_assert(_EXPECTED[2])
    ExpectAux(EqValid_Regexp(*args, bool_collect=BoolCollect.ANY_FALSE) == other).check_assert(_EXPECTED[3])

    ExpectAux(EqValid_RegexpAllTrue(*args) == other).check_assert(_EXPECTED[0])
    ExpectAux(EqValid_RegexpAnyTrue(*args) == other).check_assert(_EXPECTED[1])
    ExpectAux(EqValid_RegexpAllFalse(*args) == other).check_assert(_EXPECTED[2])
    ExpectAux(EqValid_RegexpAnyFalse(*args) == other).check_assert(_EXPECTED[3])

    ExpectAux(EqValid_RegexpAllTrue(*args, reverse=True) == other).check_assert(not _EXPECTED[0])
    ExpectAux(EqValid_RegexpAnyTrue(*args, reverse=True) == other).check_assert(not _EXPECTED[1])
    ExpectAux(EqValid_RegexpAllFalse(*args, reverse=True) == other).check_assert(not _EXPECTED[2])
    ExpectAux(EqValid_RegexpAnyFalse(*args, reverse=True) == other).check_assert(not _EXPECTED[3])


# =====================================================================================================================
