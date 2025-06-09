from typing import *
import pathlib
from base_aux.aux_values.m0_value_special import *


# =====================================================================================================================
class _Cls:
    def meth(self):
        pass
    @property
    def prop(self):
        return


def _explore():
    print(isinstance(_Cls.prop, property))  # True
    print(type(_Cls.prop))  # <class 'property'>
    print(type(_Cls().prop))  # <class 'NoneType'>


# =====================================================================================================================
OBJ_NAMES__BUILTINS = tuple(dir(globals().get("__builtins__")))
"""
('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BaseExceptionGroup', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception', 'ExceptionGroup', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip')
"""


# COLLECTIONS =========================================================================================================
@final
class TYPES:
    """
    GOAL
    ----
    collect all types USEFUL variants
    """
    # SINGLE ---------------------------
    NONE: type = type(None)
    NUMBER = int | float

    FUNCTION: type = type(lambda: True)
    METHOD: type = type(_Cls().meth)
    # PROPERTY: type    # cant check by type
    # MODULE: type    # cant check by type - only by method!

    # COLLECTIONS ---------------------------
    ELEMENTARY_SINGLE: tuple[type, ...] = (
        type(None),
        bool,
        int, float,
        str, bytes,
    )
    ELEMENTARY_COLLECTION: tuple[type, ...] = (
        tuple, list,
        set, dict,
    )
    ELEMENTARY: tuple[type, ...] = (
        *ELEMENTARY_SINGLE,
        *ELEMENTARY_COLLECTION,
    )


# =====================================================================================================================
@final
class TYPING:
    """
    GOAL
    ----
    collect all typing USER variants
    """
    ELEMENTARY = Union[*TYPES.ELEMENTARY]

    # -----------------------------------------------------------------------------------------------------------------
    ARGS_FINAL = tuple[Any, ...]
    ARGS_DRAFT = Union[Any, ARGS_FINAL, 'ArgsKwargs']           # you can use direct single value

    KWARGS_FINAL = dict[str, Any]
    KWARGS_DRAFT = Union[None, KWARGS_FINAL, 'ArgsKwargs']  # if passed NONE - no data!

    # -----------------------------------------------------------------------------------------------------------------
    PATH_FINAL = pathlib.Path
    PATH_DRAFT = Union[str, PATH_FINAL]

    STR_FINAL = str
    STR_DRAFT = Union[STR_FINAL, Any]

    # -----------------------------------------------------------------------------------------------------------------
    DICT_ANY_NONE = dict[Any, None]             # just to show - dict with None values after clearing!
    DICT_ANY_ANY = dict[Any, Any]               # just to show - dict could be any! on keys/values
    DICT_STR_ANY = dict[str, Any]               # just to show - dict could be any! on values! not just an elementary1
    DICT_STR_ELEM = DICT_JSON_ANY = dict[str, ELEMENTARY]       # just to show - parsed by json - dict
    DICT_STR_STR = DICT_INI = dict[str, str]               # just to show - parsed by ini!
    JSON_ANY = ELEMENTARY | DICT_STR_ELEM  # just to show - parsed by json - any object

    # -----------------------------------------------------------------------------------------------------------------
    ORDERED_ITERABLE = Union[dict, list, tuple, Iterable]     # "SET" - DONT USE!
    ITERPATH_KEY = Union[Any, int]   # Any is for dict
    ITERPATH = tuple[ITERPATH_KEY, ...]

    # -----------------------------------------------------------------------------------------------------------------
    RESULT__NONE = None
    RESULT__BOOL = bool

    RESULT__BOOL_NONE = bool | None
    RESULT__BOOL_RAISE = bool | NoReturn
    RESULT__RAISE_NONE = NoReturn | None

    RESULT__BOOL_RAISE_NONE = bool | NoReturn | None

    # -----------------------------------------------------------------------------------------------------------------
    CALLABLE__NONE = Callable[..., None]
    CALLABLE__BOOL = Callable[..., bool]

    CALLABLE__BOOL_NONE = Callable[..., bool | None]
    CALLABLE__BOOL_RAISE = Callable[..., bool | NoReturn]
    CALLABLE__RAISE_NONE = Callable[..., NoReturn | None]    # not expecting any bool! intended/inportant only raising as inappropriate position!

    CALLABLE__BOOL_RAISE_NONE = Callable[..., bool | NoReturn | None]


# VALUES --------------------------------------------------------------------------------------------------------------
ARGS_FINAL__BLANK = ()
KWARGS_FINAL__BLANK = {}


# VALIDS ==============================================================================================================
TYPE__VALID_EXX = Union[Exception, type[Exception]]
TYPE__VALID_RESULT = Union[
    Any,
    TYPE__VALID_EXX,  # as main idea! instead of raise
]
TYPE__VALID_BOOL__DRAFT = Union[
    Any,                                # fixme: hide? does it need? for results like []/{}/()/0/"" think KEEP! it mean you must know that its expecting boolComparing in further logic!
    bool,                               # as main idea! as already final generic
    Callable[[...], bool | Any | NoReturn],   # as main idea! to get final generic
    TYPE__VALID_EXX,
    VALUE_SPECIAL.NOVALUE
]
TYPE__VALID_BOOL__FINAL = Union[
    # this is when you need get only bool! raise - as False!
    bool,  # as main idea! instead of raise/exx
]
TYPE__VALID_BOOL_EXX__FINAL = Union[
    bool,
    TYPE__VALID_EXX,
]
# TYPE__VALID_TRUE__FINAL = Union[

TYPE__VALID_VALIDATOR = Union[
    Any,    # generic final instance as expecting value - direct comparison OR comparison instance like Valid!
    # Type,   # Class as validator like Exception????? fixme
    type[Exception],  # direct comparison
    Callable[[Any, ...], bool | NoReturn]     # func with first param for validating source
]


# =====================================================================================================================
TYPE__LAMBDA_CONSTRUCTOR = Union[Any, type[Any], Callable[..., Any | NoReturn]]
_TYPE__LAMBDA_BOOL = Union[Any, Callable[..., bool | NoReturn]]


# =====================================================================================================================
