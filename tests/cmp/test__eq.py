from typing import *
import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux
from base_aux.base_objects.m0_primitives import *

from base_aux.cmp.eq import Eq


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
    PytestAux(Eq(source).eq_doublesided_or_exx, args).assert_check(_EXPECTED[0])
    PytestAux(Eq(source).eq_doublesided__bool, args).assert_check(_EXPECTED[1])
    PytestAux(Eq(source).eq_doublesided__reverse, args).assert_check(_EXPECTED[2])


# =====================================================================================================================
