from typing import *

from base_aux.aux_attr.m1_annot_attr1_aux import *


# =====================================================================================================================
class NestLen_AttrNotPrivate:
    """
    GOAL
    ----
    apply str/repr for show attrs names+values

    CAREFUL
    -------
    dont use in Nest* classes - it can used only in FINALs!!! cause it can have same or meaning is not appropriate!
    """
    def __len__(self) -> int:
        return len([*AttrAux_Existed(self).iter__names_filter__not_private()])


# =====================================================================================================================
class NestLen_AttrNotHidden:
    def __len__(self) -> int:
        return len([*AttrAux_Existed(self).iter__names_filter__not_hidden()])


# =====================================================================================================================
