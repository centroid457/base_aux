from typing import *
import pathlib

from base_aux.aux_values.m2_value_special import VALUE_SPECIAL
from base_aux.aux_types.m0_static_types import TYPES


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

    DICT_ANY_TUPLE_ANY = dict[Any, tuple[Any, ...]]     # as DICT_DIFF_DICTS
    DICT_STR_TUPLE_ANY = dict[str, tuple[Any, ...]]     # as DICT_DIFF_ATTRS

    # -----------------------------------------------------------------------------------------------------------------
    ITERABLE_ORDERED = Union[dict, list, tuple, Iterable]     # "SET" - DONT USE!
    ITERPATH_KEY = Union[Any, int]   # Any is for dict
    ITERPATH = tuple[ITERPATH_KEY, ...]

    # -----------------------------------------------------------------------------------------------------------------
    BOOL_DRAFT = Union[
        None,
        Any,                                # fixme: hide? does it need? for results like []/{}/()/0/"" think KEEP! it mean you must know that its expecting boolComparing in further logic!
        bool,                               # as main idea! as already final generic
        Exception,
        Callable[..., bool | Any | NoReturn | Exception],   # as main idea! to get final generic
        VALUE_SPECIAL.NOVALUE
    ]

    # -----------------------------------------------------------------------------------------------------------------
    RESULT__NONE = None
    RESULT__BOOL = bool
    RESULT__EXX = Exception     # | type[Exception] - DONT USE typeExx! from any process Exception comes as instance!

    RESULT__ANY_EXX = Any | Exception
    RESULT__ANY_RAISE = Any | NoReturn

    RESULT__BOOL_NONE = bool | None
    RESULT__BOOL_RAISE = bool | NoReturn
    RESULT__BOOL_EXX = bool | Exception
    RESULT__RAISE_NONE = NoReturn | None

    RESULT__BOOL_RAISE_NONE = bool | NoReturn | None

    # -----------------------------------------------------------------------------------------------------------------
    EXPECTED = bool | type[Any | Exception] | Any

    # -----------------------------------------------------------------------------------------------------------------
    CALLABLE__NONE = Callable[..., None]
    CALLABLE__BOOL = Callable[..., bool]
    CALLABLE__EXX = Callable[..., Exception]

    CALLABLE__BOOL_NONE = Callable[..., bool | None]
    CALLABLE__BOOL_RAISE = Callable[..., bool | NoReturn]
    CALLABLE__BOOL_EXX = Callable[..., bool | Exception]
    CALLABLE__RAISE_NONE = Callable[..., NoReturn | None]  # not expecting any bool! intended/inportant only raising as inappropriate position!

    CALLABLE__BOOL_RAISE_NONE = Callable[..., bool | NoReturn | None]


# =====================================================================================================================
TYPING__VALID_VALIDATOR = Union[
    Any,    # generic final instance as expecting value - direct comparison OR comparison instance like Valid!
    # Type,   # Class as validator like Exception????? fixme
    type[Exception],  # direct comparison
    Callable[[Any, ...], bool | NoReturn]     # func with first param for validating source
]


# =====================================================================================================================
TYPING__LAMBDA_CONSTRUCTOR = Union[Any, type[Any], Callable[..., Any | NoReturn]]
_TYPING__LAMBDA_BOOL = Union[Any, Callable[..., bool | NoReturn]]


# =====================================================================================================================
