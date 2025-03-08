import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_text.m5_re1_rexp import RExp


# =====================================================================================================================
def test__rexp():
    try:
        RExp()
        assert False
    except:
        pass

    assert RExp(111)[0] == 111

    assert RExp(111)[1] == None
    assert RExp(111, 222)[1] == 222

    assert RExp(111)[2] == None
    assert RExp(111, sub=333)[2] == 333
    assert RExp(111, sub=333).SUB == 333
    assert RExp(1, 2, 3, sub=333).sub == 333


# =====================================================================================================================
