import pytest

from base_aux.base_lambdas.m1_lambda import *

from base_aux.base_values.m3_exceptions import *
from base_aux.aux_attr.m3_ga1_prefix_1_inst import NestGa_Prefix_RaiseIf


# =====================================================================================================================
class Victim(NestGa_Prefix_RaiseIf):
    TRUE = True
    FALSE = False
    NONE = None

    def meth(self, value: Any = None):
        return value


# =====================================================================================================================
def test__register():
    # --------------------------------
    assert Victim().TRUE is True
    assert Victim().true is True

    # --------------------------------
    try:
        Victim().raise_if__true()
    except Exc__GetattrPrefix_RaiseIf:
        pass
    else:
        assert False
    try:
        Victim().raise_if__TRUE()
    except Exc__GetattrPrefix_RaiseIf:
        pass
    else:
        assert False
    try:
        Victim().RAISE_IF__TRUE()
    except Exc__GetattrPrefix_RaiseIf:
        pass
    else:
        assert False

    # --------------------------------
    assert Victim().raise_if_not__TRUE() is None
    assert Victim().raise_if_not__true() is None
    assert Victim().RAISE_IF_NOT__TRUE() is None


# =====================================================================================================================
def test__attr__not_exists():
    # TRUE ---------------------
    try:
        Victim().raise_if__HELLO()
    except Exception:
        pass
    else:
        assert False


# ---------------------------------------------------------------------------------------------------------------------
def test__attr__static():
    # TRUE ---------------------
    assert Victim().TRUE is True

    try:
        Victim().raise_if__TRUE()
    except Exc__GetattrPrefix_RaiseIf:
        pass
    else:
        assert False
    assert Victim().raise_if_not__TRUE() is None
    assert Victim().raise_if_not__true() is None
    assert Victim().RAISE_IF_NOT__TRUE() is None

    # FALSE ---------------------
    assert Victim().FALSE is False

    try:
        Victim().raise_if_not__FALSE()
    except Exc__GetattrPrefix_RaiseIf:
        pass
    else:
        assert False
    assert Victim().raise_if__FALSE() is None

    # NONE ---------------------
    assert Victim().NONE is None

    try:
        Victim().raise_if_not__NONE()
    except Exc__GetattrPrefix_RaiseIf:
        pass
    else:
        assert False
    assert Victim().raise_if__NONE() is None


# =====================================================================================================================
def test__meth_not_passed():
    # NOT_PASSED ---------------------
    assert Victim().meth() is None
    assert Victim().METH() is None

    try:
        Victim().METH2()
    except AttributeError:
        pass
    else:
        assert False


@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (None, None),
        (True, Exc__GetattrPrefix_RaiseIf),
        (False, None),
    ]
)
def test___meth__raise_if(args, _EXPECTED):
    func_link = Victim().raise_if__METH
    Lambda(func_link, args).check_expected__assert(_EXPECTED)


@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (None, Exc__GetattrPrefix_RaiseIf),
        (True, None),
        (False, Exc__GetattrPrefix_RaiseIf),
    ]
)
def test___meth__raise_if_not(args, _EXPECTED):
    func_link = Victim().raise_if_not__METH
    Lambda(func_link, args).check_expected__assert(_EXPECTED)


# =====================================================================================================================
# @pytest.mark.skip
def test__comment():
    COMMENT_APPLYED = "COMMENT_APPLYED"
    try:
        Victim().raise_if__METH(True, COMMENT=COMMENT_APPLYED)
    except Exc__GetattrPrefix_RaiseIf as exc:
        print(exc)
        # ObjectInfo(exc).print()
        assert COMMENT_APPLYED in str(exc)
    else:
        assert False


# =====================================================================================================================
