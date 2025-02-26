import pytest
from base_aux.aux_expect.m1_expect_aux import ExpectAux

from base_aux.base_statics.m3_primitives import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.aux_cmp_eq.m3_eq_valid3_derivatives import *
from base_aux.aux_cmp_eq.m1_cmp import *


# =====================================================================================================================
class Cls(NestCmp):
    def __init__(self, value):
        self.VALUE = value

    def __cmp__(self, other):
        other = Cls(other)
        if self.VALUE == other.VALUE:
            return 0
        if self.VALUE > other.VALUE:
            return 1
        if self.VALUE < other.VALUE:
            return -1


def test____LE__():
    func_link = lambda result: result == 1
    ExpectAux(func_link, Cls(1)).check_assert(True)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="func_link, args, kwargs, _EXPECTED, _pytestExpected",
    argvalues=[
        # not callable ------------
        (True, (), None, True, True),

        (True, 111, {"111": 222}, True, True),
        (True, 111, {"111": 222}, False, False),
        (True, 111, {"111": 222}, Exception, False),

        (False, (), {}, True, False),

        # callable ------------
        (LAMBDA_ECHO, (), {}, True, False),

        (LAMBDA_ECHO, None, {}, True, False),
        (LAMBDA_ECHO, None, {}, None, True),
        (LAMBDA_ECHO, True, {}, True, True),
        (LAMBDA_ECHO, (True, ), {}, True, True),
        (lambda value: value, (), {"value": True}, True, True),
        (lambda value: value, (), {"value": None}, True, False),
    ]
)
def test__pytest_func_tester(func_link, args, kwargs, _EXPECTED, _pytestExpected):
    try:
        ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)
    except:
        assert not _pytestExpected
    else:
        assert _pytestExpected


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, []),
        (None, {}, [None, ]),
        (1, {}, [1, ]),
        ((1, 1), {}, [1, 1]),

        ((1, 1), None, [1, 1]),
        ((1, 1), {}, [1, 1]),
        ((1, 1), {"2": 22}, [1, 1, "2"]),
        ((1, 1), {"2": 22, "3": 33}, [1, 1, "2", "3"]),
    ]
)
def test__func_list_direct(args, kwargs, _EXPECTED):
    func_link = LAMBDA_LIST_DIRECT
    ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, []),
        (None, {}, [None, ]),
        (1, {}, [1, ]),
        ((1, 1), {}, [1, 1]),

        ((1, 1), None, [1, 1]),
        ((1, 1), {}, [1, 1]),
        ((1, 1), {"2": 22}, [1, 1, 22]),
        ((1, 1), {"2": 22, "3": 33}, [1, 1, 22, 33]),
    ]
)
def test__func_list_values(args, kwargs, _EXPECTED):
    func_link = LAMBDA_LIST_VALUES
    ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, {}),
        (None, {}, {None: None}),
        (1, {}, {1: None}),
        ((1, 1), {}, {1: None}),

        ((1, 1), None, {1: None}),
        ((1, 1), {}, {1: None}),
        ((1, 1), {"2": 22}, {1: None, "2": 22}),
        ((1, 1), {"2": 22, "3": 33}, {1: None, "2": 22, "3": 33}),
    ]
)
def test__func_dict(args, kwargs, _EXPECTED):
    func_link = LAMBDA_DICT
    ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, True),
        (None, {}, False),
        (1, {}, True),
        ((1, 1), {}, True),

        ((1, 1), None, True),
        ((1, 1), {}, True),
        ((1, 1), {"2": 22}, True),
        ((1, 1), {"2": 22, "3": 33}, True),

        ((1, 1), {"2": 22, "3": None}, False),
    ]
)
def test__func_all(args, kwargs, _EXPECTED):
    func_link = LAMBDA_ALL
    ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, False),
        (None, {}, False),
        (1, {}, True),
        ((1, 1), {}, True),

        ((1, 1), None, True),
        ((1, 1), {}, True),
        ((1, 1), {"2": 22}, True),
        ((1, 1), {"2": 22, "3": 33}, True),

        ((1, 1), {"2": 22, "3": None}, True),
        ((1, None), {"2": 22, "3": None}, True),
        ((None, None), {"2": True, "3": None}, True),
        ((None, None), {"2": False, "3": None}, False),

        (Args(None, None), {"2": False, "3": None}, False),
    ]
)
def test__func_any(args, kwargs, _EXPECTED):
    func_link = LAMBDA_ANY
    ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="source, other, _EXPECTED",
    argvalues=[
        ("11.688889V", EqValid_Regexp(r"\d+[.,]?\d*V"), True),
        (INST_EQ_TRUE, INST_EQ_TRUE, True),
        (INST_EQ_TRUE, INST_EQ_FALSE, True),
        (INST_EQ_FALSE, INST_EQ_TRUE, True),
        (INST_EQ_FALSE, INST_EQ_FALSE, False),
    ]
)
def test__EQ(source, other, _EXPECTED):
    assert ExpectAux(source).check_bool(other) == _EXPECTED


# =====================================================================================================================
