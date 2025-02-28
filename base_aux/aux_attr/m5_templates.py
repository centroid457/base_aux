from typing import *

from base_aux.base_inits.m3_nest_init_annots_attrs_by_kwargs import *
from base_aux.aux_attr.m2_annot1_aux import *


# =====================================================================================================================
class AttrTemplate_Direct(NestInit_AnnotsAttrByKwArgs, NestEq_Attrs):     # TODO: decide to delete! use only dynamic??
    """
    GOAL
    ----
    just show that child is just Template
    """

    # -----------------------------------------------------------------------------------------------------------------
    def __contains__(self, item: str) -> bool:
        return AttrAux(self).anycase__check_exists(item)

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self) -> str:
        result = f"{self.__class__.__name__}("

        for name, value in AttrAux(self).dump_dict(CallableResolve.DIRECT).items():
            if not result.endswith("("):
                result += ","
            result += f"{name}={value}"

        result += ")"
        return result

    def __repr__(self) -> str:
        return str(self)


# =====================================================================================================================
class AttrTemplate_Callable(AttrTemplate_Direct):
    """
    GOAL
    ----
    callables would resolve!
    """
    def __str__(self) -> str:
        result = f"{self.__class__.__name__}("

        for name, value in AttrAux(self).dump_dict(CallableResolve.EXX).items():
            if not result.endswith("("):
                result += ","
            result += f"{name}={value}"

        result += ")"
        return result

    def __repr__(self) -> str:
        result = f"{self.__class__.__name__}("

        for name, value in AttrAux(self).dump_dict(CallableResolve.DIRECT).items():
            if not result.endswith("("):
                result += ","
            result += f"{name}={value}"

        result += ")"
        return result


# =====================================================================================================================
