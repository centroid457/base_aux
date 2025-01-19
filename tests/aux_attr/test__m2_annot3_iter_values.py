import pytest

from base_aux.aux_attr.m2_annot1_aux import *
from base_aux.aux_attr.m2_annot3_iter_values import *


# =====================================================================================================================
class Victim1(AnnotsBase):
    ATTR1: int
    ATTR2: int = 2
    ATTR01 = 11


class Victim2(Victim1):
    ATTR3: int
    ATTR4: int = 4
    ATTR02 = 22


# =====================================================================================================================
class VictimIterValues(Victim2, AnnotsValuesIter):
    pass


def test__nested_iter():
    assert list(VictimIterValues()) == [2, 4]


# =====================================================================================================================
