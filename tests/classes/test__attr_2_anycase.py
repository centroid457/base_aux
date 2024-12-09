from typing import *
import pytest

from base_aux.pytester import *
from base_aux.classes import *


# =====================================================================================================================
class Victim(AttrAnycase):
    attr_lowercase = "value"
    ATTR_UPPERCASE = "VALUE"
    Attr_CamelCase = "Value"


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

        ("     attr_uppercase", "VALUE"),
    ]
)
def test__attr(attr, _EXPECTED):
    args = (Victim(), attr)
    func_link = getattr
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

        ("     attr_uppercase", "VALUE"),
    ]
)
def test__item(attr, _EXPECTED):
    func_link = lambda _attr: Victim()[_attr]
    pytest_func_tester__no_kwargs(func_link, attr, _EXPECTED)


# =====================================================================================================================
