from base_aux.base_enums.m1_enum0_nest_eq import *


# =====================================================================================================================
class EnumAdj_SingleMultiple(NestEq_EnumAdj):
    NOT_EXISTS = None
    SINGLE = 1
    MULTIPLE = 2


class EnumAdj_StaticCallable(NestEq_EnumAdj):
    STATIC = 1
    CALLABLE = 2


# =====================================================================================================================
class EnumAdj_When2(NestEq_EnumAdj):
    BEFORE = 1
    AFTER = 2


class EnumAdj_When3(NestEq_EnumAdj):
    BEFORE = 1
    AFTER = 2
    MIDDLE = 3


# ---------------------------------------------------------------------------------------------------------------------
class EnumAdj_Where2(NestEq_EnumAdj):
    FIRST = 1
    LAST = 2


class EnumAdj_Where3(NestEq_EnumAdj):
    FIRST = 1
    LAST = 2
    MIDDLE = 3


# =====================================================================================================================
class EnumAdj_CallResolveStyle(NestEq_EnumAdj):
    DIRECT = 1
    EXC = 2
    RAISE = 3
    RAISE_AS_NONE = 4
    BOOL = 5

    SKIP_CALLABLE = 6
    SKIP_RAISED = 7


class EnumAdj_ReturnOnRaise(NestEq_EnumAdj):
    """
    GOAL
    ----
    select what to return on raise

    SPECIALLY CREATED FOR
    ---------------------
    ChainResolve
    """
    RAISE = 1
    NONE = 2
    EXC = 3


# =====================================================================================================================
class EnumAdj_SourceOrigOrCopy(NestEq_EnumAdj):
    """
    GOAL
    ----
    define where work process in original source or copy

    SPECIALLY CREATED FOR
    ---------------------
    DictAuxInline/Deepcopy
    """
    ORIGINAL = True
    COPY = False


# =====================================================================================================================
class EnumAdj_IgnoreCase(NestEq_EnumAdj):
    """
    GOAL
    ----
    replace many bool params about case sensing

    SPECIALLY CREATED FOR
    ---------------------
    Meta_ClsGaAnnotNamesAsValuesIc
    """
    IGNORECASE = True
    CASESENSE = False


class EnumAdj__TextCaseStyle(NestEq_EnumAdj):
    """
    GOAL
    ----
    select the representation for text

    SPECIALLY CREATED FOR
    ---------------------
    StrIc
    """
    ORIGINAL: int = 0
    LOWER: int = 1
    UPPER: int = 2


# =====================================================================================================================
class EnumAdj_ProcessResult(NestEq_EnumAdj):
    """
    GOAL
    ----
    define special values for methods

    SPECIALLY CREATED FOR
    ---------------------
    CallableAux.resolve when returns SKIPPED like object!
    """
    NONE = None
    SKIPPED = 1
    STOPPED = 2
    RAISED = 3
    FAILED = False
    SUCCESS = True


class EnumAdj_ProcessStateActive(NestEq_EnumAdj):
    """
    NAME
    ----
    STATE_ACTIVE
    """
    NONE = None
    STARTED = True
    FINISHED = False


class EnumAdj_ProcessStateResult(NestEq_EnumAdj):
    """
    GOAL
    ----
    use processActive+Result in one value

    SPECIALLY CREATED FOR
    ---------------------
    1/ VALID
    2/ tc.startup_cls/teardown_cls
    """
    NONE = None
    STARTED = 0
    FINISHED_FAIL = False
    FINISHED_SUCCESS = True


# =====================================================================================================================
class EnumAdj_StopResetHardSoft(NestEq_EnumAdj):
    SOFT: int = 1
    HARD: int = 2


# ---------------------------------------------------------------------------------------------------------------------
class EnumAdj_Buffer(NestEq_EnumAdj):
    STDIN: int = 1
    STDOUT: int = 2
    STDERR: int = 3
    DEBUG: int = 9


