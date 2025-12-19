from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_nest_dunders.m1_init0_reinit2_lambdas_resolve import *


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

    except Exception as exc:
        define_was_ok = exc

    Lambda(define_was_ok).check_expected__assert(_EXPECTED)


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
    class Victim(NestInit_AttrsLambdaResolve):
        ATTR0 = 0
        ATTR_INT = Lambda(int, value)
        ATTR_STR = Lambda(str, value)

    assert True     # no exc above!

    # INIT -----------------------
    init_was_ok = True
    try:
        victim = Victim()
    except Exception as exc:
        init_was_ok = exc
    else:
        assert victim.ATTR0 == 0
        assert victim.ATTR_INT == value
        assert victim.ATTR_STR == str(value)

    Lambda(init_was_ok).check_expected__assert(_EXPECTED)


# =====================================================================================================================
