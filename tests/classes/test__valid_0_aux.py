from typing import *
import pytest

from base_aux.funcs import *
from base_aux.classes import *
from base_aux.objects import *


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
        # (ClsBoolRaise(), ClsBoolRaise()),
    ]
)
def test__get_result(args, _EXPECTED):
    func_link = ValidAux.get_result_or_raise
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


def test__get_result2():
    try:
        ValidAux.get_result_or_raise(LAMBDA_RAISE)
    except:
        assert True
    else:
        assert False

    assert ValidAux.get_result_or_raise(Exception) == Exception

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
        # (ClsBoolRaise(), ClsBoolRaise()),
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
        (ClsBoolRaise(), False),
    ]
)
def test__get_bool(args, _EXPECTED):
    func_link = Valid.get_result_bool
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        ((1, 1),        (True, True, False)),
        ((1, 2),        (False, False, True)),
        ((LAMBDA_TRUE, True), (False, False, True)),

        ((ClsEq(1), 1), (True, True, False)),
        ((ClsEq(1), 2), (False, False, True)),
        ((1, ClsEq(1)), (True, True, False)),
        ((2, ClsEq(1)), (False, False, True)),

        ((ClsEqRaise(), 1), (Exception, False, True)),
        ((1, ClsEqRaise()), (Exception, False, True)),
    ]
)
def test__compare_doublesided(args, _EXPECTED):
    func_link = Valid.compare_doublesided_or_exx
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED[0])

    func_link = Valid.compare_doublesided__bool
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED[1])

    func_link = Valid.compare_doublesided__reverse
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED[2])


# =====================================================================================================================
