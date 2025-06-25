import pytest

from base_aux.lambdas.m1_lambda import *
from base_aux.aux_values.m6_value_valid1_eq import *
from base_aux.aux_eq.m4_eq_valid_chain import *
from base_aux.aux_values.m4_primitives import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, eq, _EXPECTED",
    argvalues=[
        (LAMBDA_RAISE, NoValue, None),
        (1, NoValue, None),

        (1, EqValid_GE(1), None),
        (1, EqValid_GE(2), Exception),

        (1, EqValid_EQ(1), None),
        (1, EqValid_EQ(2), Exception),
    ]
)
def test__1_init(source, eq, _EXPECTED):
    if _EXPECTED is None:
        _EXPECTED = source
        # here it will be compared with source or Exception!

    func_link = ValueEqValid
    Lambda(func_link, source, eq).expect__check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="source, eq, new, _EXPECTED",
    argvalues=[
        (LAMBDA_RAISE, NoValue, 10, True),
        (1, NoValue, 10, True),

        (1, EqValid_GE(1), 10, True),
        (1, EqValid_GE(1), 0, Exception),

        (1, EqValid_EQ(1), 10, Exception),
        (1, EqValid_EQ(1, 10), 10, True),
    ]
)
def test__2_reset(source, eq, new, _EXPECTED):
    func_link = ValueEqValid(source, eq).value_update
    Lambda(func_link, new).expect__check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="source, eq, other, _EXPECTED",
    argvalues=[
        (1, NoValue, 1, True),
        (1, NoValue, 10, False),

        (1, EqValid_GE(1), 1, True),
        (1, EqValid_GE(1), 10, False),
        (1, EqValid_GE(1), 0, False),

        (1, EqValid_EQ(1), 10, False),
        (1, EqValid_EQ(1, 10), 10, False),
    ]
)
def test__3_eq(source, eq, other, _EXPECTED):
    func_link = ValueEqValid(source, eq) == other
    Lambda(func_link).expect__check_assert(_EXPECTED)


# =====================================================================================================================
