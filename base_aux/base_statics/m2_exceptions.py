from base_aux.base_nest_dunders.m3_bool import *


# =====================================================================================================================
# USE COMMON/GENERAL TYPES

_std = [
    # base ----------------
    BaseException,
    Exception,
    BaseExceptionGroup,

    AssertionError,

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

    InterruptedError,

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
    PermissionError,

    NameError,
    AttributeError,
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
class Base_Exx(NestBool_False, Exception):
    """
    GOAL
    ----
    just a solution to collect all dunder methods intended for Exceptions in one place
     - get correct bool() if get Exx as value

    SPECIALLY CREATED FOR
    ---------------------
    classes.VALID if
    """
    pass


# =====================================================================================================================
class Exx__WrongUsage(Base_Exx):
    """
    GOAL
    ----
    you perform incorrect usage!

    SPECIALLY CREATED FOR
    ---------------------
    NoValue - never instantiate it! use value only as Class!
    """


class Exx__Incompatible(Base_Exx):
    pass


class Exx__OutOfRange(Base_Exx):
    pass


class Exx__Overlayed(Base_Exx):
    """
    GOAL
    ----
    ENY OVERLAY ITEMS/ADDRESSES
    index
    """
    pass


class Exx__NotExists(Base_Exx):
    pass


# =====================================================================================================================
class Exx__GetattrPrefix(Base_Exx):
    pass


class Exx__GetattrPrefix_RaiseIf(Exx__GetattrPrefix):
    pass


class Exx__ValueNotParsed(Base_Exx):
    pass


class Exx__StartOuterNONE_UsedInStackByRecreation(Base_Exx):
    """
    in stack it will be recreate automatically! so dont use in pure single BreederStrSeries!
    """
    pass


class Exx__BreederObjectList_GroupsNotGenerated(Base_Exx):
    pass


class Exx__BreederObjectList_GroupNotExists(Base_Exx):
    pass


# =====================================================================================================================
class Exx__Valid(Base_Exx):
    pass


class Exx__ValueNotValidated(Exx__Valid):
    pass


# =====================================================================================================================
if __name__ == '__main__':
    # REASON --------------
    assert bool(Exception(0)) is True
    assert bool(Exception(False)) is True

    # SOLUTION --------------
    assert bool(Base_Exx(0)) is False
    assert bool(Base_Exx(False)) is False


# =====================================================================================================================
