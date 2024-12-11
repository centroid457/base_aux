import pytest
from typing import *

from base_aux.base_argskwargs import *

from base_aux.pytester import *
from base_aux.funcs.value_0_explicit import Default
from base_aux.classes.cmp import CmpInst
from base_aux.objects import *


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
    pytest_func_tester__no_kwargs(func_link=lambda result: result == 1, args=Cls(1), _EXPECTED=True)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="func_link, args, kwargs, _EXPECTED, _pytestExpected",
    argvalues=[
        # not callable ------------
        (True, Default, None, True, True),
        (True, 111, {111: 222}, True, True),
        (False, Default, {}, True, False),

        # callable ------------
        (lambda value: value, Default, {}, True, False),

        (lambda value: value, None, {}, True, False),
        (lambda value: value, None, {}, None, True),
        (lambda value: value, True, {}, True, True),
        (lambda value: value, (True, ), {}, True, True),
        (lambda value: value, Default, {"value": True}, True, True),
        (lambda value: value, Default, {"value": None}, True, False),
    ]
)
def test__pytest_func_tester(func_link, args, kwargs, _EXPECTED, _pytestExpected):
    try:
        pytest_func_tester(func_link=func_link, args=args, kwargs=kwargs, _EXPECTED=_EXPECTED)
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
    pytest_func_tester(func_link, args, kwargs, _EXPECTED)


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
    pytest_func_tester(func_link, args, kwargs, _EXPECTED)


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
    pytest_func_tester(func_link, args, kwargs, _EXPECTED)


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
    pytest_func_tester(func_link, args, kwargs, _EXPECTED)


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
    pytest_func_tester(func_link, args, kwargs, _EXPECTED)


# =====================================================================================================================
