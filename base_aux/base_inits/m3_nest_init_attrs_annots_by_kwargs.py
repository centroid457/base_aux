from typing import *

from base_aux.aux_attr.m1_attr1_aux import *
from base_aux.aux_attr.m1_attr2_nest_gsai_anycase import *
from base_aux.base_statics.m4_enums import *
from base_aux.aux_attr.m2_annot1_aux import *


# =====================================================================================================================
class NestInit_AttrsByKwArgs_Base:
    """
    GOAL
    ----
    init attrs by dict model / template

    useful like creating simple object with exact attrs
    """
    ATTRS_SCOPE: AttrsScope = AttrsScope.ALL

    def __init__(self, *args, **kwargs) -> None | NoReturn:
        self.__init_args(*args)
        self.__init_kwargs(**kwargs)

    def __init_kwargs(self, **kwargs) -> None | NoReturn:
        for name, value in kwargs.items():
            if self.ATTRS_SCOPE == AttrsScope.ATTRS_ONLY:
                AttrAux(self).anycase__setattr(name, value)
            elif self.ATTRS_SCOPE == AttrsScope.ANNOTS_ONLY:
                AnnotsAux(self).set_value(name, value, only_annot=True)
            elif self.ATTRS_SCOPE == AttrsScope.ALL:
                AnnotsAux(self).set_value(name, value, only_annot=False)

    def __init_args(self, *args) -> None | NoReturn:
        kwargs = dict.fromkeys(args)
        self.__init_kwargs(**kwargs)


# =====================================================================================================================
class NestInit_AttrsAnnotsByKwArgs(NestInit_AttrsByKwArgs_Base):
    """
    NOTE
    ----
    BEST CHOICE! for all derivatives! all others can cause incorrect work - not clear!
    """
    ATTRS_SCOPE: AttrsScope = AttrsScope.ALL


class NestInit_AttrsAnnotsByKwArgsIC(NestInit_AttrsAnnotsByKwArgs, NestGSAI_AttrAnycase):
    """
    SAME AS - 1=parent
    -------
    but attrs access will be IgnoreCased
    """
    pass


# ---------------------------------------------------------------------------------------------------------------------
class NestInit_AttrsByKwArgs(NestInit_AttrsByKwArgs_Base):
    """
    NOTE
    ----
    use NestInit_AttrsAnnotsByKwArgs instead!
    """
    ATTRS_SCOPE: AttrsScope = AttrsScope.ATTRS_ONLY


# ---------------------------------------------------------------------------------------------------------------------
class NestInit_AnnotsByKwArgs(NestInit_AttrsByKwArgs_Base):
    """
    NOTE
    ----
    use NestInit_AttrsAnnotsByKwArgs instead!
    """
    ATTRS_SCOPE: AttrsScope = AttrsScope.ANNOTS_ONLY


# =====================================================================================================================
