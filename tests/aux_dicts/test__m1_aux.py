from typing import *
import pytest

from base_aux.aux_dict.m1_dict_aux import *
from base_aux.base_enums.m0_enums import FormIntExt
from base_aux.base_objects.m0_primitives import LAMBDA_ECHO


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

    victim = DictAux(VICTIM)
    victim = victim.collapse_key(4)
    assert victim == VICTIM
    assert victim[1] == {1: 1, 2: 2, 3: 3}
    assert victim[2] == {1: 1, 2: 2}
    assert victim[3] == {1: 1}
    assert victim[4] == 4

    victim = DictAux(VICTIM)
    victim = victim.collapse_key(3)
    assert victim != VICTIM
    assert victim[1] == 3
    assert victim[2] == {1: 1, 2: 2}
    assert victim[3] == {1: 1}
    assert victim[4] == 4

    victim = DictAux(VICTIM)
    victim = victim.collapse_key(2)
    assert victim != VICTIM
    assert victim[1] == 2
    assert victim[2] == 2
    assert victim[3] == {1: 1}
    assert victim[4] == 4


def test__clear_values():
    VICTIM = VICTIM_DEF.copy()

    victim = DictAux(VICTIM).clear_values(FormIntExt.EXTERNAL)
    assert victim != VICTIM
    assert victim == dict.fromkeys(VICTIM)
    assert victim[4] == None
    assert VICTIM[4] == 4

    victim = DictAux(VICTIM).clear_values(FormIntExt.INTERNAL)
    assert victim == VICTIM
    assert victim == dict.fromkeys(VICTIM)
    assert victim[4] == None
    assert VICTIM[4] == None


def test__keys_del():
    VICTIM = VICTIM_DEF.copy()

    key = 4444
    assert key not in VICTIM
    DictAux(VICTIM).keys_del(key)

    key = 4
    assert key in VICTIM
    assert VICTIM[4] == 4
    DictAux(VICTIM).keys_del(key)
    assert key not in VICTIM


def test__keys_rename__by_func():
    VICTIM = VICTIM_DEF.copy()
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    victim = DictAux(VICTIM).keys_rename__by_func(LAMBDA_ECHO, form=FormIntExt.EXTERNAL)
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    assert list(victim) == [*range(1, 5), *DICT_LU]

    # ================================
    VICTIM = VICTIM_DEF.copy()
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    victim = DictAux(VICTIM).keys_rename__by_func(str.lower, form=FormIntExt.EXTERNAL)
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    assert list(victim) == ["lower", "upper"]

    # --------------------------------
    VICTIM = VICTIM_DEF.copy()
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    victim = DictAux(VICTIM).keys_rename__by_func(str.upper, form=FormIntExt.EXTERNAL)
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    assert list(victim) == ["LOWER", "UPPER"]

    # ================================
    VICTIM = VICTIM_DEF.copy()
    assert list(VICTIM) == [*range(1, 5), *DICT_LU]
    victim = DictAux(VICTIM).keys_rename__by_func(str.lower, form=FormIntExt.INTERNAL)
    assert list(VICTIM) == ["lower", "upper"]
    assert list(victim) == ["lower", "upper"]


# =====================================================================================================================
