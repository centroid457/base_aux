import sys
from base_aux.base_nest_dunders.m3_bool import *


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
class Warn(
    NestBool_False,
):
    """
    GOAL
    ----
    when you dont want to use logger and raise error (by now).
    print msg in some inner functions when raising Exx after inner function return False.

    SPECIALLY CREATED FOR
    ---------------------
    ReleaseHistory.check_new_release__is_correct/generate

    TODO: try use direct logger?
        or rename nito some new class! as universal Msging!
    """
    PREFIX: str = "[WARN]"
    INDENT: str = "__"
    EOL: str = "\n"
    MSG_LINES: tuple[str, ...]

    def __init__(self, *lines, prefix: str = None, **kwargs) -> None:
        if prefix is not None:
            self.PREFIX = prefix

        self.MSG_LINES = lines
        print(self, file=sys.stderr)

        super().__init__(**kwargs)

    def __str__(self):
        return self.MSG_STR

    @property
    def MSG_STR(self) -> str:
        result = f"{self.PREFIX}"
        for index, line in enumerate(self.MSG_LINES):
            if index == 0:
                result += f"{line}"
            else:
                result += f"{self.EOL}{self.INDENT}{line}"

        return result


# =====================================================================================================================
class Base_Exx(
    Warn,

    Exception,
    # BaseException,
    # BaseExceptionGroup,
):
    """
    GOAL
    ----
    1/ with raise - just a solution to collect all dunder methods intended for Exceptions in one place
        - get correct bool() if get Exx as value
    2/ without raising - use like logger (Warn)

    SPECIALLY CREATED FOR
    ---------------------
    classes.VALID if
    """
    PREFIX: str = "[EXX]"


# =====================================================================================================================
class Exx__EncodeDecode(
    Base_Exx,

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


class Exx__Connection(
    Base_Exx,

    # ConnectionError,
    # ConnectionAbortedError,
    # ConnectionResetError,
    # ConnectionRefusedError,
    # TimeoutError,
):
    pass


class Exx__Imports(
    Base_Exx,

    # ImportError,
    # ImportWarning,
    # ModuleNotFoundError,
):
    pass


class Exx__SyntaxFormat(
    Base_Exx,

    # SyntaxWarning,
    # SyntaxError,
    # IndentationError,
    #
    # EOFError,
    # TabError,
):
    pass


class Exx__Addressing(
    Base_Exx,

    # NameError,
    # AttributeError,
    # KeyError,
    # IndexError,
):
    pass


class Exx__NotExistsNotFoundNotCreated(
    Base_Exx,

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


# =====================================================================================================================
class Exx__WrongUsage(Base_Exx):
    """
    GOAL
    ----
    somebody perform incorrect usage!
    """


class Exx__WrongUsage_Programmer(Exx__WrongUsage):
    """
    GOAL
    ----
    wrong programmer behaviour (smth about architecture)
    """
    pass


class Exx__WrongUsage_YouForgotSmth(Exx__WrongUsage_Programmer):
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
class Exx__Expected(Base_Exx):
    """
    GOAL
    ----
    Any requirement/exact cmp/eq
    """


class Exx__Overlayed(Base_Exx):
    """
    GOAL
    ----
    ENY OVERLAY ITEMS/ADDRESSES
    index
    """
    pass


class Exx__NotReady(Base_Exx):
    pass


# =====================================================================================================================
class Exx__Incompatible(Base_Exx):
    pass


# =====================================================================================================================
class Exx__GetattrPrefix(Base_Exx):
    pass


class Exx__GetattrPrefix_RaiseIf(Exx__GetattrPrefix):
    pass


class Exx__StartOuterNONE_UsedInStackByRecreation(Base_Exx):
    """
    in stack it will be recreate automatically! so dont use in pure single BreederStrSeries!
    """
    pass


# =====================================================================================================================
class Exx__Valid(Base_Exx):
    pass


class Exx__ValueNotValidated(Exx__Valid):
    pass


# =====================================================================================================================
class Exx__NestingLevels(Base_Exx):
    """Exception when used several unsuitable levels in nesting!

    EXAMPLE:
        VictimBase = SingletonWMetaCall
        setattr(VictimBase, "attr", 0)
        class Victim1(VictimBase):
            attr = 1

        assert VictimBase().attr == 0
        try:
            assert Victim1().attr == 1
        except Exx_SingletonDifferentNestingLevels:
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
    assert bool(Base_Exx(0)) is False
    assert bool(Base_Exx(False)) is False

    # NO RAISING =====================================
    Base_Exx(0, 1, 2, 3)
    Warn(0, 1)


# =====================================================================================================================
