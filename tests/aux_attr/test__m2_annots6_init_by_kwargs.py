import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.base_inits.m3_nest_init_annots_attrs_by_kwargs import *
from base_aux.aux_cmp_eq.m3_eq_valid3_derivatives import *


# =====================================================================================================================
EQ_ISINSTANCE_VICTIM = EqValid_Isinstance(NestInit_AnnotsAttrByKwArgs)


class Test__NestInit:
    def test__notNested(self):
        try:
            Init_AnnotsAttrsByKwArgs()
            # Init_AnnotsAttrsByKwArgsIc()
            NestInit_AnnotsAttrByKwArgs()
            # NestInit_AnnotsAttrByKwArgsIc()
            assert True
        except:
            assert False

        assert Init_AnnotsAttrsByKwArgs(a1=1).a1 == 1
        assert NestInit_AnnotsAttrByKwArgs(a1=1).a1 == 1
        try:
            assert Init_AnnotsAttrsByKwArgs(a1=1).A1 == 1
            assert False
        except:
            assert True

        try:
            assert NestInit_AnnotsAttrByKwArgs(a1=1).A1 == 1
            assert False
        except:
            assert True

        # assert Init_AnnotsAttrsByKwArgsIc(a1=1).a1 == 1
        # assert Init_AnnotsAttrsByKwArgsIc(a1=1).A1 == 1

    def test__Nested(self):
        class Example(NestInit_AnnotsAttrByKwArgs):
            A1: Any
            A2: Any = None
            A3 = None

        try:
            Example()
            assert False
        except:
            assert True

        assert Example(a1=1).A1 == 1
        assert Example(1, a1=2).A1 == 2

        assert Example(1).A1 == 1
        assert Example(1).A2 == None
        assert Example(1).A3 == None

        assert Example(1, 1, 1).A1 == 1
        assert Example(1, 1, 1).A2 == 1
        assert Example(1, 1, 1).A3 == None
        assert Example(1, 1, a3=1).A3 == 1

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, kwargs, _EXPECTED",
        argvalues=[
            ((), {1: 1}, Exception),

            ((), dict(k1=1), EQ_ISINSTANCE_VICTIM),
            ((), dict(k1=1, k2=2), EQ_ISINSTANCE_VICTIM),

            (("a1", "a2"), dict(k1=1, k2=2), EQ_ISINSTANCE_VICTIM),
        ]
    )
    def test__1(self, args, kwargs, _EXPECTED):
        func_link = lambda *_args, **_kwargs: NestInit_AnnotsAttrByKwArgs(*_args, **_kwargs)
        ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)

        if _EXPECTED == Exception:
            return

        victim = func_link(*args, **kwargs)
        for key, value in kwargs.items():
            assert getattr(victim, key) == value

        for arg in args:
            # args used only for Annots!
            try:
                getattr(victim, arg)
                assert False
            except:
                assert True


# =====================================================================================================================
class Victim(NestInit_AnnotsAttrByKwArgs):
    # At0
    At1 = None
    An0: Any
    An1: Any = None


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED, values",
    argvalues=[
        ((), {1: 1}, Exception, ()),

        ((), dict(At0=111), Exception, ()),
        ((), dict(At1=111), Exception, ()),

        ((333, 444), dict(At0=111, At1=222), EQ_ISINSTANCE_VICTIM, (111, 222, 333, 444)),
        ((333, 444, 1, 2, 3, 4), dict(At0=111, At1=222), EQ_ISINSTANCE_VICTIM, (111, 222, 333, 444)),
        ((11, 22, 33, 44), dict(At0=111, At1=222, An0=333, An1=444), EQ_ISINSTANCE_VICTIM, (111, 222, 333, 444)),

        ((11, 22, 33, 44), dict(AT0=111, AT1=222, AN0=333, AN1=444), EQ_ISINSTANCE_VICTIM, (Exception, 222, 333, 444)),
    ]
)
def test__2(args, kwargs, _EXPECTED, values):
    func_link = lambda *_args, **_kwargs: Victim(*_args, **_kwargs)
    ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)

    if _EXPECTED == Exception:
        return

    victim = func_link(*args, **kwargs)
    for index, name in enumerate(["At0", "At1", "An0", "An1"]):
        ExpectAux(getattr, (victim, name)).check_assert(values[index])


# =====================================================================================================================
