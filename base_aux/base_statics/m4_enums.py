from enum import Enum, auto

from base_aux.base_statics.m4_enum0_nest_eq import *


# =====================================================================================================================
"""
see _examples below and tests to understand work
"""


# =====================================================================================================================
class When2(NestEq_Enum):
    BEFORE = auto()
    AFTER = auto()


class When3(NestEq_Enum):
    BEFORE = auto()
    AFTER = auto()
    MIDDLE = auto()


# ---------------------------------------------------------------------------------------------------------------------
class Where2(NestEq_Enum):
    FIRST = auto()
    LAST = auto()


class Where3(NestEq_Enum):
    FIRST = auto()
    LAST = auto()
    MIDDLE = auto()


# =====================================================================================================================
class CallableResolve(NestEq_Enum):
    DIRECT = auto()
    EXX = auto()
    RAISE = auto()
    RAISE_AS_NONE = auto()
    BOOL = auto()

    SKIP_CALLABLE = auto()
    SKIP_RAISED = auto()


# =====================================================================================================================
class ProcessState(NestEq_Enum):
    """
    GOAL
    ----
    define special values for methods

    SPECIALLY CREATED FOR
    ---------------------
    CallableAux.resolve when returns SKIPPED like object!
    """
    NONE = None
    STARTED = auto()
    SKIPPED = auto()
    STOPPED = auto()
    RAISED = auto()
    FAILED = False
    SUCCESS = True


# =====================================================================================================================
class FormIntExt(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    AttrAux show internal external names for PRIVATES
    """
    INTERNAL = auto()
    EXTERNAL = auto()


# =====================================================================================================================
class BoolCumulate(NestEq_Enum):
    """
    GOAL
    ----
    combine result for collection

    SPECIALLY CREATED FOR
    ---------------------
    EqValid_RegexpAllTrue
    """
    ALL_TRUE = all
    ANY_TRUE = any
    ANY_FALSE = auto()
    ALL_FALSE = auto()


# =====================================================================================================================
class PathType(NestEq_Enum):
    FILE = auto()
    DIR = auto()
    ALL = auto()


# ---------------------------------------------------------------------------------------------------------------------
# class AppendType(NestEq_Enum):
#     NEWLINE = auto()


# ---------------------------------------------------------------------------------------------------------------------
class DictTextFormat(NestEq_Enum):
    AUTO = None

    CSV = "csv"
    INI = "ini"
    JSON = "json"
    STR = "str"     # str(dict)


class TextStyle(NestEq_Enum):
    ANY = any       # keep decide?
    AUTO = None     # keep decide?

    CSV = "csv"
    INI = "ini"
    JSON = "json"

    PY = "py"
    BAT = "bat"
    REQ = "requirements"
    GITIGNORE = "gitignore"
    MD = "md"


class CmtStyle(NestEq_Enum):
    """
    GOAL
    ----
    select
    """
    AUTO = None     # keep decide?
    ALL = all

    SHARP = "#"
    DSLASH = "//"
    REM = "rem"


class PatCoverStyle(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    TextAux.sub__regexp
    """
    NONE = None
    WORD = "word"
    LINE = "line"


# ---------------------------------------------------------------------------------------------------------------------
class NumType(NestEq_Enum):
    INT = int
    FLOAT = float
    BOTH = None


# =====================================================================================================================
class FPoint(NestEq_Enum):
    """
    GOAL
    ----
    floating point style

    SPECIALLY CREATED FOR
    ---------------------
    TextAux.parse__single_number
    """
    DOT = "."
    COMMA = ","
    AUTO = None     # auto is more important for SingleNum!


TYPE__FPOINT_DRAFT = FPoint | str | None


# =====================================================================================================================
class CmpType(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    path1_dirs.DirAux.iter(timestamp)
    """
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()


# =====================================================================================================================
class AttrsScope(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    AttrAux for separating/defining, but maybe not needed
    """
    ALL = None
    EXISTED_ONLY = auto()
    ANNOTS_ONLY = auto()


# =====================================================================================================================
# class Represent(NestEq_Enum):
#     NAME = auto()
#     OBJECT = auto()


# =====================================================================================================================
def _examples() -> None:
    WHEN = When2.BEFORE
    if WHEN == When2.BEFORE:
        pass

    print(FPoint.COMMA)  # FPoint.COMMA
    print(FPoint("."))  # FPoint.DOT

    print("." in FPoint)  # True
    print(FPoint.DOT in FPoint)  # True

    print(FPoint(".") == ".")  # False
    print(FPoint(FPoint.DOT))  # FPoint.DOT     # BEST WAY to init value!


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
