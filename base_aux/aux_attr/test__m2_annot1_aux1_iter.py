import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.base_nest_dunders.m4_gsai_ic__annots import NestGAI_AnnotAttrIC
from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
class VictimAt:
    at1 = 1
    _at1 = 11
    __at1 = 111


class VictimAn:
    an1: int = 1
    _an1: int = 11
    __an1: int = 111


class VictimAnNest(VictimAn):
    an2: int = 1
    _an2: int = 11
    __an2: int = 111


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (VictimAt(), [], [
            {"at1", "_at1", "__at1"},
            {"at1", "_at1", "__at1"},
            {"at1", "_at1", "__at1"},
        ]),
        (VictimAn(), [], [
            {"an1", "_an1", "__an1"},
            {"an1", "_an1", "__an1"},
            {"an1", "_an1", "__an1"},
        ]),
        (VictimAnNest(), [], [
            {"an1", "_an1", "__an1", "an2", "_an2", "__an2"},
            {"an1", "_an1", "__an1", "an2", "_an2", "__an2"},
            {"an1", "_an1", "__an1", "an2", "_an2", "__an2"},
        ]),
    ]
)
def test__ITER_1__iter__attrs_external_not_builtin(source, skip_names, _EXPECTED):
    ExpectAux(set(AttrAux(source, *skip_names).iter__attrs_external_not_builtin())).check_assert(set(_EXPECTED[0]))
    ExpectAux(set(AnnotsAllAux(source, *skip_names).iter__attrs_external_not_builtin())).check_assert(set(_EXPECTED[1]))
    ExpectAux(set(AnnotsLastAux(source, *skip_names).iter__attrs_external_not_builtin())).check_assert(set(_EXPECTED[2]))


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (VictimAt(), [], [
            {"at1", "_at1", "__at1"},
            {"at1", "_at1", "__at1"},
            {"at1", "_at1", "__at1"},
        ]),
        (VictimAn(), [], [
            {"an1", "_an1", "__an1"},
            {"an1", "_an1", "__an1"},
            {"an1", "_an1", "__an1"},
        ]),
        (VictimAnNest(), [], [
            {"an1", "_an1", "__an1", "an2", "_an2", "__an2"},
            {"an1", "_an1", "__an1", "an2", "_an2", "__an2"},
            {"an1", "_an1", "__an1", "an2", "_an2", "__an2"},
        ]),
    ]
)
def test__ITER_2__iter__names(source, skip_names, _EXPECTED):
    ExpectAux(set(AttrAux(source, *skip_names).iter__names())).check_assert(set(_EXPECTED[0]))
    ExpectAux(set(AnnotsAllAux(source, *skip_names).iter__names())).check_assert(set(_EXPECTED[1]))
    ExpectAux(set(AnnotsLastAux(source, *skip_names).iter__names())).check_assert(set(_EXPECTED[2]))


# =====================================================================================================================
