from typing import *

from base_aux.aux_attr.m2_annot1_aux import *


# =====================================================================================================================
class Init_AnnotsByTypes_All:
    """
    GOAL
    ----
    when create class with only annots
    and need to init instance with default attr values like dict/list/set/...

    SPECIALLY CREATED FOR
    ---------------------
    game1_noun5letters.CharMask
    """
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        AnnotsAux(self).values__reinit_by_types(False)


# =====================================================================================================================
class Init_AnnotsByTypes_NotExisted:
    """
    GOAL
    ----
    same as Init_AnnotsByTypes_All but for only not existed values
    """
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        AnnotsAux(self).values__reinit_by_types(True)


# =====================================================================================================================
