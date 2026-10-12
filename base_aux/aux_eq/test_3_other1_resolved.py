import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m4_primitives import *

from base_aux.aux_eq.m3_eq_other1_resolved import *


# ======================================================================================================================
@pytest.mark.parametrize(
    argnames="modifiers, source, _EXPECTED_raise",
    argvalues=[
        ([], 1, False),

        ([None, ], 1, True),
        ([1, ], 1, True),
    ]
)
def test__raised(source, modifiers, _EXPECTED_raise):
    if _EXPECTED_raise:
        with pytest.raises(Exception):
            OtherResolved(source, modifiers)
    else:
        OtherResolved(source, modifiers)


# ======================================================================================================================
@pytest.mark.parametrize(
    argnames="source",
    argvalues=[1, LAMBDA_1]
)
@pytest.mark.parametrize(
    argnames="modifiers, other, _EXPECTED",
    argvalues=[
        # RAISES
        ([None, ], 1, Exception),
        ([1, ], 1, Exception),

        # CORRECT
        ([], 1, True),
        ([], "1", False),
        ([str, ], "1", True),
        ([str, ], 1, False),
        ([LAMBDA_RAISE, ], 1, True),
        ([LAMBDA_RAISE, str], 1, False),
        ([str, LAMBDA_RAISE, int], 1, True),
        ([LAMBDA_RAISE, ], 1, True),
        ([LAMBDA_RAISE, str], 1, False),
        ([str, LAMBDA_RAISE, int], 1, True),

        ([str, LAMBDA_RAISE, int, 1], 1, Exception),
    ]
)
def test__1(source, modifiers, other, _EXPECTED):
    func_link = lambda: OtherResolved(source, modifiers).RESULT == other
    Lambda(func_link).check_expected__assert(_EXPECTED)


# ======================================================================================================================
