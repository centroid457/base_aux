import pytest

from base_aux.aux_types.m0_primitives import *
from base_aux.aux_argskwargs.m1_argskwargs import *

from base_aux.aux_pytester.m1_pytest_aux import PytestAux

from base_aux.cmp.m1_cmp import CmpInst


# =====================================================================================================================
class Cls(CmpInst):
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
    PytestAux(func_link, Cls(1)).assert_check(True)


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
        PytestAux(func_link, args, kwargs).assert_check(_EXPECTED)
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
    PytestAux(func_link, args, kwargs).assert_check(_EXPECTED)


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
    PytestAux(func_link, args, kwargs).assert_check(_EXPECTED)


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
    PytestAux(func_link, args, kwargs).assert_check(_EXPECTED)


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
    PytestAux(func_link, args, kwargs).assert_check(_EXPECTED)


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
    PytestAux(func_link, args, kwargs).assert_check(_EXPECTED)


# =====================================================================================================================
