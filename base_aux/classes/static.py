# GOAL
# KEEP STATIC OBJECTS like TYPE__* and Exx__* in separated file.
# make clear importing by resolving circular imports!
from typing import *


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
TYPE__LAMBDA_CONSTRUCTOR = Any | type[Any] | Callable[..., Any | NoReturn]
TYPE__LAMBDA_ARGS = tuple[Any, ...]
TYPE__LAMBDA_KWARGS = dict[str, Any]


# =====================================================================================================================
