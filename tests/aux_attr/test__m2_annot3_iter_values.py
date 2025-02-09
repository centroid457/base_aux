import pytest

from base_aux.aux_attr.m2_annot1_aux import *
from base_aux.aux_attr.m2_annot3_nest_iter_values import *
from base_aux.aux_attr.m1_attr2_nest_gsai_anycase import *


# =====================================================================================================================
class Victim1(NestGAI_AttrAnycase):
    ATTR1: int
    ATTR2: int = 2
    ATTR01 = 11


class Victim2(Victim1):
    ATTR3: int
    ATTR4: int = 4
    ATTR02 = 22


# =====================================================================================================================
class VictimIterValues(Victim2, NestIter_AnnotValues):
    pass


def test__nested_iter():
    assert list(VictimIterValues()) == [2, 4]


# =====================================================================================================================
