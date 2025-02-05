# =====================================================================================================================
# USE COMMON/GENERAL TYPES

_std = [
# base ----
BaseException,
Exception,

# USER ----
UserWarning,
BytesWarning,
Warning,
DeprecationWarning,
PendingDeprecationWarning,

AssertionError,

NotImplemented,
NotImplementedError,

# std ------
TypeError,
NameError,
ValueError,
AttributeError,

SyntaxWarning,
SyntaxError,

# imports -----
ImportError,
ImportWarning,
ModuleNotFoundError,

# PATH
NotADirectoryError,
IsADirectoryError,

# std logic
GeneratorExit,
StopIteration,
SystemExit,

# arithm
ZeroDivisionError,
ArithmeticError,
FloatingPointError,
OverflowError,

# OS
WindowsError,
IOError,
OSError,
EnvironmentError,
SystemError,
PermissionError,
ChildProcessError,
MemoryError,

KeyError,
KeyboardInterrupt,

FileExistsError,
FileNotFoundError,

ConnectionError,
ConnectionAbortedError,
ConnectionResetError,
ConnectionRefusedError,
TimeoutError,
EOFError,
BufferError,

LookupError,
IndexError,

EncodingWarning,

UnicodeWarning,
UnicodeDecodeError,
UnicodeEncodeError,
UnicodeTranslateError,

UnboundLocalError,
TabError,

BrokenPipeError,

StopAsyncIteration,
RuntimeWarning,
ResourceWarning,
ReferenceError,
RecursionError,
ProcessLookupError,
RuntimeError,
InterruptedError,
IndentationError,
FutureWarning,
ExceptionGroup,
BlockingIOError,
BaseExceptionGroup,

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
