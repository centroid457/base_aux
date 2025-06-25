import pytest

from base_aux.lambdas.m1_lambda import *
from base_aux.aux_eq.m1_eq_args import EqArgs
from base_aux.aux_values.m4_primitives import INST_EQ_RAISE, INST_EQ_FALSE, INST_EQ_TRUE


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        ((), Exception),
        ((1, ), Exception),
        ((1, 1), True),
        ((1, 1, 1, 1), True),

        ((1, 1, 1, 11), False),
        ((1, 1, 11, 1), False),
        ((1, INST_EQ_RAISE), False),
        ((1, INST_EQ_FALSE), False),
        ((1, INST_EQ_TRUE), True),
    ]
)
def test__1(args, _EXPECTED):
    Lambda(EqArgs(*args)).expect__check_assert(_EXPECTED)


# =====================================================================================================================
