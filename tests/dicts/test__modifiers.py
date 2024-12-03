from typing import *
import pytest

from base_aux.dicts import *


# =====================================================================================================================
VICTIM = {
    1: {1: 1, 2: 2, 3: 3},
    2: {1: 1, 2: None},
    3: {1: 1},
    4: 4,
}


def test__collapse_key():
    victim = Dicts(VICTIM)
    victim = victim.collapse_key(4)
    assert victim == VICTIM
    assert victim[1] == {1: 1, 2: 2, 3: 3}
    assert victim[4] == 4

    victim = Dicts(VICTIM)
    victim = victim.collapse_key(3)
    assert victim != VICTIM
    assert victim[1] == 3
    assert victim[4] == 4


# =====================================================================================================================
