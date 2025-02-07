# =====================================================================================================================
# USE COMMON/GENERAL TYPES

_std = [
    # base ----------------
    BaseException,
    Exception,
    BaseExceptionGroup,

    # imports -------------
    ImportError,
    ImportWarning,
    ModuleNotFoundError,

    # FILE/PATH
    FileExistsError,    # ExistsAlready
    FileNotFoundError,  # NotExists

    NotADirectoryError,
    IsADirectoryError,

    # USER ----------------
    UserWarning,
    Warning,
    DeprecationWarning,
    PendingDeprecationWarning,

    AssertionError,

    NotImplemented,
    NotImplementedError,

    # VALUE ---------------
    # type
    TypeError,

    # value
    ValueError,

    # syntax/format
    SyntaxWarning,
    SyntaxError,
    IndentationError,

    EOFError,
    TabError,
    BytesWarning,

    EncodingWarning,

    UnicodeWarning,
    UnicodeDecodeError,
    UnicodeEncodeError,
    UnicodeTranslateError,

    # ACCESS ------
    NameError,
    AttributeError,
    PermissionError,
    KeyError,
    IndexError,

    # COLLECTION
    GeneratorExit,
    StopIteration,
    StopAsyncIteration,

    # arithm/logic
    ZeroDivisionError,
    ArithmeticError,
    FloatingPointError,
    OverflowError,

    RecursionError,
    BrokenPipeError,
    InterruptedError,

    # CONNECTION
    ConnectionError,
    ConnectionAbortedError,
    ConnectionResetError,
    ConnectionRefusedError,
    TimeoutError,

    # OS/OTHER
    SystemExit,
    WindowsError,
    IOError,
    OSError,
    EnvironmentError,
    SystemError,
    ChildProcessError,
    MemoryError,
    KeyboardInterrupt,

    BufferError,
    LookupError,

    UnboundLocalError,

    RuntimeWarning,
    ResourceWarning,
    ReferenceError,
    ProcessLookupError,
    RuntimeError,
    FutureWarning,
    ExceptionGroup,
    BlockingIOError,

    # REAL VALUE = NOT AN EXCEPTION!!!
    NotImplemented,      # NotImplemented = None # (!) real value is 'NotImplemented'
]


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
class Exx__Valid(Exception):
    pass


class Exx__ValueNotValidated(Exx__Valid):
    pass


# =====================================================================================================================
class Exx__SameKeys(Exception):
    """Same keys NOT allowed!
    """


# =====================================================================================================================
