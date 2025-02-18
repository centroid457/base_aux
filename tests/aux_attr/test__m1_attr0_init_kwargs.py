import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.base_inits.m3_nest_init_attrs_annots_by_kwargs import *
from base_aux.aux_eq.m2_eq_valid3_derivatives import *


# =====================================================================================================================
# @pytest.mark.parametrize(
#     argnames="args, kwargs, init_ok",
#     argvalues=[
#         ((), {1: 1}, False),
#
#         ((), dict(k1=1), True),
#         ((), dict(k1=1, k2=2), True),
#
#         (("a1", "a2"), dict(k1=1, k2=2), True),
#     ]
# )
# def test__0(args, kwargs, init_ok):
#     try:
#         victim = NestInit_AttrsOnlyByKwArgs(*args, **kwargs)
#         assert init_ok
#     except:
#         assert not init_ok
#         return
#
#     for key, value in kwargs.items():
#         assert getattr(victim, key) == value
#
#     for arg in args:
#         assert getattr(victim, arg) == None


# =====================================================================================================================
EQ_ISINSTANCE_VICTIM = EqValid_Isinstance(NestInit_AttrsByKwArgs_Base)
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {1: 1}, Exception),

        ((), dict(k1=1), EQ_ISINSTANCE_VICTIM),
        ((), dict(k1=1, k2=2), EQ_ISINSTANCE_VICTIM),

        (("a1", "a2"), dict(k1=1, k2=2), EQ_ISINSTANCE_VICTIM),
    ]
)
def test__1(args, kwargs, _EXPECTED):
    func_link = lambda *_args, **_kwargs: NestInit_AttrsOnlyByKwArgs(*_args, **_kwargs)
    ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)

    if _EXPECTED == Exception:
        return

    victim = func_link(*args, **kwargs)
    for key, value in kwargs.items():
        assert getattr(victim, key) == value

    for arg in args:
        assert getattr(victim, arg) == None


# =====================================================================================================================
class VictimAttrsOnly(NestInit_AttrsOnlyByKwArgs):
    # At0
    At1 = None
    An0: Any
    An1: Any = None


class VictimAnnotsOnly(NestInit_AnnotsOnlyByKwArgs):
    # At0
    At1 = None
    An0: Any
    An1: Any = None


class VictimAttrsAnnots(NestInit_AttrsAnnotsByKwArgs):
    # At0
    At1 = None
    An0: Any
    An1: Any = None


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, Cls, _EXPECTED, values",
    argvalues=[
        ((), {1: 1}, VictimAttrsOnly, Exception, ()),

        ((), dict(At0=111), VictimAttrsOnly, EQ_ISINSTANCE_VICTIM, (111, None, Exception, None)),
        ((), dict(At1=111), VictimAttrsOnly, EQ_ISINSTANCE_VICTIM, (Exception, 111, Exception, None)),

        (("a1", "a2"), dict(k1=1, k2=2), VictimAttrsOnly, EQ_ISINSTANCE_VICTIM, ()),
    ]
)
def test__2(args, kwargs, Cls, _EXPECTED, values):
    func_link = lambda *_args, **_kwargs: Cls(*_args, **_kwargs)
    ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)

    if _EXPECTED == Exception:
        return

    victim = func_link(*args, **kwargs)
    for index, name in enumerate(["At0", "At1", "An0", "An1"]):
        ExpectAux(getattr, (victim, name)).check_assert(values[index])


# =====================================================================================================================
