import pytest

from base_aux.attrs.attr_3_lambdas_resolve import *
from base_aux.pytester import *


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

    pytest_func_tester__no_args_kwargs(define_was_ok, _EXPECTED)


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

    pytest_func_tester__no_args_kwargs(init_was_ok, _EXPECTED)


# =====================================================================================================================