class EnumAdj_FinishedStatus(NestEq_EnumAdj):
    """
    SPECIALLY CREATED FOR
    ---------------------
    CmdResult
    """
    NOT_FINISHED: int = 0
    CORRECT: int = 1

    TIMED_OUT: int = 10
    EXCEPTION: int = 11


# =====================================================================================================================
class EnumAdj_BoolCumulate(NestEq_EnumAdj):
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
    ALL_FALSE = 1
    ANY_FALSE = 2


class EnumAdj_PathType(NestEq_EnumAdj):
    FILE = 1
    DIR = 2
    ALL = 3


# class AppendType(NestEq_EnumAdj):
#     NEWLINE = 1


class EnumAdj_AttemptsUsage(NestEq_EnumAdj):
    """
    SPECIALLY CREATED FOR
    ---------------------
    Base_ReAttempts/RExp
    """
    FIRST = None
    ALL = all


class EnumAdj_TypeIteration(NestEq_EnumAdj):
    """
    SPECIALLY CREATED FOR
    ---------------------
    CmdSession_old
    """
    ALL = None
    TILL_FIRST_FAIL = 1
    TILL_FIRST_OK = 2


# =====================================================================================================================
class EnumAdj_DictTextFormat(NestEq_EnumAdj):
    AUTO = None     # by trying all variants
    EXTENTION = 0

    CSV = "csv"
    INI = "ini"
    JSON = "json"
    STR = "str"     # str(dict)


class EnumAdj_TextStyle(NestEq_EnumAdj):
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


class EnumAdj_CmtStyle(NestEq_EnumAdj):
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
    C = "c"             # /*...*/
    SEMICOLON = ";"     # for INI files


class EnumAdj_PatCoverStyle(NestEq_EnumAdj):
    """
    SPECIALLY CREATED FOR
    ---------------------
    TextAux.sub__regexp
    """
    NONE = None
    WORD = "word"
    LINE = "line"


# =====================================================================================================================
class EnumAdj_NumType(NestEq_EnumAdj):
    INT = int
    FLOAT = float
    BOTH = None


class EnumAdj_NumFPoint(NestEq_EnumAdj):
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


TYPING__FPOINT_DRAFT = EnumAdj_NumFPoint | str | None


# =====================================================================================================================
class EnumAdj_CmpType(NestEq_EnumAdj):
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
class EnumAdj_FormIntExt(NestEq_EnumAdj):
    """
    SPECIALLY CREATED FOR
    ---------------------
    AttrAux_Existed show internal external names for PRIVATES
    """
    INTERNAL = 1
    EXTERNAL = 2


class EnumAdj_AttrAnnotsOrExisted(NestEq_EnumAdj):
    """
    SPECIALLY CREATED FOR
    ---------------------
    NestInit_AnnotsAttrsByKwArgs_Base for separating work with - TODO: DEPRECATE?
    """
    ATTRS_EXISTED = None
    ANNOTS_ONLY = 1


class EnumAdj_AnnotsDepthAllOrLast(NestEq_EnumAdj):
    """
    GOAL
    ----
    need to separate work with last/allNested annots!

    SPECIALLY CREATED FOR
    ---------------------
    Base_ReqCheckStr
    """
    ALL_NESTED = None
    LAST_CHILD = 1


class EnumAdj_AttrScope(NestEq_EnumAdj):
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
    WHEN = EnumAdj_When2.BEFORE
    if WHEN is EnumAdj_When2.BEFORE:
        pass

    print(EnumAdj_NumFPoint.COMMA.name)
    print(EnumAdj_NumFPoint.COMMA.value)
    print()
    print()

    print(EnumAdj_NumFPoint.COMMA)  # EnumAdj_NumFPoint.COMMA
    print(EnumAdj_NumFPoint("."))  # EnumAdj_NumFPoint.DOT

    print("." in EnumAdj_NumFPoint)  # True
    print(EnumAdj_NumFPoint.DOT in EnumAdj_NumFPoint)  # True

    print(EnumAdj_NumFPoint(".") == ".")  # True
    print(EnumAdj_NumFPoint(EnumAdj_NumFPoint.DOT))  # EnumAdj_NumFPoint.DOT     # BEST WAY to init value!


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
