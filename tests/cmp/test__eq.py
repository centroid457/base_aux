import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_types.m0_primitives import *

from base_aux.cmp.m2_eq import EqAux


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, args, _EXPECTED",
    argvalues=[
        (1, 1,        (True, True, False)),
        (1, 2,        (False, False, True)),
        (LAMBDA_TRUE, True, (False, False, True)),

        (ClsEq(1), 1, (True, True, False)),
        (ClsEq(1), 2, (False, False, True)),
        (1, ClsEq(1), (True, True, False)),
        (2, ClsEq(1), (False, False, True)),

        (ClsEqRaise(), 1, (Exception, False, True)),
        (1, ClsEqRaise(), (Exception, False, True)),
    ]
)
def test__compare_doublesided(source, args, _EXPECTED):
    ExpectAux(EqAux(source).check_doubleside__exx, args).check_assert(_EXPECTED[0])
    ExpectAux(EqAux(source).check_doubleside__bool, args).check_assert(_EXPECTED[1])
    ExpectAux(EqAux(source).check_doubleside__reverse, args).check_assert(_EXPECTED[2])


# =====================================================================================================================
