from typing import *

from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.aux_iter.m1_iter_aux import *


# =====================================================================================================================
class NestContains_AttrIcNoPrivate:
    """
    GOAL
    ----
    apply str/repr for show attrs names+values

    CAREFUL
    -------
    dont use in Nest* classes - it can used only in FINALs!!! cause it can have same or meaning is not appropriate!
    """
    def __contains__(self, item: Any) -> bool:
        return IterAux([*AttrAux(self).iter__names_filter__not_private()]).item__get_original(item) not in [NoValue, None]
        # return AttrAux(self).name_ic__check_exists(item)


# =====================================================================================================================
class NestContains_AttrIcNotHidden:
    """
    GOAL
    ----
    apply str/repr for show attrs names+values

    CAREFUL
    -------
    dont use in Nest* classes - it can used only in FINALs!!! cause it can have same or meaning is not appropriate!
    """
    def __contains__(self, item: Any):
        return IterAux([*AttrAux(self).iter__names_filter__not_hidden()]).item__get_original(item) not in [NoValue, None]


# =====================================================================================================================
