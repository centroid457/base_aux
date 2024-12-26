from typing import *
import pytest

from base_aux.dicts import *


# =====================================================================================================================
VICTIM = {
    1: {1: 1, 2: 2, 3: 3},
    2: {1: 1, 2: 2},
    3: {1: 1},
    4: 4,
}


def test__collapse_key():
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
    victim = DictAux(VICTIM)
    victim = victim.clear_values()
    assert victim != VICTIM
    assert victim == dict.fromkeys(VICTIM)


# =====================================================================================================================
