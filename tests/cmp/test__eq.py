from typing import *
import pytest

from base_aux.base_objects import *

from base_aux.aux_pytester import *
from base_aux.cmp.eq import Eq


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, other, _EXPECTED",
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
def test__compare_doublesided(source, other, _EXPECTED):
    func_link = Eq(source).eq_doublesided_or_exx
    pytest_func_tester__no_kwargs(func_link, other, _EXPECTED[0])

    func_link = Eq(source).eq_doublesided__bool
    pytest_func_tester__no_kwargs(func_link, other, _EXPECTED[1])

    func_link = Eq(source).eq_doublesided__reverse
    pytest_func_tester__no_kwargs(func_link, other, _EXPECTED[2])


# =====================================================================================================================
