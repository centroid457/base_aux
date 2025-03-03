from typing import *
import pytest

from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
def test__kits():
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
