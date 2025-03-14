import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.base_statics.m3_primitives import *

from base_aux.aux_cmp_eq.m3_eq_valid1_base import _EqValidator

from base_aux.aux_cmp_eq.m3_eq_valid3_derivatives import *
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_kwargs import *


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
    ExpectAux(EqValid_VariantsDirect(*args) == other).check_assert(_EXPECTED[0])
    ExpectAux(EqValid_VariantsStrLow(*args) == other).check_assert(_EXPECTED[1])

    ExpectAux(EqValid_VariantsDirect(*args, reverse=True) == other).check_assert(not _EXPECTED[0])
    ExpectAux(EqValid_VariantsStrLow(*args, reverse=True) == other).check_assert(not _EXPECTED[1])

    # -----
    ExpectAux(other in EqValid_VariantsDirect(*args)).check_assert(_EXPECTED[0])
    ExpectAux(other in EqValid_VariantsStrLow(*args)).check_assert(_EXPECTED[1])

    ExpectAux(other in EqValid_VariantsDirect(*args, reverse=True)).check_assert(not _EXPECTED[0])
    ExpectAux(other in EqValid_VariantsStrLow(*args, reverse=True)).check_assert(not _EXPECTED[1])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ((bool, int), True, True),
        ((bool, int), 1, True),
        ((bool, int), 1.0, False),

        ((bool, int, None), 1, True),
        ((1, 2), 1, False),
    ]
)
def test__isinstance(args, other, _EXPECTED):
    ExpectAux(EqValid_Isinstance(*args) == other).check_assert(_EXPECTED)


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
        (False, (False, False, False, True, False)),
        (True, (True, False, False, True, False)),
        (1, (True, False, False, True, False)),
        (Exception, (False, True, False, True, True)),
        (Exception(), (False, True, False, True, True)),
        (LAMBDA_EXX, (False, True, False, True, True)),
        (LAMBDA_RAISE, (False, False, True, False, True)),
    ]
)
def test__exx_raise(other, _EXPECTED):
    ExpectAux(EqValid_True() == other).check_assert(_EXPECTED[0])
    ExpectAux(EqValid_Exx() == other).check_assert(_EXPECTED[1])
    ExpectAux(EqValid_Raise() == other).check_assert(_EXPECTED[2])
    ExpectAux(EqValid_NotRaise() == other).check_assert(_EXPECTED[3])
    ExpectAux(EqValid_ExxRaise() == other).check_assert(_EXPECTED[4])

    ExpectAux(EqValid_True(reverse=True) == other).check_assert(not _EXPECTED[0])
    ExpectAux(EqValid_Exx(reverse=True) == other).check_assert(not _EXPECTED[1])
    ExpectAux(EqValid_Raise(reverse=True) == other).check_assert(not _EXPECTED[2])
    ExpectAux(EqValid_NotRaise(reverse=True) == other).check_assert(not _EXPECTED[3])
    ExpectAux(EqValid_ExxRaise(reverse=True) == other).check_assert(not _EXPECTED[4])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXP_obj, _EXP_sn",
    argvalues=[
        # fails ------
        ((1,2), False, (False, False, False, False), (False, False, False, False)),
        ((1,2), Exception, (False, False, False, False), (False, False, False, False)),
        ((Exception, 2), 1, (False, False, False, False), (False, False, False, False)),

        # correct cmp ------
        ((1,2), 0, (False, False, False, False), (False, False, False, False)),
        ((1,2), 1, (False, False, True, True), (False, False, True, True)),
        ((1,2), 2, (False, True, False, True), (False, True, False, True)),
        ((1,2), 3, (False, False, False, False), (False, False, False, False)),

        ((1, 2), "a0c", (False, False, False, False), (False, False, False, False)),
        ((1, 2), "a1c", (False, False, False, False), (False, False, True, True)),
        ((1, 2), "a2c", (False, False, False, False), (False, True, False, True)),
        ((1, 2), "a3c", (False, False, False, False), (False, False, False, False)),
    ]
)
def test__lg(args, other, _EXP_obj, _EXP_sn):
    ExpectAux(EqValid_LtGt_Obj(*args) == other).check_assert(_EXP_obj[0])
    ExpectAux(EqValid_LtGe_Obj(*args) == other).check_assert(_EXP_obj[1])
    ExpectAux(EqValid_LeGt_Obj(*args) == other).check_assert(_EXP_obj[2])
    ExpectAux(EqValid_LeGe_Obj(*args) == other).check_assert(_EXP_obj[3])

    ExpectAux(EqValid_LtGt_Obj(*args, reverse=True) == other).check_assert(not _EXP_obj[0])
    ExpectAux(EqValid_LtGe_Obj(*args, reverse=True) == other).check_assert(not _EXP_obj[1])
    ExpectAux(EqValid_LeGt_Obj(*args, reverse=True) == other).check_assert(not _EXP_obj[2])
    ExpectAux(EqValid_LeGe_Obj(*args, reverse=True) == other).check_assert(not _EXP_obj[3])

    # ------
    ExpectAux(EqValid_LtGt_NumParsedSingle(*args) == other).check_assert(_EXP_sn[0])
    ExpectAux(EqValid_LtGe_NumParsedSingle(*args) == other).check_assert(_EXP_sn[1])
    ExpectAux(EqValid_LeGt_NumParsedSingle(*args) == other).check_assert(_EXP_sn[2])
    ExpectAux(EqValid_LeGe_NumParsedSingle(*args) == other).check_assert(_EXP_sn[3])

    ExpectAux(EqValid_LtGt_NumParsedSingle(*args, reverse=True) == other).check_assert(not _EXP_sn[0])
    ExpectAux(EqValid_LtGe_NumParsedSingle(*args, reverse=True) == other).check_assert(not _EXP_sn[1])
    ExpectAux(EqValid_LeGt_NumParsedSingle(*args, reverse=True) == other).check_assert(not _EXP_sn[2])
    ExpectAux(EqValid_LeGe_NumParsedSingle(*args, reverse=True) == other).check_assert(not _EXP_sn[3])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="other, expect, _EXPECTED",
    argvalues=[
        # TRASH ----
        (True, True, (False, False, False, )),
        (False, True, (False, False, False, )),
        (True, False, (True, False, False, )),
        (True, None, (True, False, False, )),
        ("", False, (True, False, False, )),

        # VALUES ----
        ("123", False, (False, True, False, )),
        ("123", True, (True, True, False, )),

        ("123", 1, (False, True, False, )),
        ("123", 123, (True, True, False, )),
        ("123", "123", (True, True, False, )),

        ("a123a", "b123b", (True, True, False, )),
        ("a1.2.3a", "b123b", (False, False, False, )),
        ("a1.2.3a", "hello", (True, False, False, )),

        ("a1.00a", "b001bb", (True, False, True, )),

        ("a111a", int, (True, True, False, )),
        ("a111a", float, (False, True, False, )),

        ("a11.22a", int, (False, False, True, )),
        ("a11.22a", float, (True, False, True, )),
    ]
)
def test__EqValid_NumParsedSingle(other, expect, _EXPECTED):
    ExpectAux(EqValid_NumParsedSingle(expect) == other).check_assert(_EXPECTED[0])

    ExpectAux(EqValid_NumParsedSingle_Int() == other).check_assert(_EXPECTED[1])
    ExpectAux(EqValid_NumParsedSingle_Float() == other).check_assert(_EXPECTED[2])


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
    ExpectAux(EqValid_Regexp(*args, bool_collect=Enum_BoolCumulate.ALL_TRUE) == other).check_assert(_EXPECTED[0])
    ExpectAux(EqValid_Regexp(*args, bool_collect=Enum_BoolCumulate.ANY_TRUE) == other).check_assert(_EXPECTED[1])
    ExpectAux(EqValid_Regexp(*args, bool_collect=Enum_BoolCumulate.ALL_FALSE) == other).check_assert(_EXPECTED[2])
    ExpectAux(EqValid_Regexp(*args, bool_collect=Enum_BoolCumulate.ANY_FALSE) == other).check_assert(_EXPECTED[3])

    ExpectAux(EqValid_RegexpAllTrue(*args) == other).check_assert(_EXPECTED[0])
    ExpectAux(EqValid_RegexpAnyTrue(*args) == other).check_assert(_EXPECTED[1])
    ExpectAux(EqValid_RegexpAllFalse(*args) == other).check_assert(_EXPECTED[2])
    ExpectAux(EqValid_RegexpAnyFalse(*args) == other).check_assert(_EXPECTED[3])

    ExpectAux(EqValid_RegexpAllTrue(*args, reverse=True) == other).check_assert(not _EXPECTED[0])
    ExpectAux(EqValid_RegexpAnyTrue(*args, reverse=True) == other).check_assert(not _EXPECTED[1])
    ExpectAux(EqValid_RegexpAllFalse(*args, reverse=True) == other).check_assert(not _EXPECTED[2])
    ExpectAux(EqValid_RegexpAnyFalse(*args, reverse=True) == other).check_assert(not _EXPECTED[3])


