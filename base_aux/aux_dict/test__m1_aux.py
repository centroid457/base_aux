import pytest

from base_aux.aux_dict.m1_dict_aux import *
from base_aux.base_statics.m4_enums import *
from base_aux.base_statics.m3_primitives import LAMBDA_ECHO
from base_aux.aux_expect.m1_expect_aux import *


# =====================================================================================================================
DICT_LU = {
    "lower": "lower",
    "UPPER": "UPPER",
}
VICTIM_DEF = {
    1: {1: 1, 2: 2, 3: 3},
    2: {1: 1, 2: 2},
    3: {1: 1},
    4: 4,
    **DICT_LU
}


def test__collapse_key():
    VICTIM = VICTIM_DEF.copy()

    victim = DictAuxInline(VICTIM)
    victim = victim.collapse_key(4)
    assert victim == VICTIM
    assert victim[1] == {1: 1, 2: 2, 3: 3}
    assert victim[2] == {1: 1, 2: 2}
    assert victim[3] == {1: 1}
    assert victim[4] == 4

    victim = DictAuxInline(VICTIM)
    victim = victim.collapse_key(3)
    assert victim == VICTIM
    assert victim[1] == 3
    assert victim[2] == {1: 1, 2: 2}
    assert victim[3] == {1: 1}
    assert victim[4] == 4

    victim = DictAuxInline(VICTIM)
    victim = victim.collapse_key(2)
    assert victim == VICTIM
    assert victim[1] == 3
    assert victim[2] == 2
    assert victim[3] == {1: 1}
    assert victim[4] == 4


def test__clear_values():
    VICTIM = VICTIM_DEF.copy()

    victim = DictAuxCopy(VICTIM).clear_values()
    assert victim != VICTIM
    assert victim == dict.fromkeys(VICTIM)
    assert victim[4] == None
    assert VICTIM[4] == 4

    victim = DictAuxInline(VICTIM).clear_values()
    assert victim == VICTIM
    assert victim == dict.fromkeys(VICTIM)
    assert victim[4] == None
    assert VICTIM[4] == None


def test__keys_del():
    VICTIM = VICTIM_DEF.copy()

    key = 4444
    assert key not in VICTIM
    DictAuxInline(VICTIM).keys_del(key)

    key = 4
    assert key in VICTIM
    assert VICTIM[4] == 4
    DictAuxInline(VICTIM).keys_del(key)
    assert key not in VICTIM


def test__keys_rename__by_func():
    VICTIM = VICTIM_DEF.copy()
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    victim = DictAuxCopy(VICTIM).keys_rename__by_func(LAMBDA_ECHO)
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    assert list(victim) == [*range(1, 5), *DICT_LU]

    # ================================
    VICTIM = VICTIM_DEF.copy()
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    victim = DictAuxCopy(VICTIM).keys_rename__by_func(str.lower)
    assert VICTIM != victim
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    assert list(victim) == [*range(1, 5), "lower", "upper"]

    # --------------------------------
    VICTIM = VICTIM_DEF.copy()
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    victim = DictAuxCopy(VICTIM).keys_rename__by_func(str.upper)
    assert VICTIM != victim
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    assert list(victim) == [*range(1, 5), "LOWER", "UPPER"]

    # ================================
    VICTIM = VICTIM_DEF.copy()
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    victim = DictAuxInline(VICTIM).keys_rename__by_func(str.lower)
    assert VICTIM == victim
    assert list(VICTIM) == [*range(1, 5), "lower", "upper"]
    assert list(victim) == [*range(1, 5), "lower", "upper"]


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, func, walk, _EXPECTED",
    argvalues=[
        ({1:1, 2:{11:11}}, str, False, {"1":1, "2":{11:11}}),
        ({1:1, 2:{11:11}}, str, True, {"1":1, "2":{"11":11}}),
        ({1:1, 2:{11:{111: 222}}}, str, True, {"1":1, "2":{"11":{"111":222}}}),
        ({1:1, 2:{11:[111, {1111:2222}]}}, str, True, {"1":1, "2": {"11": [111, {"1111": 2222}]}}),
    ]
)
def test__keys_rename__by_func__walk(source, func, walk, _EXPECTED):
    func_link = DictAuxCopy(source).keys_rename__by_func
    ExpectAux(func_link, (func, walk)).check_assert(_EXPECTED)
    assert source != _EXPECTED      # check original is not changed


# =====================================================================================================================
