from typing import *

from base_aux.aux_attr.m1_annot_attr1_aux import *


# =====================================================================================================================
class NestInit_Mutable:
    """
    GOAL
    ----
    reinit mutable values

    NOTE
    ----
    use simple copy past method!
    """
    def __init__(self, *args, **kwargs) -> None:
        AttrAux(self).reinit__mutable_values()  # keep on first step!!! reinit only selfValues! not classvalues!
        super().__init__(*args, **kwargs)


# =====================================================================================================================
def test__reinit_mutables():
    # check common way ---------
    CONST = {}
    CONST2 = {1:1}

    assert {} == {}
    assert {} is not {}
    assert CONST is CONST

    assert {1:1} == {1:1}
    assert {1:1} is not {1:1}
    assert CONST2 is CONST2

    # NEW WAY -------------------
    class Victim:
        LIST = []
        SET = {}
        DICT = {}

    class Victim2(Victim, NestInit_Mutable):
        pass

    victim = Victim()
    assert victim.LIST == Victim.LIST
    assert victim.LIST is Victim.LIST

    victim2 = Victim2()
    assert victim2.LIST == Victim2.LIST
    assert victim2.LIST is not Victim2.LIST


# =====================================================================================================================
