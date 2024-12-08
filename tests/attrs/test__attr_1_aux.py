from typing import *
import pytest

from base_aux.pytester import *
from base_aux.attrs import *


# =====================================================================================================================
class Victim(AttrAux):
    attr_lowercase = "value"
    ATTR_UPPERCASE = "VALUE"
    Attr_CamelCase = "Value"


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="attr, _EXPECTED",
    argvalues=[
        (1, None),
        (None, None),
        (True, None),
        ("", None),
        (" TRUE", None),

        ("attr_lowercase", "attr_lowercase"),
        ("ATTR_LOWERCASE", "attr_lowercase"),

        ("ATTR_UPPERCASE", "ATTR_UPPERCASE"),
        ("attr_uppercase", "ATTR_UPPERCASE"),

        ("     attr_uppercase", "ATTR_UPPERCASE"),
    ]
)
def test__get_name(attr, _EXPECTED):
    args = (attr, Victim())
    func_link = AttrAux._attr_anycase__find
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="attr, _EXPECTED",
    argvalues=[
        (1, Exception),
        (None, Exception),
        (True, Exception),
        ("", Exception),
        (" TRUE", Exception),

        ("attr_lowercase", "value"),
        ("ATTR_LOWERCASE", "value"),

        ("ATTR_UPPERCASE", "VALUE"),
        ("attr_uppercase", "VALUE"),

        ("     attr_uppercase", "VALUE"),
    ]
)
def test__get_value(attr, _EXPECTED):
    args = (attr, Victim())
    func_link = AttrAux._getattr_anycase
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="attr, _EXPECTED",
    argvalues=[
        (1, Exception),
        (None, Exception),
        (True, Exception),
        ("", Exception),
        (" TRUE", None),    #->obj.TRUE!!!

        ("attr_lowercase", None),
        ("ATTR_LOWERCASE", None),

        ("ATTR_UPPERCASE", None),
        ("attr_uppercase", None),

        ("     attr_uppercase", None),

        ("HELLO", None),
    ]
)
def test__set_value(attr, _EXPECTED):
    victim = Victim()
    args = (attr, 123, victim)
    func_link = AttrAux._setattr_anycase
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
