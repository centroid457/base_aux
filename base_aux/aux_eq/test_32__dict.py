import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m4_primitives import *

from base_aux.aux_eq.m4_eq_valid2_derivatives import *


# ======================================================================================================================
@pytest.mark.parametrize(
    argnames="other, variant, _EXPECTED",   # [full, part, direct]
    argvalues=[
        (None, dict(), [False, False, False]),
        (1, dict(), [False, False, False]),
        (LAMBDA_RAISE, dict(), [False, False, False]),

        (dict(), dict(), [True, True, True]),

        (dict(), dict(k1=1, k2=2), [False, False, False]),
        (dict(k1=1, k2=2), dict(), [False, True, False]),

        (dict(k1=1, k2=2), dict(k2=2), [False, True, False]),
        (dict(k1=1, k2=2), dict(k2=EqValid_EQ(2)), [False, True, False]),
        (dict(k1=1, k2=2), dict(k1=EqValid_NumParsedSingle_TypeInt(), k2=EqValid_EQ(2)), [True, True, True]),

        (dict(k1=1, k2=2), dict(k2=22), [False, False, False]),
        (dict(k1=1, k2=2), dict(k2=EqValid_EQ(22)), [False, False, False]),
    ]
)
def test__dict(other, variant, _EXPECTED):
    # OBJECT
    Lambda(EqValid_DictFull(variant) == other).check_expected__assert(_EXPECTED[0])
    Lambda(other in EqValid_DictFull(variant)).check_expected__assert(_EXPECTED[0])

    Lambda(EqValid_DictPart(variant) == other).check_expected__assert(_EXPECTED[1])
    Lambda(other in EqValid_DictPart(variant)).check_expected__assert(_EXPECTED[1])

    # DIRECT
    Lambda(variant == other).check_expected__assert(_EXPECTED[2])


# ======================================================================================================================
def test__direct():
    target = {
        "UTC": 8372420,
        "Distance up": 19,
        "Distance side": 0,
        "Temperature": 23,
        "Battery": 99,
        "Percentage": 22
    }
    validator = {
        "UTC": EqValid_GT_NumParsedSingle(0),
        "Distance up": EqValid_GL_EE((0, 100)),
        "Distance side": EqValid_GL_EE((0, 10)),
        "Temperature": EqValid_GL_EE((0, 40)),
        "Battery": EqValid_GL_EE((0, 100)),
        "Percentage": EqValid_GL_EE((0, 100)),
    }
    assert EqValid_GT_NumParsedSingle(0) == 8372420
    assert target.keys() == validator.keys()

    for key, value in target.items():
        print(f"TRY={validator[key]=}/{value=}")
        assert validator[key] == value
        print(f"TRUE")

    assert target == validator
