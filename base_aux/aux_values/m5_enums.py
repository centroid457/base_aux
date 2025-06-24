from base_aux.aux_values.m5_enum0_nest_eq import *


# =====================================================================================================================
class Enum_SingleMultiple(NestEq_Enum):
    NOT_EXISTS = None
    SINGLE = 1
    MULTIPLE = 2


class Enum_StaticCallable(NestEq_Enum):
    STATIC = 1
    CALLABLE = 2


# =====================================================================================================================
class Enum_When2(NestEq_Enum):
    BEFORE = 1
    AFTER = 2


class Enum_When3(NestEq_Enum):
    BEFORE = 1
    AFTER = 2
    MIDDLE = 3


# ---------------------------------------------------------------------------------------------------------------------
class Enum_Where2(NestEq_Enum):
    FIRST = 1
    LAST = 2


class Enum_Where3(NestEq_Enum):
    FIRST = 1
    LAST = 2
    MIDDLE = 3


# =====================================================================================================================
class Enum_CallResolveStyle(NestEq_Enum):
    DIRECT = 1
    EXX = 2
    RAISE = 3
    RAISE_AS_NONE = 4
    BOOL = 5

    SKIP_CALLABLE = 6
    SKIP_RAISED = 7


# =====================================================================================================================
class Enum_SourceOrigOrCopy(NestEq_Enum):
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
class Enum_IgnoreCase(NestEq_Enum):
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


# =====================================================================================================================
class Enum_ProcessResult(NestEq_Enum):
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


class Enum_ProcessStateActive(NestEq_Enum):
    """
    NAME
    ----
    STATE_ACTIVE
    """
    NONE = None
    STARTED = True
    FINISHED = False


class Enum_ProcessStateResult(NestEq_Enum):
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
class Enum_BoolCumulate(NestEq_Enum):
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


class Enum_PathType(NestEq_Enum):
    FILE = 1
    DIR = 2
    ALL = 3


# class AppendType(NestEq_Enum):
#     NEWLINE = 1


class Enum_AttemptsUsage(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    Base_ReAttempts/RExp
    """
    FIRST = None
    ALL = all


# =====================================================================================================================
class Enum_DictTextFormat(NestEq_Enum):
    AUTO = None     # by trying all variants
    EXTENTION = 0

    CSV = "csv"
    INI = "ini"
    JSON = "json"
    STR = "str"     # str(dict)


class Enum_TextStyle(NestEq_Enum):
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


class Enum_CmtStyle(NestEq_Enum):
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


class Enum_PatCoverStyle(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    TextAux.sub__regexp
    """
    NONE = None
    WORD = "word"
    LINE = "line"


# =====================================================================================================================
class Enum_NumType(NestEq_Enum):
    INT = int
    FLOAT = float
    BOTH = None


class Enum_NumFPoint(NestEq_Enum):
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


TYPING__FPOINT_DRAFT = Enum_NumFPoint | str | None


# =====================================================================================================================
class Enum_CmpType(NestEq_Enum):
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
class Enum_FormIntExt(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    AttrAux_Existed show internal external names for PRIVATES
    """
    INTERNAL = 1
    EXTERNAL = 2


class Enum_AttrAnnotsOrExisted(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    NestInit_AnnotsAttrsByKwArgs_Base for separating work with - TODO: DEPRECATE?
    """
    ATTRS_EXISTED = None
    ANNOTS_ONLY = 1


class Enum_AnnotsDepthAllOrLast(NestEq_Enum):
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


class Enum_AttrScope(NestEq_Enum):
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
class Enum_Os(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    ReqCheckStr_Os
    """
    LINUX = "linux"
    WINDOWS = "windows"


class Enum_MachineArch(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    ReqCheckStr_Os
    """
    PC = "amd64"        # standard PC
    WSL = "x86_64"      # wsl standard
    ARM = "aarch64"     # raspberry=ARM!


# =====================================================================================================================
# class Represent(NestEq_EnumNestEqIc_Enum):
#     NAME = 1
#     OBJECT = 2


# =====================================================================================================================
def _examples() -> None:
    WHEN = Enum_When2.BEFORE
    if WHEN is Enum_When2.BEFORE:
        pass

    print(Enum_NumFPoint.COMMA.name)
    print(Enum_NumFPoint.COMMA.value)
    print()
    print()

    print(Enum_NumFPoint.COMMA)  # Enum_NumFPoint.COMMA
    print(Enum_NumFPoint("."))  # Enum_NumFPoint.DOT

    print("." in Enum_NumFPoint)  # True
    print(Enum_NumFPoint.DOT in Enum_NumFPoint)  # True

    print(Enum_NumFPoint(".") == ".")  # True
    print(Enum_NumFPoint(Enum_NumFPoint.DOT))  # Enum_NumFPoint.DOT     # BEST WAY to init value!


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
