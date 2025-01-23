import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_attr.m1_attr2_anycase import *


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
    ExpectAux(func_link, args).check_assert(_EXPECTED)


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
    ExpectAux(func_link, attr).check_assert(_EXPECTED)


# =====================================================================================================================
