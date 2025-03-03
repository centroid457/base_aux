import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_values.m1_value_valid_eq import *
from base_aux.aux_cmp_eq.m4_eq_valid_chain import *
from base_aux.base_statics.m3_primitives import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, eq, _EXPECTED",
    argvalues=[
        (LAMBDA_RAISE, NoValue, None),
        (1, NoValue, None),

        (1, EqValid_LeGe_Obj(1), None),
        (1, EqValid_LeGe_Obj(2), Exception),

        (1, EqValid_VariantsDirect(1), None),
        (1, EqValid_VariantsDirect(2), Exception),
    ]
)
def test__1_init(source, eq, _EXPECTED):
    if _EXPECTED is None:
        _EXPECTED = source
        # here it will be compared with source or Exception!

    func_link = ValueEqValid
    ExpectAux(func_link, (source, eq)).check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="source, eq, new, _EXPECTED",
    argvalues=[
        (LAMBDA_RAISE, NoValue, 10, True),
        (1, NoValue, 10, True),

        (1, EqValid_LeGe_Obj(1), 10, True),
        (1, EqValid_LeGe_Obj(1), 0, Exception),

        (1, EqValid_VariantsDirect(1), 10, Exception),
        (1, EqValid_VariantsDirect(1, 10), 10, True),
    ]
)
def test__2_reset(source, eq, new, _EXPECTED):
    func_link = ValueEqValid(source, eq).reset
    ExpectAux(func_link, new).check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="source, eq, other, _EXPECTED",
    argvalues=[
        (1, NoValue, 1, True),
        (1, NoValue, 10, False),

        (1, EqValid_LeGe_Obj(1), 1, True),
        (1, EqValid_LeGe_Obj(1), 10, False),
        (1, EqValid_LeGe_Obj(1), 0, False),

        (1, EqValid_VariantsDirect(1), 10, False),
        (1, EqValid_VariantsDirect(1, 10), 10, False),
    ]
)
def test__3_eq(source, eq, other, _EXPECTED):
    func_link = ValueEqValid(source, eq) == other
    ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
