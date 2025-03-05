from base_aux.aux_expect.m1_expect_aux import *
from base_aux.aux_attr.m1_attr1_aux import *
from base_aux.base_statics.m3_primitives import *
from base_aux.base_statics.m4_enums import *
from base_aux.aux_attr.m4_kits import *


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
    argnames="source, _EXPECTED",
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
    ExpectAux(set(AttrAux(source).iter__attrs_external_not_builtin())).check_assert(_EXPECTED[0])
    ExpectAux(set(AttrAux(source).iter__attrs_not_hidden())).check_assert(_EXPECTED[1])
    ExpectAux(set(AttrAux(source).iter__attrs_not_private())).check_assert(_EXPECTED[2])
    ExpectAux(set(AttrAux(source).iter__attrs_private())).check_assert(_EXPECTED[3])


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
def test__anycase__getset(attr, _EXPECTED):
    # use here EXACTLY the instance! if used class - value would changed in class and further values will not cmp correctly!

    ExpectAux(AttrAux(Victim2()).name_ic__get_original, attr).check_assert(_EXPECTED[0])
    ExpectAux(AttrAux(Victim2()).gai_ic, attr).check_assert(_EXPECTED[1])
    ExpectAux(AttrAux(Victim2()).sai_ic, (attr, 123)).check_assert(_EXPECTED[2])


# =====================================================================================================================
def test__load():
    victim = AttrDump()
    AttrAux(victim).sai__by_args_kwargs(**dict(attr=1))
    assert victim.attr == 1

    class Victim:
        pass

    victim = Victim()
    assert not hasattr(victim, "attr")
    assert not hasattr(victim, "ATTR")

    AttrAux(victim).sai__by_args_kwargs(**dict(attr=1))
    assert victim.attr == 1

    AttrAux(victim).sai__by_args_kwargs(**dict(ATTR=2))
    assert victim.attr == 2

    assert not hasattr(victim, "ATTR")


# =====================================================================================================================
class Victim:
    NONE = None
    TRUE = True
    LTRUE = LAMBDA_TRUE
    RAISE = LAMBDA_RAISE


class Test__Dump:
    def test__zero(self):
        assert AttrAux().dump_dict() == dict()

    def test__names(self):
        class VictimNames:
            attr = None
            _attr = None
            __attr = None

        result = AttrAux(VictimNames()).dump_dict()
        assert result == {"attr": None, "_attr": None}

    @pytest.mark.parametrize(
        argnames="cal_use, _EXPECTED",
        argvalues=[
            (CallableResolve.DIRECT, (None, True, LAMBDA_TRUE, LAMBDA_RAISE,)),
            (CallableResolve.EXX, (None, True, True, Exception,)),
            # (CallableResolve.RAISE, Exception),          # need special tests!
            (CallableResolve.RAISE_AS_NONE, (None, True, True, None,)),
            (CallableResolve.BOOL, (False, True, True, False,)),
            (CallableResolve.SKIP_CALLABLE, (None, True, None, None,)),
            (CallableResolve.SKIP_RAISED, (None, True, True, None,)),
        ]
    )
    def test__callable_use(self, cal_use, _EXPECTED):
        result_dict = AttrAux(Victim).dump_dict(cal_use)
        ExpectAux(dict.get, (result_dict, "NONE")).check_assert(_EXPECTED[0])
        ExpectAux(dict.get, (result_dict, "TRUE")).check_assert(_EXPECTED[1])
        ExpectAux(dict.get, (result_dict, "LTRUE")).check_assert(_EXPECTED[2])
        ExpectAux(dict.get, (result_dict, "RAISE")).check_assert(_EXPECTED[3])

    def test__callable_use__special_raise(self):
        try:
            result_dict = AttrAux(Victim).dump_dict(CallableResolve.RAISE)
            assert False
        except:
            assert True


# =====================================================================================================================
