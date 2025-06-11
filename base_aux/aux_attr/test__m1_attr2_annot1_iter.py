import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.base_nest_dunders.m4_gsai_ic__annots import NestGAI_AnnotAttrIC
from base_aux.aux_attr.m4_kits import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# =====================================================================================================================
class VictimAt:
    at1 = 1
    _at1 = 11
    __at1 = 111


class VictimAn:
    an1: int = 2
    _an1: int = 22
    __an1: int = 222


class VictimAnNest(VictimAn):
    an2: int = 3
    _an2: int = 33
    __an2: int = 333


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

        # -------------------------------
        (VictimAt(), ["at1", ], [
            {"_at1", "__at1"},
            {"_at1", "__at1"},
            {"_at1", "__at1"},
        ]),
        (VictimAn(), ["an1", ], [
            {"_an1", "__an1"},
            {"_an1", "__an1"},
            {"_an1", "__an1"},
        ]),
        (VictimAnNest(), ["an1", ], [
            {"_an1", "__an1", "an2", "_an2", "__an2"},
            {"_an1", "__an1", "an2", "_an2", "__an2"},
            {"_an1", "__an1", "an2", "_an2", "__an2"},
        ]),

        # -------------------------------
        (VictimAt(), [EqValid_ContainStrIc("_a"), ], [
            {"at1", },
            {"at1", },
            {"at1", },
        ]),
        (VictimAn(), [EqValid_ContainStrIc("_a"), ], [
            {"an1", },
            {"an1", },
            {"an1", },
        ]),
        (VictimAnNest(), [EqValid_ContainStrIc("_a"), ], [
            {"an1", "an2", },
            {"an1", "an2", },
            {"an1", "an2", },
        ]),
    ]
)
def test__ITER_1__iter__dirnames_original_not_builtin(source, skip_names, _EXPECTED):
    ExpectAux(set(AttrAux(source, *skip_names).iter__dirnames_original_not_builtin())).check_assert(set(_EXPECTED[0]))
    ExpectAux(set(AnnotsAllAux(source, *skip_names).iter__dirnames_original_not_builtin())).check_assert(set(_EXPECTED[1]))
    ExpectAux(set(AnnotsLastAux(source, *skip_names).iter__dirnames_original_not_builtin())).check_assert(set(_EXPECTED[2]))


# =====================================================================================================================
# NOTE: add iter_names - NOT NEED! used as next exact methods


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (VictimAt(), [], [
            {"at1", },
            {},
            {},
        ]),
        (VictimAn(), [], [
            {"an1", },
            {"an1", },
            {"an1", },
        ]),
        (VictimAnNest(), [], [
            {"an1", "an2", },
            {"an1", "an2", },
            {"an2", },
        ]),
    ]
)
def test__ITER__iter__names_filter__not_hidden(source, skip_names, _EXPECTED):
    ExpectAux(set(AttrAux(source, *skip_names).iter__names_filter__not_hidden())).check_assert(set(_EXPECTED[0]))
    ExpectAux(set(AnnotsAllAux(source, *skip_names).iter__names_filter__not_hidden())).check_assert(set(_EXPECTED[1]))
    ExpectAux(set(AnnotsLastAux(source, *skip_names).iter__names_filter__not_hidden())).check_assert(set(_EXPECTED[2]))


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (VictimAt(), [], [
            {"at1", "_at1", },
            {},
            {},
        ]),
        (VictimAn(), [], [
            {"an1", "_an1", },
            {"an1", "_an1", },
            {"an1", "_an1", },
        ]),
        (VictimAnNest(), [], [
            {"an1", "an2", "_an1", "_an2", },
            {"an1", "an2", "_an1", "_an2", },
            {"an2", "_an2", },
        ]),
    ]
)
def test__ITER__iter__names_filter__not_private(source, skip_names, _EXPECTED):
    ExpectAux(set(AttrAux(source, *skip_names).iter__names_filter__not_private())).check_assert(set(_EXPECTED[0]))
    ExpectAux(set(AnnotsAllAux(source, *skip_names).iter__names_filter__not_private())).check_assert(set(_EXPECTED[1]))
    ExpectAux(set(AnnotsLastAux(source, *skip_names).iter__names_filter__not_private())).check_assert(set(_EXPECTED[2]))


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (VictimAt(), [], [
            {"__at1", },
            {},
            {},
        ]),
        (VictimAn(), [], [
            {"__an1", },
            {"__an1", },
            {"__an1", },
        ]),
        (VictimAnNest(), [], [
            {"__an1", "__an2", },
            {"__an1", "__an2", },
            {"__an2", },
        ]),
    ]
)
def test__ITER__iter__names_filter__private(source, skip_names, _EXPECTED):
    ExpectAux(set(AttrAux(source, *skip_names).iter__names_filter__private())).check_assert(set(_EXPECTED[0]))
    ExpectAux(set(AnnotsAllAux(source, *skip_names).iter__names_filter__private())).check_assert(set(_EXPECTED[1]))
    ExpectAux(set(AnnotsLastAux(source, *skip_names).iter__names_filter__private())).check_assert(set(_EXPECTED[2]))


