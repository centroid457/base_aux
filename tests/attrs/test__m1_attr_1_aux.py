from typing import *
import pytest

from base_aux.pytester import *
from base_aux.attrs.m0_static import check_name__buildin
from base_aux.attrs.m1_attr_0_init_kwargs import AttrsInitByKwArgs
from base_aux.attrs.m1_attr_1_aux import AttrAux


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        ("_", False),
        ("__", False),
        ("____", False),

        ("___abc___", True),
        ("__abc__", True),
        ("__abc_", False),
        ("__abc", False),

        ("_abc__", False),
        ("_abc_", False),
        ("_abc", False),

        ("abc__", False),
        ("abc_", False),
        ("abc", False),
    ]
)
def test__name_is_build_in(source, _EXPECTED):
    func_link = check_name__buildin(source)
    pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
class Victim:
    a=1
    _h=2
    __p=3


@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (Victim, (dict(a=None), dict(a=None, _h=None), dict(__p=None))),
        (Victim(), (dict(a=None), dict(a=None, _h=None), dict(__p=None))),
    ]
)
def test__iter(source, _EXPECTED):
    # TODO: add tests for NESTED objects!
    pytest_func_tester__no_args_kwargs(set(AttrAux(source).iter__not_hidden()), set(_EXPECTED[0]))
    # pytest_func_tester__no_args_kwargs(set(AttrAux(source).iter__not_private()), set(_EXPECTED[1]))  # FIXME: need working!
    pytest_func_tester__no_args_kwargs(set(AttrAux(source).iter__private()), set(_EXPECTED[2]))


# =====================================================================================================================
class Victim2:
    attr_lowercase = "value"
    ATTR_UPPERCASE = "VALUE"
    Attr_CamelCase = "Value"


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

        ("     attr_uppercase", ("ATTR_UPPERCASE", "VALUE", None, )),
    ]
)
def test__anycase__xxx(attr, _EXPECTED):
    # use here EXACTLY the instance! if used class - value would changed in class and further values will not cmp correctly!

    pytest_func_tester__no_kwargs(AttrAux(Victim2()).anycase__find, attr, _EXPECTED[0])
    pytest_func_tester__no_kwargs(AttrAux(Victim2()).anycase__getattr, attr, _EXPECTED[1])
    pytest_func_tester__no_kwargs(AttrAux(Victim2()).anycase__setattr, (attr, 123), _EXPECTED[2])


# =====================================================================================================================
