import pytest

from base_aux.aux_attr.m4_kits import AttrKit_Blank
from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_args_kwargs import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# =====================================================================================================================
EQ_ISINSTANCE_VICTIM = EqValid_IsinstanceSameinstance(NestInit_AnnotsAttr_ByArgsKwargs)


class Test__NestInit:
    def test__notNested(self):
        try:
            AttrKit_Blank()
            # Init_AnnotsAttrsByKwArgsIc()
            NestInit_AnnotsAttr_ByArgsKwargs()
            # NestInit_AnnotsAttrByKwArgsIc()
        except:
            assert False

        assert AttrKit_Blank(a1=1).a1 == 1
        assert AttrKit_Blank(a1=1).A1 == 1

        assert NestInit_AnnotsAttr_ByArgsKwargs(a1=1).a1 == 1
        try:
            assert NestInit_AnnotsAttr_ByArgsKwargs(a1=1).A1 == 1
        except:
            pass
        else:
            assert False

        # assert Init_AnnotsAttrsByKwArgsIc(a1=1).a1 == 1
        # assert Init_AnnotsAttrsByKwArgsIc(a1=1).A1 == 1

    def test__Nested(self):
        class Example(NestInit_AnnotsAttr_ByArgsKwargs):
            A1: Any
            A2: Any = None
            A3 = None

        Example()

        # assert Example(a1=1).A1 == 1
        # assert Example(1, a1=2).A1 == 2

        assert Example(1).A1 == 1
        assert Example(1).A2 == None
        assert Example(1).A3 == None

        try:
            assert Example(1, 1, 1)
        except:
            pass

        assert Example(1, 1).A2 == 1
        assert Example(1, 1).A3 == None
        assert Example(1, 1, a3=1).A3 == 1

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, kwargs, _EXPECTED",
        argvalues=[
            ((), dict(k1=1), EQ_ISINSTANCE_VICTIM),
            ((), dict(k1=1, k2=2), EQ_ISINSTANCE_VICTIM),

            ((), dict(k1=1, k2=2), EQ_ISINSTANCE_VICTIM),
        ]
    )
    def test__1(self, args, kwargs, _EXPECTED):
        Lambda(NestInit_AnnotsAttr_ByArgsKwargs, *args, **kwargs).expect__check_assert(_EXPECTED)

        if _EXPECTED == Exception:
            return

        victim = NestInit_AnnotsAttr_ByArgsKwargs(*args, **kwargs)
        for key, value in kwargs.items():
            assert getattr(victim, key) == value

        for arg in args:
            # args used only for Annots!
            try:
                getattr(victim, arg)
            except:
                pass
            else:
                assert False

# =====================================================================================================================
class Victim(NestInit_AnnotsAttr_ByArgsKwargs):
    # At0
    At1 = None
    An0: Any
    An1: Any = None


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED, values",
    argvalues=[
        ((), dict(At0=111), Victim, (111, None, Exception, None)),
        ((), dict(At1=222), Victim, (Exception, 222, Exception, None)),

        ((333, 444), dict(At0=111, At1=222), EQ_ISINSTANCE_VICTIM, (111, 222, 333, 444)),
        ((333, 444), dict(At0=111, At1=222), EQ_ISINSTANCE_VICTIM, (111, 222, 333, 444)),
        ((11, 22), dict(At0=111, At1=222, An0=333, An1=444), EQ_ISINSTANCE_VICTIM, (111, 222, 333, 444)),
        ((11, 22), dict(AT0=111, AT1=222, AN0=333, AN1=444), EQ_ISINSTANCE_VICTIM, (Exception, 222, 333, 444)),
    ]
)
def test__2(args, kwargs, _EXPECTED, values):
    Lambda(Victim, *args, **kwargs).expect__check_assert(_EXPECTED)

    victim = Victim(*args, **kwargs)
    for index, name in enumerate(["At0", "At1", "An0", "An1"]):
        Lambda(getattr, victim, name).expect__check_assert(values[index])


# =====================================================================================================================
