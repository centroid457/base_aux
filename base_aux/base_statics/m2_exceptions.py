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
class Exx__BoolBase(Exception):
    """
    just a solution to get correct bool() if get Exx as value

    SPECIALLY CREATED FOR
    ---------------------
    classes.VALID if
    """
    def __bool__(self):
        return False


# =====================================================================================================================
class Exx__WrongUsage(Exx__BoolBase):
    """
    GOAL
    ----
    you perform incorrect usage!

    SPECIALLY CREATED FOR
    ---------------------
    NoValue - never instantiate it! use value only as Class!
    """


class Exx__Incompatible(Exx__BoolBase):
    pass


class Exx__OutOfRange(Exx__BoolBase):
    pass


# =====================================================================================================================
class Exx__AnnotNotDefined(Exx__BoolBase):
    """Exception in case of not defined attribute in instance
    """


class Exx__NumberArithm_NoName(Exx__BoolBase):
    pass


class Exx__GetattrPrefix(Exx__BoolBase):
    pass


class Exx__GetattrPrefix_RaiseIf(Exx__GetattrPrefix):
    pass


class Exx__ValueNotParsed(Exx__BoolBase):
    pass


class Exx__ValueUnitsIncompatible(Exx__BoolBase):
    pass


class Exx__IndexOverlayed(Exx__BoolBase):
    pass


class Exx__IndexNotSet(Exx__BoolBase):
    pass


class Exx__ItemNotExists(Exx__BoolBase):
    """
    not exists INDEX (out of range) or NAME not in defined values
    """
    pass


class Exx__StartOuterNONE_UsedInStackByRecreation(Exx__BoolBase):
    """
    in stack it will be recreate automatically! so dont use in pure single BreederStrSeries!
    """
    pass


class Exx__BreederObjectList_GroupsNotGenerated(Exx__BoolBase):
    pass


class Exx__BreederObjectList_GroupNotExists(Exx__BoolBase):
    pass


class Exx__BreederObjectList_ObjCantAccessIndex(Exx__BoolBase):
    pass


# =====================================================================================================================
class Exx__Valid(Exx__BoolBase):
    pass


class Exx__ValueNotValidated(Exx__Valid):
    pass


# =====================================================================================================================
class Exx__SameKeys(Exx__BoolBase):
    """Same keys NOT allowed!
    """


# =====================================================================================================================
if __name__ == '__main__':
    # REASON --------------
    assert bool(Exception(0)) is True
    assert bool(Exception(False)) is True

    # SOLUTION --------------
    assert bool(Exx__BoolBase(0)) is False
    assert bool(Exx__BoolBase(False)) is False


# =====================================================================================================================
