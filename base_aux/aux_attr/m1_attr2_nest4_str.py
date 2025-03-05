from typing import *

from base_aux.aux_attr.m1_attr1_aux import AttrAux


# =====================================================================================================================
class NestStR_AttrsNotPrivate:
    """
    GOAL
    ----
    apply str/repr for show attrs names+values

    CAREFUL
    -------
    dont use in Nest* classes - it can used only in FINALs!!! cause it can have same or meaning is not appropriate!
    """
    def __str__(self):  # it can used only in FINAL!!! dont use in Nest*!!!
        result = ""
        for attr_name in AttrAux(self).iter__attrs_not_private():
            if result:
                result += ","
            elif not result:
                result += f"{self.__class__.__name__}("
            value = getattr(self, attr_name)
            result += f"{attr_name}={value}"

        result += ")"
        return result

    def __repr__(self):       # it can used only in FINAL!!! dont use in Nest*!!!
        return str(self)


# =====================================================================================================================
class NestStR_AttrsNotHidden:
    """
    GOAL
    ----
    apply str/repr for show attrs names+values

    CAREFUL
    -------
    dont use in Nest* classes - it can used only in FINALs!!! cause it can have same or meaning is not appropriate!
    """
    def __str__(self):  # it can used only in FINAL!!! dont use in Nest*!!!
        result = ""
        for attr_name in AttrAux(self).iter__attrs_not_hidden():
            if result:
                result += ","
            elif not result:
                result += f"{self.__class__.__name__}("
            value = getattr(self, attr_name)
            result += f"{attr_name}={value}"

        result += ")"
        return result


# =====================================================================================================================
