from typing import *
import pathlib
from base_aux.aux_values.m0_novalue import *


# =====================================================================================================================
class _Cls:
    def meth(self):
        pass


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
    DICT_ANY_ANY = dict[Any, Any]               # just to show - dict could be any! on keys/values
    DICT_STR_ANY = dict[str, Any]               # just to show - dict could be any! on values! not just an elementary1
    DICT_STR_ELEM = dict[str, ELEMENTARY]       # just to show - parsed by json - dict
    DICT_JSON_ANY = ELEMENTARY | DICT_STR_ELEM  # just to show - parsed by json - any object

    # -----------------------------------------------------------------------------------------------------------------


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
    NoValue
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
