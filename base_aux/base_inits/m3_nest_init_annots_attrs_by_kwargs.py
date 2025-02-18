from typing import *

from base_aux.aux_attr.m1_attr1_aux import *
from base_aux.aux_attr.m1_attr2_nest_gsai_anycase import *
from base_aux.base_statics.m4_enums import *
from base_aux.aux_attr.m2_annot1_aux import *


# =====================================================================================================================
class NestInit_AnnotsAttrsByKwArgs:     # NOTE: dont create AnnotsOnly/AttrsOnly! always use this class!
    def __init__(self, *args: Any, **kwargs: TYPING.KWARGS_FINAL) -> None | NoReturn:
        AnnotsAux(self).set_values__by_args_kwargs(*args, **kwargs)


# =====================================================================================================================
class NestInit_AnnotsAttrByKwArgsIC(NestInit_AnnotsAttrsByKwArgs, NestGSAI_AttrAnycase):
    """
    SAME AS - 1=parent
    -------
    but attrs access will be IgnoreCased
    """
    pass


# =====================================================================================================================