def test__regexp_manual():
    ExpectAux(EqValid_Regexp(r"\d+[.,]?\d*V") == "11.688889V").check_assert()


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, other, _EXPECTED",
    argvalues=[
        # (dict(a1=1), True, False),
        (dict(a1=1), dict(a1=11), False),
        (dict(a1=1), dict(a1=1), True),
        (dict(a1=1), dict(a1=1, b2=2), True),

        (dict(a1=1, a2=1), dict(a1=1), False),
        (dict(a1=1, a2=1), dict(A1=1, A2=1), True),
    ]
)
def test__AttrsByKwargs(source, other, _EXPECTED):
    ExpectAux(EqValid_AttrsByKwargs(**source) == NestInit_AnnotsAttrByKwArgs(**other)).check_assert(_EXPECTED)


@pytest.mark.parametrize(
    argnames="source, other, _EXPECTED",
    argvalues=[
        # OBVIOUS ------
        (dict(a1=1), dict(a1=11), (False, False)),
        (dict(a1=1), dict(a1=1), (True, True)),
        (dict(a1=1), dict(a1=1, b2=2), (True, True)),

        (dict(a1=1, a2=1), dict(a1=1), (False, False)),
        (dict(a1=1, a2=1), dict(A1=1, A2=1), (True, True)),

        # MESHED LEVELS ------
        (dict(a1=1, _a2=2), dict(a1=1), (False, True)),
    ]
)
def test__AttrsByObj(source, other, _EXPECTED):
    ExpectAux(
        EqValid_AttrsByObjNotPrivate(NestInit_AnnotsAttrByKwArgs(**source)) == NestInit_AnnotsAttrByKwArgs(**other)
    ).check_assert(_EXPECTED[0])
    ExpectAux(
        EqValid_AttrsByObjNotHidden(NestInit_AnnotsAttrByKwArgs(**source)) == NestInit_AnnotsAttrByKwArgs(**other)
    ).check_assert(_EXPECTED[1])


# =====================================================================================================================
