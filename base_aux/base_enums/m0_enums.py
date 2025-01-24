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
    EXCEPTION = auto()
    RAISE = auto()
    RAISE_AS_NONE = auto()
    BOOL = auto()

    SKIP_CALLABLE = auto()
    SKIP_RAISED = auto()


# =====================================================================================================================
class CallableFinish(Enum):
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
    RAISED = auto()
    SKIPPED = auto()
    STOPPED = auto()
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
class BoolCollection(Enum):
    """
    GOAL
    ----
    combine result for collection

    SPECIALLY CREATED FOR
    ---------------------
    EqValid_Regexp
    """
    ALL = auto()
    ANY = auto()
    NOT_ANY = auto()
    NOT_ALL = auto()


# =====================================================================================================================