# =====================================================================================================================
# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (VictimAt(), [], [
            {VictimAt, },
            {VictimAt, },
            {VictimAt, },
        ]),
        (VictimAn(), [], [
            {VictimAn, },
            {VictimAn, },
            {VictimAn, },
        ]),
        (VictimAnNest(), [], [
            {VictimAnNest, VictimAn},
            {VictimAnNest, VictimAn},
            {VictimAnNest, VictimAn},
        ]),
    ]
)
def test__ITER___iter_mro(source, skip_names, _EXPECTED):
    ExpectAux(set(AttrAux(source, *skip_names)._iter_mro())).check_assert(set(_EXPECTED[0]))
    ExpectAux(set(AnnotsAllAux(source, *skip_names)._iter_mro())).check_assert(set(_EXPECTED[1]))
    ExpectAux(set(AnnotsLastAux(source, *skip_names)._iter_mro())).check_assert(set(_EXPECTED[2]))


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (VictimAt(), [], [
            {},
            {},
            {},
        ]),
        (VictimAn(), [], [
            {"an1", "_an1", "__an1"},
            {"an1", "_an1", "__an1"},
            {"an1", "_an1", "__an1"},
        ]),
        (VictimAnNest(), [], [
            {"an1", "_an1", "__an1", "an2", "_an2", "__an2"},
            {"an1", "_an1", "__an1", "an2", "_an2", "__an2"},
            {"an2", "_an2", "__an2"},
        ]),
    ]
)
def test__ITER__iter__annot_names(source, skip_names, _EXPECTED):
    ExpectAux(set(AttrAux(source, *skip_names).iter__annot_names())).check_assert(set(_EXPECTED[0]))
    ExpectAux(set(AnnotsAllAux(source, *skip_names).iter__annot_names())).check_assert(set(_EXPECTED[1]))
    ExpectAux(set(AnnotsLastAux(source, *skip_names).iter__annot_names())).check_assert(set(_EXPECTED[2]))


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (VictimAt(), [], [
            {},
            {},
            {},
        ]),
        (VictimAn(), [], [
            {2, 22, },
            {2, 22, },
            {2, 22, },
        ]),
        (VictimAnNest(), [], [
            {2, 22, 3, 33},
            {2, 22, 3, 33},
            {3, 33, },
        ]),
    ]
)
def test__ITER__iter__annot_values(source, skip_names, _EXPECTED):
    ExpectAux(set(AttrAux(source, *skip_names).iter__annot_values())).check_assert(set(_EXPECTED[0]))
    ExpectAux(set(AnnotsAllAux(source, *skip_names).iter__annot_values())).check_assert(set(_EXPECTED[1]))
    ExpectAux(set(AnnotsLastAux(source, *skip_names).iter__annot_values())).check_assert(set(_EXPECTED[2]))


# =====================================================================================================================
