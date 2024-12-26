from typing import *
import pytest

from base_aux.pytester import *
from base_aux.attrs import *


# =====================================================================================================================
class Victim:
    attr_lowercase = "value"
    ATTR_UPPERCASE = "VALUE"
    Attr_CamelCase = "Value"


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="attr, _EXPECTED",
    argvalues=[
        (1, (None, Exception, Exception, )),
        (None, (None, Exception, Exception, )),
        (True, (None, Exception, Exception, )),
        ("", (None, Exception, Exception, )),
        (" TRUE", (None, Exception, None, )),

        ("attr_lowercase", ("attr_lowercase", "value", None)),
        ("ATTR_LOWERCASE", ("attr_lowercase", "value", None, )),

        ("ATTR_UPPERCASE", ("ATTR_UPPERCASE", "VALUE", None, )),
        ("attr_uppercase", ("ATTR_UPPERCASE", "VALUE", None, )),

        ("     attr_uppercase",("ATTR_UPPERCASE", "VALUE", None, )),
    ]
)
def test__anycase__xxx(attr, _EXPECTED):
    pytest_func_tester__no_kwargs(AttrAux(Victim()).anycase__find, attr, _EXPECTED[0])
    pytest_func_tester__no_kwargs(AttrAux(Victim()).anycase__getattr, attr, _EXPECTED[1])
    pytest_func_tester__no_kwargs(AttrAux(Victim()).anycase__setattr, (attr, 123), _EXPECTED[2])


# =====================================================================================================================
