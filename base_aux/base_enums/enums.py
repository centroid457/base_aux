from enum import Enum, auto


# =====================================================================================================================
"""
USAGE
-----
    if WHEN == When2.BEFORE:
        pass

"""


# =====================================================================================================================
class When2(Enum):
    BEFORE = auto()
    AFTER = auto()


class When3(Enum):
    BEFORE = auto()
    AFTER = auto()
    MIDDLE = auto()


# =====================================================================================================================
class Where2(Enum):
    FIRST = auto()
    LAST = auto()


class Where3(Enum):
    FIRST = auto()
    LAST = auto()
    MIDDLE = auto()


# =====================================================================================================================
class CallablesUse(Enum):
    DIRECT = auto()
    RESOLVE_EXX = auto()
    RESOLVE_RAISE = auto()

    SKIP = auto()
    RESOLVE_RAISE_SKIP = auto()


# =====================================================================================================================
class FormIntExt(Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    AttrAux show internal external names for PRIVATES
    """
    INTERNAL = auto()
    EXTERNAL = auto()


# =====================================================================================================================
