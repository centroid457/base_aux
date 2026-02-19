from base_aux.loggers.m1_print import Warn


# =====================================================================================================================
# USE COMMON/GENERAL TYPES

_std = [
    # base ----------------
    AssertionError,

    # FILE/PATH
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
    TypeError,      # type
    ValueError,     # value

    # ACCESS ------
    PermissionError,

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

    # OS/OTHER
    SystemExit,
    # WindowsError,     # NOTE: NOT EXISTS IN LINUX!!! dont use in any variation!!!
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

    # PROCESS
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
class Base_Exc(
    Warn,

    Exception,
    # BaseException,    # DONT USE BASEEXCEPTION!!! or check all tests!
    # BaseExceptionGroup,
):
    """
    GOAL
    ----
    1/ with raise - just a solution to collect all dunder methods intended for Exceptions in one place
        - get correct bool() if get Exc as value
    2/ without raising - use like logger (Warn)

    SPECIALLY CREATED FOR
    ---------------------
    classes.VALID if
    """
    PREFIX: str = "[EXC]"


# =====================================================================================================================
class Exc__EncodeDecode(
    Base_Exc,

    # BytesWarning,
    # EncodingWarning,
    # UnicodeWarning,
    # UnicodeDecodeError,
    # UnicodeEncodeError,
    # UnicodeTranslateError,
):
    """
    GOAL
    ----
    collect all EncodeDecode Errors
    """
    pass


class Exc__Imports(
    Base_Exc,

    # ImportError,
    # ImportWarning,
    # ModuleNotFoundError,
):
    pass


class Exc__SyntaxFormat(
    Base_Exc,

    # SyntaxWarning,
    # SyntaxError,
    # IndentationError,
    #
    # EOFError,
    # TabError,
):
    pass


class Exc__Addressing(
    Base_Exc,

    # NameError,
    # AttributeError,
    # KeyError,
    # IndexError,
):
    pass


class Exc__NotExistsNotFoundNotCreated(
    Base_Exc,

    # FileExistsError,    # ExistsAlready
    # FileNotFoundError,  # NotExists
):
    """
    GOAL
    ----
    any exception intended Exists/NotExists any object
    dont mess with ADDRESSING!
    """
    pass


class Exc__NotAvailable(Exc__NotExistsNotFoundNotCreated):
    pass


# =====================================================================================================================
class Exc__UnDefined(Base_Exc):
    """
    GOAL
    ----
    Any not expected Exception!
    when we catch all exact variants and finally get not specified.
    """
    pass


class Exc__ExpectedAnother(Base_Exc):
    """
    GOAL
    ----
    Any requirement/exact cmp/eq is not match!
    """


# =====================================================================================================================
class Exc__Io(
    Base_Exc,

    # ConnectionError,
    # ConnectionAbortedError,
    # ConnectionResetError,
    # ConnectionRefusedError,
    # TimeoutError,
):
    """
    GOAL
    ----
    SPECIALLY CREATED FOR
    ---------------------
    CmdTerminal_OsAio._bg_reading_buffer
    to make a universal exceptions in different objects
    """
    pass


class Exc__IoConnection(
    Exc__Io,
):
    """
    GOAL
    ----
    Connection Broken/Closed while read/write process
    """
    pass


class Exc__IoTimeout(
    Exc__Io,
):
    """
    GOAL
    ----
    read/write process was timed out
    """
    pass


class Exc__IoCancel(
    Exc__Io,
):
    """
    GOAL
    ----
    read/write process was cancelled
    """
    pass


# =====================================================================================================================
class Exc__Permission(PermissionError):  # use original! but keep here new name!
    """
    GOAL
    ----
    catch exception and show that cause is permission!
    """
    pass


# =====================================================================================================================
class Exc__Incompatible(Base_Exc):
    """
    GOAL
    ----
    any incompatibility
    """
    pass


# ---------------------------------------------------------------------------------------------------------------------
class Exc__Incompatible_Data(Exc__Incompatible):
    pass


class Exc__Incompatible_Struct(Exc__Incompatible):
    """
    GOAL
    ----
    data has incorrect structure/schema

    SPECIALLY CREATED FOR
    ---------------------
    aio_testplan.TableObj._validate_schema
    """
    pass


# =====================================================================================================================
class Exc__WrongUsage(Base_Exc):
    """
    GOAL
    ----
    somebody perform incorrect usage!
    """


# ---------------------------------------------------------------------------------------------------------------------
class Exc__WrongUsage_Programmer(Exc__WrongUsage):
    """
    GOAL
    ----
    wrong programmer behaviour (smth about architecture)
    """
    pass


class Exc__WrongUsage_YouForgotSmth(Exc__WrongUsage_Programmer):
    """
    GOAL
    ----
    just a shallow error when you forget smth


    SPECIALLY CREATED FOR
    ---------------------
    ReleaseHistory - cause it is not Programmer
    """
    pass


# =====================================================================================================================
class Exc__Overlapped(Base_Exc):
    """
    GOAL
    ----
    ENY OVERLAPPED ITEMS/ADDRESSES
    index
    """
    pass


class Exc__NotReady(Base_Exc):
    """
    GOAL
    ----
    any not ready state/object
    connection/...
    """
    pass


# =====================================================================================================================
class Exc__GetattrPrefix(Base_Exc):
    pass


class Exc__GetattrPrefix_RaiseIf(Exc__GetattrPrefix):
    pass


class Exc__StartOuterNONE_UsedInStackByRecreation(Base_Exc):
    """
    in stack it will be recreate automatically! so dont use in pure single BreederStrSeries!
    """
    pass


# =====================================================================================================================
class Exc__NestingLevels(Base_Exc):
    """Exception when used several unsuitable levels in nesting!

    EXAMPLE:
        VictimBase = SingletonWMetaCall
        setattr(VictimBase, "attr", 0)
        class Victim1(VictimBase):
            attr = 1

        assert VictimBase().attr == 0
        try:
            assert Victim1().attr == 1
        except Exc_SingletonDifferentNestingLevels:
            pass
        else:
            assert False

    MAIN RULES:
    1. always instantiate only last Classes in your tree project!


    SPECIALLY CREATED FOR
    ---------------------
    Base_SingletonManager
    """
    pass


# =====================================================================================================================
if __name__ == '__main__':
    # WITH RAISING =====================================
    # REASON --------------
    assert bool(Exception(0)) is True
    assert bool(Exception(False)) is True

    # SOLUTION --------------
    assert bool(Base_Exc(0)) is False
    assert bool(Base_Exc(False)) is False

    # NO RAISING =====================================
    Base_Exc(0, 1, 2, 3)
    Warn(0, 1)


# =====================================================================================================================
