from base_aux.base_statics.m4_enum0_nest_eq import *


# =====================================================================================================================
"""
see _examples below and tests to understand work
"""


# =====================================================================================================================
class When2(NestEq_Enum):
    BEFORE = 1
    AFTER = 2


class When3(NestEq_Enum):
    BEFORE = 1
    AFTER = 2
    MIDDLE = 3


# ---------------------------------------------------------------------------------------------------------------------
class Where2(NestEq_Enum):
    FIRST = 1
    LAST = 2


class Where3(NestEq_Enum):
    FIRST = 1
    LAST = 2
    MIDDLE = 3


# =====================================================================================================================
class CallableResolve(NestEq_Enum):
    DIRECT = 1
    EXX = 2
    RAISE = 3
    RAISE_AS_NONE = 4
    BOOL = 5

    SKIP_CALLABLE = 6
    SKIP_RAISED = 7


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
    STARTED = 1
    SKIPPED = 2
    STOPPED = 3
    RAISED = 4
    FAILED = False
    SUCCESS = True


# =====================================================================================================================
class FormIntExt(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    AttrAux show internal external names for PRIVATES
    """
    INTERNAL = 1
    EXTERNAL = 2


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
    ANY_FALSE = 1
    ALL_FALSE = 2


# =====================================================================================================================
class PathType(NestEq_Enum):
    FILE = 1
    DIR = 2
    ALL = 3


# ---------------------------------------------------------------------------------------------------------------------
# class AppendType(NestEq_Enum):
#     NEWLINE = 1


# ---------------------------------------------------------------------------------------------------------------------
class DictTextFormat(NestEq_Enum):
    AUTO = None     # by trying all variants
    EXTENTION = 0

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
    TXT = "txt"

    PY = "py"
    C = "c"
    BAT = "bat"
    SH = "sh"

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
    C = "c"     # /*...*/


# ---------------------------------------------------------------------------------------------------------------------
class PatCoverStyle(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    TextAux.sub__regexp
    """
    NONE = None
    WORD = "word"
    LINE = "line"


class AttemptsUsage(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    Re/RExp
    """
    FISRT = None
    ALL = all


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
    LT = 1
    LE = 2
    GT = 3
    GE = 4


# =====================================================================================================================
class AttrStyle(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    NestInit_AnnotsAttrsByKwArgs_Base for separating work with - TODO: DEPRECATE?
    """
    ATTRS_EXISTED = None
    ANNOTS_ONLY = 1


class AttrLevel(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    AttrKit_Blank
    """
    NOT_HIDDEN = None
    NOT_PRIVATE = 1
    ALL = 2

    PRIVATE = 3    # usually not used! just in case!


# =====================================================================================================================
# class Represent(NestEq_EnumNestEqIc_Enum):
#     NAME = 1
#     OBJECT = 2


# =====================================================================================================================
def _examples() -> None:
    WHEN = When2.BEFORE
    if WHEN is When2.BEFORE:
        pass

    print(FPoint.COMMA)  # FPoint.COMMA
    print(FPoint("."))  # FPoint.DOT

    print("." in FPoint)  # True
    print(FPoint.DOT in FPoint)  # True

    print(FPoint(".") == ".")  # True
    print(FPoint(FPoint.DOT))  # FPoint.DOT     # BEST WAY to init value!


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
