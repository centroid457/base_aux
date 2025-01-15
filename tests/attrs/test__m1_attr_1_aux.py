import pytest

from base_aux.aux_pytester import *
from base_aux.aux_attr.m0_static import AttrsDump
from base_aux.aux_attr.m1_attr_1_aux import AttrAux


# =====================================================================================================================
class Victim:
    a=1
    _h=2
    __p=3


class VictimNested_Old(Victim):
    pass

class VictimNested_ReNew(Victim):
    a = 1
    _h = 2
    __p = 3

class VictimNested_New(Victim):
    a2 = 1
    _h2 = 2
    __p2 = 3


@pytest.mark.parametrize(
    argnames="source, EXPECTED",
    argvalues=[
        (Victim,    ({"a", "_h", "__p"}, {"a", }, {"a", "_h", }, {"__p", })),
        (Victim(),  ({"a", "_h", "__p"}, {"a", }, {"a", "_h", }, {"__p", })),

        (VictimNested_Old,      ({"a", "_h", "__p"}, {"a", }, {"a", "_h", }, {"__p", })),
        (VictimNested_Old(),    ({"a", "_h", "__p"}, {"a", }, {"a", "_h", }, {"__p", })),

        (VictimNested_ReNew,    ({"a", "_h", "__p"}, {"a", }, {"a", "_h", }, {"__p", })),
        (VictimNested_ReNew(),  ({"a", "_h", "__p"}, {"a", }, {"a", "_h", }, {"__p", })),

        (VictimNested_New,
         (
                {"a", "_h", "__p", "a2", "_h2", "__p2", },
                {"a", "a2", },
                {"a", "_h", "a2", "_h2", },
                {"__p", "__p2", },
         )),
        (VictimNested_New(),
         (
                 {"a", "_h", "__p", "a2", "_h2", "__p2", },
                 {"a", "a2", },
                 {"a", "_h", "a2", "_h2", },
                 {"__p", "__p2", },
         )),
    ]
)
def test__iter(source, _EXPECTED):
    pytest_func_tester__no_args_kwargs(set(AttrAux(source).iter__external_not_builtin()), _EXPECTED[0])
    pytest_func_tester__no_args_kwargs(set(AttrAux(source).iter__not_hidden()), _EXPECTED[1])
    pytest_func_tester__no_args_kwargs(set(AttrAux(source).iter__not_private()), _EXPECTED[2])
    pytest_func_tester__no_args_kwargs(set(AttrAux(source).iter__private()), _EXPECTED[3])


# =====================================================================================================================
class Victim2:
    attr_lowercase = "value"
    ATTR_UPPERCASE = "VALUE"
    Attr_CamelCase = "Value"


@pytest.mark.parametrize(
    argnames="attr, EXPECTED",
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
def test__load__wo_template():
    other = AttrAux().load__by_dict(dict(attr=1))
    assert isinstance(other, AttrsDump)
    assert other.attr == 1

    class Victim:
        pass

    victim = Victim()
    assert not hasattr(victim, "attr")
    assert not hasattr(victim, "ATTR")

    other = AttrAux(victim).load__by_dict(dict(attr=1))
    assert isinstance(other, Victim)
    assert other == victim
    assert other.attr == 1

    other = AttrAux(victim).load__by_dict(dict(ATTR=2))
    assert other == victim
    assert other.attr == 2

    assert not hasattr(victim, "ATTR")


# =====================================================================================================================
