import pytest

from base_aux.attrs import *


# =====================================================================================================================
class Victim1(AnnotAux):
    ATTR1: int
    ATTR2: int = 2
    ATTR01 = 11


class Victim2(Victim1):
    ATTR3: int
    ATTR4: int = 4
    ATTR02 = 22


# =====================================================================================================================
class VictimIterValues(Victim2, AnnotValuesIter):
    pass


def test__nested_iter():
    assert list(VictimIterValues()) == [2, 4]


# =====================================================================================================================
