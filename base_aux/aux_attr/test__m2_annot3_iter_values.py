import pytest

from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.aux_attr.m2_annot2_nest3_iter_values import *
from base_aux.aux_attr.m2_annot2_nest1_gsai_ic import *


# =====================================================================================================================
class Victim1(NestIter_AnnotValues):
    ATTR1: int
    ATTR2: int = 2
    ATTR01 = 11


class Victim2(Victim1):
    ATTR3: int
    ATTR4: int = 4
    ATTR02 = 22


# =====================================================================================================================
def test__nested_iter():
    assert list([*Victim1()]) == [2, ]
    assert list([*Victim2()]) == [2, 4]


# =====================================================================================================================
