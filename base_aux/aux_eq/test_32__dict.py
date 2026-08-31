import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m4_primitives import *

from base_aux.aux_eq.m4_eq_valid2_derivatives import *


# ======================================================================================================================
# ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="other, variant, _EXPECTED",   # [full, part]
    argvalues=[
        (None, dict(), [False, False]),
        (1, dict(), [False, False]),
        (LAMBDA_RAISE, dict(), [False, False]),

        (dict(), dict(), [True, True]),

        (dict(), dict(k1=1, k2=2), [False, False]),
        (dict(k1=1, k2=2), dict(), [False, True]),

        (dict(k1=1, k2=2), dict(k2=2), [False, True]),
        (dict(k1=1, k2=2), dict(k2=EqValid_EQ(2)), [False, True]),
        (dict(k1=1, k2=2), dict(k1=EqValid_NumParsedSingle_TypeInt(), k2=EqValid_EQ(2)), [True, True]),

        (dict(k1=1, k2=2), dict(k2=22), [False, False]),
        (dict(k1=1, k2=2), dict(k2=EqValid_EQ(22)), [False, False]),
    ]
)
def test__dict(other, variant, _EXPECTED):
    Lambda(EqValid_DictFull(variant) == other).check_expected__assert(_EXPECTED[0])
    Lambda(other in EqValid_DictFull(variant)).check_expected__assert(_EXPECTED[0])

    Lambda(EqValid_DictPart(variant) == other).check_expected__assert(_EXPECTED[1])
    Lambda(other in EqValid_DictPart(variant)).check_expected__assert(_EXPECTED[1])


# ======================================================================================================================
