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


# ---------------------------------------------------------------------------------------------------------------------
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
    EXX = auto()
    RAISE = auto()
    RAISE_AS_NONE = auto()
    BOOL = auto()

    SKIP_CALLABLE = auto()
    SKIP_RAISED = auto()


# =====================================================================================================================
class Process(Enum):
    """
    GOAL
    ----
    define special values for methods

    SPECIALLY CREATED FOR
    ---------------------
    CallableAux.resolve when returns SKIPPED like object!
    """
    NONE = auto()
    STARTED = auto()
    SKIPPED = auto()
    STOPPED = auto()
    RAISED = auto()
    FAILED = auto()
    SUCCESS = auto()


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
class BoolCollect(Enum):
    """
    GOAL
    ----
    combine result for collection

    SPECIALLY CREATED FOR
    ---------------------
    EqValid_RegexpAllTrue
    """
    ALL_TRUE = auto()
    ANY_TRUE = auto()
    ANY_FALSE = auto()
    ALL_FALSE = auto()


# =====================================================================================================================
class FsObject(Enum):
    FILE = auto()
    DIR = auto()
    ALL = auto()


# ---------------------------------------------------------------------------------------------------------------------
class NumObject(Enum):
    INT = auto()
    FLOAT = auto()
    BOTH = auto()


# =====================================================================================================================
class CmpType(Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    path1_dirs.Dir.iter(timestamp)
    """
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()


# =====================================================================================================================
# class Represent(Enum):
#     NAME = auto()
#     OBJECT = auto()


# =====================================================================================================================
