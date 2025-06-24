from base_aux.aux_callable.m2_lambda import *
from base_aux.aux_values.m4_primitives import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# =====================================================================================================================
class Victim:
    a=1
    _h=2
    __p=3
    __name__=123
    __hello__=123


class VictimNested_Old(Victim):
    pass


class VictimNested_ReNew(Victim):
    a = 1
    _h = 2
    __p = 3
    __name__=123
    __hello__=123


class VictimNested_New(Victim):
    a2 = 1
    _h2 = 2
    __p2 = 3
    __name__=123
    __hello__=123


# =====================================================================================================================
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
    Lambda(set(AttrAux_Existed(source).iter__dirnames_original_not_builtin())).expect__check_assert(_EXPECTED[0])
    Lambda(set(AttrAux_Existed(source).iter__names_filter__not_hidden())).expect__check_assert(_EXPECTED[1])
    Lambda(set(AttrAux_Existed(source).iter__names_filter__not_private())).expect__check_assert(_EXPECTED[2])
    Lambda(set(AttrAux_Existed(source).iter__names_filter__private())).expect__check_assert(_EXPECTED[3])


# =====================================================================================================================
class Victim2:
    attr_lowercase = "value"
    ATTR_UPPERCASE = "VALUE"
    Attr_CamelCase = "Value"


class Victim3:
    AnE: int = 1
    AnNE: int


@pytest.mark.parametrize(
    argnames="victim, attr, _EXPECTED",
    argvalues=[
        (Victim2(), 1, (Exception, Exception, Exception, Exception, )),
        (Victim2(), None, (None, False, Exception, Exception, )),
        (Victim2(), True, (None, False, Exception, Exception, )),
        (Victim2(), "", (None, False, Exception, Exception, )),
        (Victim2(), " TRUE", (None, False, Exception, None, )),

        (Victim2(), "attr_lowercase", ("attr_lowercase", True, "value", None)),
        (Victim2(), "ATTR_LOWERCASE", ("attr_lowercase", True, "value", None, )),

        (Victim2(), "ATTR_UPPERCASE", ("ATTR_UPPERCASE", True, "VALUE", None, )),
        (Victim2(), "attr_uppercase", ("ATTR_UPPERCASE", True, "VALUE", None, )),

        (Victim2(), "     attr_uppercase", ("ATTR_UPPERCASE", True, "VALUE", None, )),

        # ANNOTS
        (Victim3(), "AnE", ("AnE", True, 1, None, )),
        (Victim3(), "ANE", ("AnE", True, 1, None, )),
        (Victim3(), "AnNE", ("AnNE", True, Exception, None, )),
        (Victim3(), "ANNE", ("AnNE", True, Exception, None, )),
    ]
)
def test__gsai(victim, attr, _EXPECTED):
    # use here EXACTLY the instance! if used class - value would changed in class and further values will not cmp correctly!

    Lambda(AttrAux_Existed(victim).name_ic__get_original, attr).expect__check_assert(_EXPECTED[0])
    Lambda(AttrAux_Existed(victim).name_ic__check_exists, attr).expect__check_assert(_EXPECTED[1])
    Lambda(AttrAux_Existed(victim).gai_ic, attr).expect__check_assert(_EXPECTED[2])
    Lambda(AttrAux_Existed(victim).sai_ic, attr, 123).expect__check_assert(_EXPECTED[3])


# =====================================================================================================================
def test__kwargs():
    victim = AttrDumped()
    AttrAux_Existed(victim).sai__by_args_kwargs(**dict(a1=1, A2=2))
    assert victim.a1 == 1
    assert victim.A2 == 2

    class Victim:
        a2=2

    victim = Victim()
    assert not hasattr(victim, "a1")
    assert hasattr(victim, "a2")
    assert not hasattr(victim, "A2")

    AttrAux_Existed(victim).sai__by_args_kwargs(**dict(a1=1))
    assert victim.a1 == 1

    AttrAux_Existed(victim).sai__by_args_kwargs(**dict(A2=22))
    assert victim.a2 == 22

    assert not hasattr(victim, "A2")


# =====================================================================================================================
class Victim:
    NONE = None
    TRUE = True
    LTRUE = LAMBDA_TRUE
    RAISE = LAMBDA_RAISE


class VictimNames:
    attr = None
    _attr = None
    __attr = None


class Test__Dump:
    def test__zero(self):
        assert AttrAux_Existed().dump_dict() == dict()

    @pytest.mark.parametrize(
        argnames="source, skip, _EXPECTED",
        argvalues=[
            (VictimNames(), [], {"attr": None, "_attr": None}),
            (VictimNames(), ["attr", ], {"_attr": None}),
            (VictimNames(), [EqValid_Contain("att"), ], {}),
            (VictimNames(), [EqValid_Contain("att5"), ], {"attr": None, "_attr": None}),
            (VictimNames(), ["attr", EqValid_Contain("att5"), ], {"_attr": None}),
        ]
    )
    def test__names(self, source, skip, _EXPECTED):
        Lambda(AttrAux_Existed(source).dump_dict, *skip).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="cal_use, _EXPECTED",
        argvalues=[
            (Enum_CallResolve.DIRECT, (None, True, LAMBDA_TRUE, LAMBDA_RAISE,)),
            (Enum_CallResolve.EXX, (None, True, True, Exception,)),
            # (Enum_CallResolve.RAISE, Exception),          # need special tests!
            (Enum_CallResolve.RAISE_AS_NONE, (None, True, True, None,)),
            (Enum_CallResolve.BOOL, (False, True, True, False,)),
            (Enum_CallResolve.SKIP_CALLABLE, (None, True, None, None,)),
            (Enum_CallResolve.SKIP_RAISED, (None, True, True, None,)),
        ]
    )
    def test__callable_use(self, cal_use, _EXPECTED):
        result_dict = AttrAux_Existed(Victim).dump_dict(callables_resolve=cal_use)
        Lambda(dict.get, result_dict, "NONE").expect__check_assert(_EXPECTED[0])
        Lambda(dict.get, result_dict, "TRUE").expect__check_assert(_EXPECTED[1])
        Lambda(dict.get, result_dict, "LTRUE").expect__check_assert(_EXPECTED[2])
        Lambda(dict.get, result_dict, "RAISE").expect__check_assert(_EXPECTED[3])

    def test__callable_use__special_raise(self):
        try:
            result_dict = AttrAux_Existed(Victim).dump_dict(callables_resolve=Enum_CallResolve.RAISE)
            assert False
        except:
            assert True


# =====================================================================================================================
