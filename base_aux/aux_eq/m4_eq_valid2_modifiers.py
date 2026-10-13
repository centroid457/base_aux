from base_aux.aux_eq.m3_eq_other2_validators import *
from base_aux.aux_eq.m4_eq_valid1_base import *
from base_aux.base_types.m0_static_types import *
from base_aux.base_enums.m2_enum1_adj import *


# ======================================================================================================================
class ModifierTry:
    """
    GOAL
    collect modifiers in separated object
    """
    def __init__(self, *args):
        self.modifiers: TYPING.MODIFIERS_TRY__FINAL = list(args)


# ======================================================================================================================
