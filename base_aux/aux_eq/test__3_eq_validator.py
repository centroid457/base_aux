import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_values.m4_primitives import *

from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_kwargs import *


# =====================================================================================================================
def _ExpectAux__eq_in__all_operators(eq_cls: type[Base_EqValid], args, other, _EXPECTED) -> None | NoReturn:
    """
    GOAL
    ----
    check one EqClass by 4 variant lines
    """
    ExpectAux(eq_cls(*args) == other).check_assert(_EXPECTED)
    # ExpectAux(eq_cls(*args, _iresult_reverse=True) == other).check_assert(not _EXPECTED)

    ExpectAux(other in eq_cls(*args)).check_assert(_EXPECTED)
    # ExpectAux(other in eq_cls(*args, _iresult_reverse=True)).check_assert(not _EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
def test__0_EqValidObj__usage_operators():
    assert 1 == EqValid_BoolTrue()
    assert 1 in EqValid_BoolTrue()
    assert 0 not in EqValid_BoolTrue()

    assert 1 in [0, 1]
    assert 1 in [0, EqValid_BoolTrue()]

    assert 0 in [0, EqValid_BoolTrue()]
    assert 0 not in [1, EqValid_BoolTrue()]


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="_validator, other, _EXPECTED",
    argvalues=[
        (bool, None, False),
        (bool, 0, False),
        (bool, 1, True),
        (bool, 2, True),
        (bool, LAMBDA_TRUE, True),
        (bool, LAMBDA_FALSE, False),
    ]
)
def test__0_Base_EqValid__single(_validator, other, _EXPECTED):
    ExpectAux(Base_EqValid(_validator=_validator) == other).check_assert(_EXPECTED)
    ExpectAux(Base_EqValid(_validator=_validator, _iresult_reverse=True) == other).check_assert(not _EXPECTED)

    ExpectAux(other in Base_EqValid(_validator=_validator)).check_assert(_EXPECTED)
    ExpectAux(other in Base_EqValid(_validator=_validator, _iresult_reverse=True)).check_assert(not _EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
def _victim_validator(source, arg) -> bool:
    return source == arg


@pytest.mark.parametrize(
    argnames="_validator, other, args, _EXPECTED",
    argvalues=[
        # ALL True ----
        (_victim_validator, 1, [1, 1], [True, True, False, False]),
        (_victim_validator, LAMBDA_1, [1, 1], [True, True, False, False]),

        # # ALL False ----
        (_victim_validator, 0, [1, 1], [False, False, True, True]),
        (_victim_validator, LAMBDA_0, [1, 1], [False, False, True, True]),
    ]
)
def test__0_Base_EqValid__args_cumulate_1__ALL(_validator, other, args, _EXPECTED):
    for index, _iresult_cumulate in enumerate(Enum_BoolCumulate):
        print()
        print(index, _iresult_cumulate)
        ExpectAux(Base_EqValid(*args, _validator=_validator, _iresult_cumulate=_iresult_cumulate) == other).check_assert(_EXPECTED[index])
        ExpectAux(Base_EqValid(*args, _validator=_validator, _iresult_cumulate=_iresult_cumulate, _iresult_reverse=True) == other).check_assert(not _EXPECTED[index])

        ExpectAux(other in Base_EqValid(*args, _validator=_validator, _iresult_cumulate=_iresult_cumulate)).check_assert(_EXPECTED[index])
        ExpectAux(other in Base_EqValid(*args, _validator=_validator, _iresult_cumulate=_iresult_cumulate, _iresult_reverse=True)).check_assert(not _EXPECTED[index])


@pytest.mark.parametrize(
    argnames="_validator, other, args, _iresult_cumulate, _EXPECTED",
    argvalues=[
        # [direct, reverse]
        # ALL True ----
        (_victim_validator, 1, [1, 1], Enum_BoolCumulate.ANY_TRUE, [True, False]),
        (_victim_validator, 1, [1, 1], Enum_BoolCumulate.ANY_FALSE, [False, True]),

        # # ALL False ----
        (_victim_validator, 0, [1, 1], Enum_BoolCumulate.ANY_TRUE, [False, True]),
        (_victim_validator, 0, [1, 1], Enum_BoolCumulate.ANY_FALSE, [True, False]),

        # ANY
        (_victim_validator, 1, [0, 1], Enum_BoolCumulate.ANY_TRUE, [True, True]),
        (_victim_validator, 1, [0, 1], Enum_BoolCumulate.ANY_FALSE, [True, True]),
    ]
)
def test__0_Base_EqValid__args_cumulate_2__ANY(_validator, other, args, _iresult_cumulate, _EXPECTED):
    ExpectAux(Base_EqValid(*args, _validator=_validator, _iresult_cumulate=_iresult_cumulate) == other).check_assert(_EXPECTED[0])
    ExpectAux(Base_EqValid(*args, _validator=_validator, _iresult_cumulate=_iresult_cumulate, _iresult_reverse=True) == other).check_assert(_EXPECTED[1])

    ExpectAux(other in Base_EqValid(*args, _validator=_validator, _iresult_cumulate=_iresult_cumulate)).check_assert(_EXPECTED[0])
    ExpectAux(other in Base_EqValid(*args, _validator=_validator, _iresult_cumulate=_iresult_cumulate, _iresult_reverse=True)).check_assert(_EXPECTED[1])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ((bool, int), True, True),
        ((bool, int), 1, True),
        ((bool, int), 1.0, False),

        ((bool, int, None), 1, True),
        ((1, 2), 1, True),
    ]
)
def test__isinstance(args, other, _EXPECTED):
    _ExpectAux__eq_in__all_operators(EqValid_IsinstanceSameinstance, args, other, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ([1,2], 1, (False, True)),
        ([1,2], "1", (False, True)),
        ([1,2], 10, (False, True)),
        ([*"12"], "1", (True, True)),
        ([*"12"], "10", (True, True)),
        ([*"12"], "hello", (False, False)),

        ([*"ABC"], "A", (True, True)),
        ([*"ABC"], "a", (False, True)),
        ([*"ABC"], "f", (False, False)),
    ]
)
def test__contains(args, other, _EXPECTED):
    _ExpectAux__eq_in__all_operators(EqValid_Contain, args, other, _EXPECTED[0])
    _ExpectAux__eq_in__all_operators(EqValid_ContainStrIc, args, other, _EXPECTED[1])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ([*"ABC"], "A1", (True, True)),
        ([*"ABC"], "a1", (False, True)),
        ([*"ABC"], "f1", (False, False)),
    ]
)
def test__startswith(args, other, _EXPECTED):
    _ExpectAux__eq_in__all_operators(EqValid_Startswith, args, other, _EXPECTED[0])
    _ExpectAux__eq_in__all_operators(EqValid_StartswithIc, args, other, _EXPECTED[1])


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ([*"ABC"], "1A", (True, True)),
        ([*"ABC"], "1a", (False, True)),
        ([*"ABC"], "1f", (False, False)),
    ]
)
def test__endswith(args, other, _EXPECTED):
    _ExpectAux__eq_in__all_operators(EqValid_Endswith, args, other, _EXPECTED[0])
    _ExpectAux__eq_in__all_operators(EqValid_EndswithIc, args, other, _EXPECTED[1])


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
def test__bool_exx_raise(other, _EXPECTED):
    args = ()
    _ExpectAux__eq_in__all_operators(EqValid_BoolTrue, args, other, _EXPECTED[0])
    _ExpectAux__eq_in__all_operators(EqValid_Exx, args, other, _EXPECTED[1])
    _ExpectAux__eq_in__all_operators(EqValid_Raise, args, other, _EXPECTED[2])
    _ExpectAux__eq_in__all_operators(EqValid_NotRaise, args, other, _EXPECTED[3])
    _ExpectAux__eq_in__all_operators(EqValid_ExxRaise, args, other, _EXPECTED[4])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, other, _EXPECTED",
    argvalues=[
        ([1, 2], 1, (True, True, True)),
        ([1, 2], "1", (False, True, True)),
        ([1, 2], 10, (False, False, False)),
        ([*"12"], "1", (True, True, False)),
        ([*"12"], "10", (False, False, False)),
        ([*"12"], "hello", (False, False, False)),

        ([*"ABC"], "A", (True, True, False)),
        ([*"ABC"], "a", (False, True, False)),
        ([*"ABC"], "f", (False, False, False)),
    ]
)
def test__EQ(args, other, _EXPECTED):
    _ExpectAux__eq_in__all_operators(EqValid_EQ, args, other, _EXPECTED[0])
    _ExpectAux__eq_in__all_operators(EqValid_EQ_StrIc, args, other, _EXPECTED[1])
    _ExpectAux__eq_in__all_operators(EqValid_EQ_NumParsedSingle, args, other, _EXPECTED[2])


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, other, _EXP_obj, _EXP_num",
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
def test__LGTE(args, other, _EXP_obj, _EXP_num):
    _ExpectAux__eq_in__all_operators(EqValid_LGTE, args, other, _EXP_obj[0])
    # FIXME: FINISH!!!
    # FIXME: FINISH!!!
    # FIXME: FINISH!!!
    # FIXME: FINISH!!!
    # FIXME: FINISH!!!
    # FIXME: FINISH!!!

    # ------
    _ExpectAux__eq_in__all_operators(EqValid_LGTE_NumParsedSingle, args, other, _EXP_num[0])
    # FIXME: FINISH!!!
    # FIXME: FINISH!!!
    # FIXME: FINISH!!!
    # FIXME: FINISH!!!
    # FIXME: FINISH!!!
    # FIXME: FINISH!!!

# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="other, value, _EXPECTED",
    argvalues=[
        # TRASH ----
        (True, True, (False, False, False, False)),
        (True, None, (False, True, False, False)),
        (True, 1, (False, False, False, False)),
        ("", False, (False, False, False, False)),

        # # VALUES ----
        ("123", False, (True, False, True, False)),
        ("123", 1, (True, False, True, False)),
        ("123", 123, (True, True, True, False)),
        ("123", "123", (True, False, True, False)),

        ("a123a", "b123b", (True, False, True, False,)),
        ("a123a", 123, (True, True, True, False,)),
        ("a123a", 1, (True, False, True, False,)),

        ("a1.2.3a", "b123b", (False, False, False, False, )),
        ("a1.2.3a", "hello", (False, False, False, False, )),

        ("a1.00a", "b001bb", (True, False, False, True, )),
    ]
)
def test__EqValid_NumParsedSingle(other, value, _EXPECTED):
    _ExpectAux__eq_in__all_operators(EqValid_NumParsedSingle_Sucess, (), other, _EXPECTED[0])
    _ExpectAux__eq_in__all_operators(EqValid_NumParsedSingle_EQ, (value, ), other, _EXPECTED[1])
    _ExpectAux__eq_in__all_operators(EqValid_EQ_NumParsedSingle, (value, ), other, _EXPECTED[1])
    _ExpectAux__eq_in__all_operators(EqValid_NumParsedSingle_TypeInt, (), other, _EXPECTED[2])
    _ExpectAux__eq_in__all_operators(EqValid_NumParsedSingle_TypeFloat, (), other, _EXPECTED[3])


