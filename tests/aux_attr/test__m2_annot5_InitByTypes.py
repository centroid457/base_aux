import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux
from base_aux.aux_attr.m2_annot4_cls_keys_as_values import *


# =====================================================================================================================
class Victim(AnnotClsKeysAsValues):
    ATTR1: str
    ATTR2: str
    ATTR3: str


Victim_VALUES = ("ATTR1", "ATTR2", "ATTR3")


# =====================================================================================================================


# =====================================================================================================================
