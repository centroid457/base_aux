import pytest

from base_aux.aux_attr.m1_attr3_lambdas_resolve import *
from base_aux.aux_pytester.m1_pytest_aux import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="value, _EXPECTED",
    argvalues=[
        (1, True),
        ("hello", Exception),
    ]
)
def test__common__define(value, _EXPECTED):
    define_was_ok = True
    try:
        class Victim:
            ATTR0 = 0
            ATTR_INT = int(value)
            ATTR_STR = str(value)

    except Exception as exx:
        define_was_ok = exx

    PytestAux(define_was_ok).assert_check(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="value, _EXPECTED",
    argvalues=[
        (1, True),
        ("hello", Exception),
    ]
)
def test__special__define_and_init(value, _EXPECTED):
    # DEFINE ---------------------
    class Victim(AttrsLambdasResolve):
        ATTR0 = 0
        ATTR_INT = Lambda(int, value)
        ATTR_STR = Lambda(str, value)

    assert True     # no exx above!

    # INIT -----------------------
    init_was_ok = True
    try:
        victim = Victim()
    except Exception as exx:
        init_was_ok = exx
    else:
        assert victim.ATTR0 == 0
        assert victim.ATTR_INT == value
        assert victim.ATTR_STR == str(value)

    PytestAux(init_was_ok).assert_check(_EXPECTED)


# =====================================================================================================================
