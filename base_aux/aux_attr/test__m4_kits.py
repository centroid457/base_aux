from typing import *
import pytest

from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
def test__values():
    class Victim(Base_AttrKit):
        A1: Any
        A2: Any = None
        A3 = None
        DICT: dict = {}

    try:
        Victim()
    except:
        pass
    else:
        assert False

    assert Victim(a1=1).A1 == 1
    assert Victim(A1=1).a1 == 1
    assert Victim(1).a1 == 1
    assert Victim(1).A1 == 1

    assert Victim(1, a1=2).A1 == 2

    assert Victim(1).A1 == 1
    assert Victim(1).A2 == None
    assert Victim(1).A3 == None

    assert Victim(1, 1, 1).A1 == 1
    assert Victim(1, 1, 1).A2 == 1
    assert Victim(1, 1, 1).A3 == None
    assert Victim(1, 1, a3=1).A3 == 1

    # mutable
    victim = Victim(1, 1, a3=1)
    assert victim.DICT == Victim.DICT
    assert victim.DICT is not Victim.DICT

    victim.DICT[1]=1
    assert victim.DICT[1] == 1
    assert victim.DICT != Victim.DICT


# ---------------------------------------------------------------------------------------------------------------------
def test__eq():
    class Victim:
        A0: Any
        A1: Any = 1

    assert AttrKit_Blank(a1=1) != Victim()
    assert AttrKit_Blank(A1=1) == Victim()
    assert AttrKit_Blank(a1=11) != Victim()
    assert AttrKit_Blank(a0=1) != Victim()

    try:
        AttrKit_AuthTgBot(1)
    except:
        pass
    else:
        assert False

    assert AttrKit_AuthTgBot(1, 2, 3).token == 3


# =====================================================================================================================
def test__cls_name():
    assert NestInit_AnnotsAttr_ByArgsKwargs().__class__.__name__ == f"NestInit_AnnotsAttr_ByArgsKwargs"

    class Victim(NestInit_AnnotsAttr_ByArgsKwargs):
        A1: Any = None

    assert Victim().__class__.__name__ == f"Victim"


# =====================================================================================================================
