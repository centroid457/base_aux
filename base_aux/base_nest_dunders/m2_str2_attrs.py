from typing import *

from base_aux.aux_attr.m1_annot_attr1_aux import AttrAux_Existed


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
        for attr_name in AttrAux_Existed(self).iter__names_filter__not_private():
            if result:
                result += ","
            elif not result:
                # result += f"{self.__class__.__name__}("
                result += f"ATTRS("
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
        for attr_name in AttrAux_Existed(self).iter__names_filter__not_hidden():
            if result:
                result += ","
            elif not result:
                # result += f"{self.__class__.__name__}("
                result += f"ATTRS("
            value = getattr(self, attr_name)
            result += f"{attr_name}={value}"

        result += ")"
        return result


# =====================================================================================================================
pass
pass
pass


class NestStR_AttrsPattern:
    """
    GOAL
    ----
    use pattern to make a special string for instance
    """
    NEST_STR__ATTR_PATTERN: str

    def __str__(self):
        return self.NEST_STR__ATTR_PATTERN.format(self)

    def __repr__(self):
        return str(self)


# =====================================================================================================================
def _examples() -> None:
    class Victim(NestStR_AttrsNotPrivate):
        A0: int
        A1: int = 1

    victim = Victim()
    print(victim)


    class Victim(NestStR_AttrsPattern):
        NEST_STR__ATTR_PATTERN = "A0={0.A0}, A1={0.A1}"
        A0: int = 0
        A1: int = 1

    victim = Victim()
    print(victim)


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
