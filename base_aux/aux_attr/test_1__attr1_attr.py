import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m4_primitives import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# =====================================================================================================================
def test__reinit__mutable_cls_values():
    class Victim:
        LIST = []
        SET = {}
        DICT = {}

        def __init__(self, LIST=None, SET=None, DICT=None):
            if LIST is not None:
                self.LIST = LIST
            if SET is not None:
                self.SET = SET
            if DICT is not None:
                self.DICT = DICT

    # SAME BLANK ----------
    victim = Victim()

    assert Victim.LIST == victim.LIST
    assert Victim.SET == victim.SET
    assert Victim.DICT == victim.DICT

    assert Victim.LIST is victim.LIST
    assert Victim.SET is victim.SET
    assert Victim.DICT is victim.DICT

    AttrAux_Existed(victim).reinit__mutable_cls_values()
    assert Victim.LIST is not victim.LIST
    assert Victim.SET is not victim.SET
    assert Victim.DICT is not victim.DICT

    # DIFF ----------
    victim = Victim([], {}, {})
    assert Victim.LIST == victim.LIST
    assert Victim.SET == victim.SET
    assert Victim.DICT == victim.DICT

    assert Victim.LIST is not victim.LIST
    assert Victim.SET is not victim.SET
    assert Victim.DICT is not victim.DICT

    AttrAux_Existed(victim).reinit__mutable_cls_values()
    assert Victim.LIST is not victim.LIST
    assert Victim.SET is not victim.SET
    assert Victim.DICT is not victim.DICT


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
    Lambda(set(AttrAux_Existed(source).iter__dirnames_original_not_builtin())).check_expected__assert(_EXPECTED[0])
    Lambda(set(AttrAux_Existed(source).iter__names_filter__not_hidden())).check_expected__assert(_EXPECTED[1])
    Lambda(set(AttrAux_Existed(source).iter__names_filter__not_private())).check_expected__assert(_EXPECTED[2])
    Lambda(set(AttrAux_Existed(source).iter__names_filter__private())).check_expected__assert(_EXPECTED[3])


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
        # (Victim3(), "AnNE", ("AnNE", True, Exception, None, )),   # FIXME: !!!!!!!!
        # (Victim3(), "ANNE", ("AnNE", True, Exception, None, )),   # FIXME: !!!!!!!!
    ]
)
def test__gsai(victim, attr, _EXPECTED):
    # use here EXACTLY the instance! if used class - value would changed in class and further values will not cmp correctly!

    Lambda(AttrAux_Existed(victim).name_ic__get_original, attr).check_expected__assert(_EXPECTED[0])
    Lambda(AttrAux_Existed(victim).name_ic__check_exists, attr).check_expected__assert(_EXPECTED[1])
    Lambda(AttrAux_Existed(victim).gai_ic, attr).check_expected__assert(_EXPECTED[2])
    Lambda(AttrAux_Existed(victim).sai_ic, attr, 123).check_expected__assert(_EXPECTED[3])


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
        Lambda(AttrAux_Existed(source).dump_dict, *skip).check_expected__assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="cal_use, _EXPECTED",
        argvalues=[
            (EnumAdj_CallResolveStyle.DIRECT, (None, True, LAMBDA_TRUE, LAMBDA_RAISE,)),
            (EnumAdj_CallResolveStyle.EXC, (None, True, True, Exception,)),
            # (EnumAdj_CallResolveStyle.RAISE, Exception),          # need special tests!
            (EnumAdj_CallResolveStyle.RAISE_AS_NONE, (None, True, True, None,)),
            (EnumAdj_CallResolveStyle.BOOL, (False, True, True, False,)),
            (EnumAdj_CallResolveStyle.SKIP_CALLABLE, (None, True, None, None,)),
            (EnumAdj_CallResolveStyle.SKIP_RAISED, (None, True, True, None,)),
        ]
    )
    def test__callable_use(self, cal_use, _EXPECTED):
        result_dict = AttrAux_Existed(Victim).dump_dict(callables_resolve=cal_use)
        Lambda(dict.get, result_dict, "NONE").check_expected__assert(_EXPECTED[0])
        Lambda(dict.get, result_dict, "TRUE").check_expected__assert(_EXPECTED[1])
        Lambda(dict.get, result_dict, "LTRUE").check_expected__assert(_EXPECTED[2])
        Lambda(dict.get, result_dict, "RAISE").check_expected__assert(_EXPECTED[3])

    def test__callable_use__special_raise(self):
        try:
            result_dict = AttrAux_Existed(Victim).dump_dict(callables_resolve=EnumAdj_CallResolveStyle.RAISE)
        except:
            pass
        else:
            assert False


# =====================================================================================================================
