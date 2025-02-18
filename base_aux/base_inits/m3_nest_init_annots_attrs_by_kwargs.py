from typing import *

from base_aux.aux_attr.m1_attr1_aux import *
from base_aux.aux_attr.m1_attr2_nest_gsai_anycase import *
from base_aux.base_statics.m4_enums import *
from base_aux.aux_attr.m2_annot1_aux import *


# =====================================================================================================================
class NestInit_AnnotsAttrsByKwArgs:     # NOTE: dont create AnnotsOnly/AttrsOnly! always use this class!
    """
    NOTE
    ----
    for more understanding application/logic use annots at first place! and dont mess them. keep your code clear!
        class Cls(NestInit_AnnotsAttrsByKwArgs):
            A1: Any
            A2: Any
            A3: Any = 1
            A4: Any = 1

    GOAL
    ----
    init annots/attrs by params in __init__

    LOGIC
    -----
    args
        - used for annots only - used as values! not names!
        - inited first without Kwargs sense
    kwargs
        - used for both annots/attrs (annots are preferred)

    annots are always preferred!

    useful like creating simple object with exact attrs
    """
    def __init__(self, *args: Any, **kwargs: TYPING.KWARGS_FINAL) -> None | NoReturn:
        self.__init_args(*args)
        self.__init_kwargs(**kwargs)

    def __init_kwargs(self, **kwargs: TYPING.KWARGS_FINAL) -> None | NoReturn:  # NoReturn is only in case of noneStr keys!
        for name, value in kwargs.items():
            AnnotsAux(self).set_value(name, value, only_annot=False)

    def __init_args(self, *args: Any) -> None:
        """
        ARGS - ARE VALUES! not names!

        IF ARGS MORE then Annots - NoRaise! # FIXME: decide?
        """
        for name, value in zip(AnnotsAux(self).iter_names(), args):
            self.__init_kwargs(**{name: value})


# =====================================================================================================================
class NestInit_AnnotsAttrByKwArgsIC(NestInit_AnnotsAttrsByKwArgs, NestGSAI_AttrAnycase):
    """
    SAME AS - 1=parent
    -------
    but attrs access will be IgnoreCased
    """
    pass


# =====================================================================================================================
