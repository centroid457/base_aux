from typing import *

from base_aux.base_statics.m2_exceptions import *
from base_aux.base_statics.m1_types import *
from base_aux.aux_iter.m1_iter_aux import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.aux_types.m1_type_aux import *

from base_aux.base_inits.m1_nest_init_source import *
from base_aux.aux_attr.m1_attr1_aux import *


# =====================================================================================================================
@final
class AnnotAttrAux(AttrAux):
    """
    GOAL
    ----
    work with all __annotations__
        from all nested classes
        in correct order

    RULES
    -----
    1. nesting available with correct order!
        class ClsFirst(BreederStrStack):
            atr1: int
            atr3: int = None

        class ClsLast(BreederStrStack):
            atr2: int = None
            atr4: int

        for key, value in ClsLast.annotations__get_nested().items():
            print(f"{key}:{value}")

        # atr1:<class 'int'>
        # atr3:<class 'int'>
        # atr2:<class 'int'>
        # atr4:<class 'int'>
    """
    def ITER_NAMES_SOURCE(self) -> Iterable[str]:
        yield from self.iter__annot_names()


# =====================================================================================================================
