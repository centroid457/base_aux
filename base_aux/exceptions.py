from typing import *


# =====================================================================================================================
class ExxBool(Exception):
    """
    just a solution to bet correct bool if get Exx as value

    SPECIALLY CREATED FOR
    ---------------------
    classes.VALID if
    """
    def __bool__(self):
        return False


# =====================================================================================================================
if __name__ == '__main__':
    # REASON --------------
    assert bool(Exception(0)) is True
    assert bool(Exception(False)) is True

    # SOLUTION --------------
    assert bool(ExxBool(0)) is False
    assert bool(ExxBool(False)) is False


# =====================================================================================================================
class Exx__AnnotNotDefined(Exception):
    """Exception in case of not defined attribute in instance
    """


class Exx__NumberArithm_NoName(Exception):
    pass


class Exx__GetattrPrefix(Exception):
    pass


class Exx__GetattrPrefix_RaiseIf(Exx__GetattrPrefix):
    pass


class Exx__ValueNotParsed(Exception):
    pass


class Exx__ValueUnitsIncompatible(Exception):
    pass


class Exx__IndexOverlayed(Exception):
    pass


class Exx__IndexNotSet(Exception):
    pass


class Exx__ItemNotExists(Exception):
    """
    not exists INDEX (out of range) or NAME not in defined values
    """
    pass


class Exx__StartOuterNONE_UsedInStackByRecreation(Exception):
    """
    in stack it will be recreate automatically! so dont use in pure single BreederStrSeries!
    """
    pass


class Exx__BreederObjectList_GroupsNotGenerated(Exception):
    pass


class Exx__BreederObjectList_GroupNotExists(Exception):
    pass


class Exx__BreederObjectList_ObjCantAccessIndex(Exception):
    pass


# =====================================================================================================================
