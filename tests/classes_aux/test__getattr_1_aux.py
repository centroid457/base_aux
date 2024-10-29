from typing import *
import pytest

from base_aux.funcs_aux import *
from base_aux.classes_aux import *


# =====================================================================================================================
class Victim(GetattrAux):
    attr_lowercase = "value"
    ATTR_UPPERCASE = "VALUE"
    Attr_CamelCase = "Value"


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="attr, _EXPECTED",
    argvalues=[
        (None, None),
        (True, None),
        ("", None),
        (" TRUE", None),

        ("attr_lowercase", "attr_lowercase"),
        ("ATTR_LOWERCASE", "attr_lowercase"),

        ("ATTR_UPPERCASE", "ATTR_UPPERCASE"),
        ("attr_uppercase", "ATTR_UPPERCASE"),
    ]
)
def test__name(attr, _EXPECTED):
    args = (attr, Victim())
    func_link = GetattrAux._attr_anycase__get_name
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="attr, _EXPECTED",
    argvalues=[
        (None, Exception),
        (True, Exception),
        ("", Exception),
        (" TRUE", Exception),

        ("attr_lowercase", "value"),
        ("ATTR_LOWERCASE", "value"),

        ("ATTR_UPPERCASE", "VALUE"),
        ("attr_uppercase", "VALUE"),
    ]
)
def test__value(attr, _EXPECTED):
    args = (attr, Victim())
    func_link = GetattrAux._attr_anycase__get_value
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
