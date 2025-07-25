from typing import *
import pytest

from base_aux.aux_attr.m4_kits2_stable_keyset import *


# =====================================================================================================================
def test__1():
    try:
        victim = AttrKit_StableKeySet(1, a1=1)
    except:
        pass
    else:
        assert False

    victim = AttrKit_StableKeySet(a1=1)

    assert victim.A1 == 1
    assert victim.a1 == 1

    victim(a1=11)
    assert victim.A1 == 11
    assert victim.a1 == 11

    victim(A1=1)
    assert victim.A1 == 1
    assert victim.a1 == 1

    victim(11)
    assert victim.A1 == 11
    assert victim.a1 == 11

    victim(1, a1=111)
    assert victim.A1 == 111
    assert victim.a1 == 111

    victim(1, a1=111, A1=1111)
    assert victim.A1 == 1111
    assert victim.a1 == 1111

    try:
        victim(11, 22)
    except:
        pass
    else:
        assert False

    try:
        victim(a2=22)
    except:
        pass
    else:
        assert False

    try:
        victim(1, a1=11, a2=22)
    except:
        pass
    else:
        assert False


# =====================================================================================================================
