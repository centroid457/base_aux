from typing import *
import pytest
from pytest import mark
from pytest_aux import *
from funcs_aux import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (Exception, Exception),
        (Exception(), Exception),
        (LAMBDA_EXX, Exception),

        (True, True),
        (False, False),
        (None, None),
        (LAMBDA_TRUE, True),
        (LAMBDA_FALSE, False),
        (LAMBDA_NONE, None),

        ((), Exception),    # ????
        (([], ), []),
        ((LAMBDA_LIST_DIRECT), []),

        (([None, ]), None),
        (([1, ]), 1),

        # (ClsBoolTrue(), ClsBoolTrue()),
        # (ClsBoolFalse(), ClsBoolFalse()),
        # (ClsBoolExx(), ClsBoolExx()),
    ]
)
def test__get_result(args, _EXPECTED):
    func_link = ValidAux.get_result
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


def test__get_result2():
    try:
        ValidAux.get_result(LAMBDA_EXX)
        assert False
    except:
        assert True

    assert ValidAux.get_result(Exception) == Exception

# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (Exception, Exception),
        (Exception(), Exception),
        (LAMBDA_EXX, Exception),

        (True, True),
        (False, False),
        (None, None),
        (LAMBDA_TRUE, True),
        (LAMBDA_FALSE, False),
        (LAMBDA_NONE, None),

        ((), Exception),    # ????
        (([], ), []),
        ((LAMBDA_LIST_DIRECT), []),

        (([None, ]), None),
        (([1, ]), 1),

        # (ClsBoolTrue(), ClsBoolTrue()),
        # (ClsBoolFalse(), ClsBoolFalse()),
        # (ClsBoolExx(), ClsBoolExx()),
    ]
)
def test__get_result_or_exx(args, _EXPECTED):
    func_link = ValidAux.get_result_or_exx
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (Exception, False),
        (Exception(), False),
        (LAMBDA_EXX, False),

        (True, True),
        (False, False),
        (None, False),
        (LAMBDA_TRUE, True),
        (LAMBDA_FALSE, False),
        (LAMBDA_NONE, False),

        ((), Exception),    # ????
        (([], ), False),
        ((LAMBDA_LIST_DIRECT), False),

        (([None, ]), False),
        (([1, ]), True),

        (ClsBoolTrue(), True),
        (ClsBoolFalse(), False),
        (ClsBoolExx(), False),
    ]
)
def test__get_bool(args, _EXPECTED):
    func_link = Valid.get_bool
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        ((1, 1), True),
        ((1, 2), False),
        ((LAMBDA_TRUE, True), False),

        ((ClsEq(1), 1), True),
        ((ClsEq(1), 2), False),
        ((1, ClsEq(1)), True),
        ((2, ClsEq(1)), False),

        ((ClsEqExx(), 1), Exception),
        ((1, ClsEqExx()), Exception),
    ]
)
def test__compare_doublesided(args, _EXPECTED):
    func_link = Valid.compare_doublesided
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
