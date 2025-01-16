import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux
from base_aux.aux_attr.m1_attr_2_anycase import *


# =====================================================================================================================
class Victim(AttrAnycaseGSAI):
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
    PytestAux(func_link, args).assert_check(_EXPECTED)


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
    PytestAux(func_link, attr).assert_check(_EXPECTED)


# =====================================================================================================================
