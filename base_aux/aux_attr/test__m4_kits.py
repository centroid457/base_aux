from typing import *
import pytest

from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
def test__values():
    class Example(Nest_AttrKit):
        A1: Any
        A2: Any = None
        A3 = None
        DICT: dict = {}

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

    # mutable
    victim = Example(1, 1, a3=1)
    assert victim.DICT == Example.DICT
    assert victim.DICT is not Example.DICT

    victim.DICT[1]=1
    assert victim.DICT[1] == 1
    assert victim.DICT != Example.DICT


# ---------------------------------------------------------------------------------------------------------------------
def test__eq():
    class Example:
        A0: Any
        A1: Any = 1

    assert AttrKit_Blank(a1=1) == Example()
    assert AttrKit_Blank(a1=11) != Example()
    assert AttrKit_Blank(a0=1) != Example()

    try:
        AttrKit_AuthTgBot(1)
        assert False
    except:
        assert True

    assert AttrKit_AuthTgBot(1, 2, 3).token == 3


# =====================================================================================================================
def test__cls_name():
    assert NestInit_AnnotsAttrByKwArgs().__class__.__name__ == f"NestInit_AnnotsAttrByKwArgs"

    class Victim(NestInit_AnnotsAttrByKwArgs):
        A1: Any = None

    assert Victim().__class__.__name__ == f"Victim"


# =====================================================================================================================
