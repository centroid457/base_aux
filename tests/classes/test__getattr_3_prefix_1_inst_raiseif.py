from typing import *
import pytest

from base_aux.exceptions import *
from base_aux.pytester import *
from base_aux.classes import *


# =====================================================================================================================
class Victim(GetattrPrefixInst_RaiseIf):
    TRUE = True
    FALSE = False
    NONE = None

    def meth(self, value: Any = None):
        return value


# =====================================================================================================================
def test__register():
    # --------------------------------
    assert Victim().TRUE is True

    try:
        assert Victim().true is True
    except AttributeError:
        pass
    else:
        assert False

    # --------------------------------
    try:
        Victim().raise_if__true()
    except Exx__GetattrPrefix_RaiseIf:
        pass
    else:
        assert False
    try:
        Victim().raise_if__TRUE()
    except Exx__GetattrPrefix_RaiseIf:
        pass
    else:
        assert False
    try:
        Victim().RAISE_IF__TRUE()
    except Exx__GetattrPrefix_RaiseIf:
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
    except AttributeError:
        pass
    else:
        assert False


# ---------------------------------------------------------------------------------------------------------------------
def test__attr__static():
    # TRUE ---------------------
    assert Victim().TRUE is True

    try:
        Victim().raise_if__TRUE()
    except Exx__GetattrPrefix_RaiseIf:
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
    except Exx__GetattrPrefix_RaiseIf:
        pass
    else:
        assert False
    assert Victim().raise_if__FALSE() is None

    # NONE ---------------------
    assert Victim().NONE is None

    try:
        Victim().raise_if_not__NONE()
    except Exx__GetattrPrefix_RaiseIf:
        pass
    else:
        assert False
    assert Victim().raise_if__NONE() is None


# =====================================================================================================================
def test__meth_not_passed():
    # NOT_PASSED ---------------------
    assert Victim().meth() is None

    try:
        Victim().METH()
    except AttributeError:
        pass
    else:
        assert False


@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (None, None),
        (True, Exx__GetattrPrefix_RaiseIf),
        (False, None),
    ]
)
def test___meth__raise_if(args, _EXPECTED):
    func_link = Victim().raise_if__METH
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)

@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (None, Exx__GetattrPrefix_RaiseIf),
        (True, None),
        (False, Exx__GetattrPrefix_RaiseIf),
    ]
)
def test___meth__raise_if_not(args, _EXPECTED):
    func_link = Victim().raise_if_not__METH
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
# @pytest.mark.skip
def test__comment():
    COMMENT_APPLYED = "COMMENT_APPLYED"
    try:
        Victim().raise_if__METH(True, COMMENT=COMMENT_APPLYED)
    except Exx__GetattrPrefix_RaiseIf as exx:
        print(exx)
        # ObjectInfo(exx).print()
        assert COMMENT_APPLYED in str(exx)
    else:
        assert False


# =====================================================================================================================
