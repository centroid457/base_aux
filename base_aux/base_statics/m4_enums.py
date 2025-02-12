from enum import Enum, auto

from base_aux.aux_values.m0_novalue import *


# =====================================================================================================================
"""
USAGE
-----
if WHEN == When2.BEFORE:
    pass
    

print(FPoint.COMMA)     # FPoint.COMMA
print(FPoint("."))      # FPoint.DOT

print("." in FPoint)            # True
print(FPoint.DOT in FPoint)     # True

print(FPoint(".") == ".")      # False
print(FPoint(FPoint.DOT))      # FPoint.DOT     # BEST WAY to init value!


MAKE A DEFAULT NONE VALUE
-------------------------
class FPoint(Enum):
    DOT = "."
    COMMA = ","
    AUTO = None     # def! when FPoint(None)
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
    NONE = None
    STARTED = auto()
    SKIPPED = auto()
    STOPPED = auto()
    RAISED = auto()
    FAILED = False
    SUCCESS = True


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
class BoolCumulate(Enum):
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
class PathType(Enum):
    FILE = auto()
    DIR = auto()
    ALL = auto()


# ---------------------------------------------------------------------------------------------------------------------
# class AppendType(Enum):
#     NEWLINE = auto()


# ---------------------------------------------------------------------------------------------------------------------
class DictTextFormat(Enum):
    AUTO = None

    CSV = "csv"
    INI = "ini"
    JSON = "json"
    STR = "str"     # str(dict)


class TextFormat(Enum):
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


class CmtType(Enum):
    AUTO = None     # keep decide?
    ALL = all

    SHARP = "#"
    DSLASH = "//"
    REM = "rem"


class PatCoverType(Enum):
    DIRECT = auto()
    WORD = auto()
    LINE = auto()


# ---------------------------------------------------------------------------------------------------------------------
class NumType(Enum):
    INT = int
    FLOAT = float
    BOTH = None


# =====================================================================================================================
class FPoint(Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    TextAux.parse__single_number
    """
    DOT = "."
    COMMA = ","
    AUTO = None     # auto is more important for SingleNum!


TYPE__FPOINT_DRAFT = FPoint | str | None


# =====================================================================================================================
class CmpType(Enum):
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
# class Represent(Enum):
#     NAME = auto()
#     OBJECT = auto()


# =====================================================================================================================
