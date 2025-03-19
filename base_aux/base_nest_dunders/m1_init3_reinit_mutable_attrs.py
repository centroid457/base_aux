from typing import *

from base_aux.aux_attr.m1_annot_attr1_aux import *


# =====================================================================================================================
class NestInit_Mutable:
    """
    GOAL
    ----
    reinit mutable values

    NOTE
    ----
    use simple copy past method!
    """
    def __init__(self, *args, **kwargs) -> None:
        AttrAux(self).reinit__mutable_values()  # keep on first step!!! reinit only classvalues!
        super().__init__(*args, **kwargs)


# =====================================================================================================================
