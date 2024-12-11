from typing import *
import pytest

from base_aux.pytester import *
from base_aux.valid import *
from base_aux.objects import *


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
    func_link = ValidAux.eq_doublesided_or_exx
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED[0])

    func_link = ValidAux.eq_doublesided__bool
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED[1])

    func_link = ValidAux.eq_doublesided__reverse
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED[2])


# =====================================================================================================================
