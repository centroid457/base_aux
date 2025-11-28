import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_text.m5_re1_rexp import RExp


# =====================================================================================================================
def test__rexp():
    try:
        RExp()
    except:
        pass
    else:
        assert False

    assert RExp(111)[0] == 111

    assert RExp(111)[1] == None
    assert RExp(111, 222)[1] == 222

    assert RExp(111)[2] == None
    assert RExp(111, sub=333)[2] == 333
    assert RExp(111, sub=333).SUB == 333
    assert RExp(1, 2, 3, sub=333).sub == 333


# =====================================================================================================================