# ---------------------------------------------------------------------------------------------------------------------
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
    ExpectAux(EqValid_Regexp(*args, _iresult_cumulate=Enum_BoolCumulate.ALL_TRUE) == other).check_assert(_EXPECTED[0])
    ExpectAux(EqValid_Regexp(*args, _iresult_cumulate=Enum_BoolCumulate.ANY_TRUE) == other).check_assert(_EXPECTED[1])
    ExpectAux(EqValid_Regexp(*args, _iresult_cumulate=Enum_BoolCumulate.ALL_FALSE) == other).check_assert(_EXPECTED[2])
    ExpectAux(EqValid_Regexp(*args, _iresult_cumulate=Enum_BoolCumulate.ANY_FALSE) == other).check_assert(_EXPECTED[3])

    # ---------
    _ExpectAux__eq_in__all_operators(EqValid_RegexpAllTrue, args, other, _EXPECTED[0])
    _ExpectAux__eq_in__all_operators(EqValid_RegexpAnyTrue, args, other, _EXPECTED[1])
    _ExpectAux__eq_in__all_operators(EqValid_RegexpAllFalse, args, other, _EXPECTED[2])
    _ExpectAux__eq_in__all_operators(EqValid_RegexpAnyFalse, args, other, _EXPECTED[3])


def test__regexp_manual():
    ExpectAux(EqValid_Regexp(r"\d+[.,]?\d*V") == "11.688889V").check_assert()


# ---------------------------------------------------------------------------------------------------------------------
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
