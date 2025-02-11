from typing import *
import pathlib

from base_aux.aux_values.m0_novalue import TYPE__NOVALUE


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
    collect all types variants
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


# ---------------------------------------------------------------------------------------------------------------------
TYPE__ELEMENTARY = Union[*TYPES.ELEMENTARY]


# DRAFTS ==============================================================================================================
TYPE__PATH_DRAFT = Union[str, pathlib.Path]
TYPE__PATH_FINAL = pathlib.Path

TYPE__STR_DRAFT = Union[str, Any]
TYPE__STR_FINAL = str


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
    TYPE__NOVALUE
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

TYPE__ARGS_FINAL = tuple[Any, ...]
TYPE__KWARGS_FINAL = dict[str, Any]

# VALUES --------------------------------------------------------------------------------------------------------------
ARGS_FINAL__NOT_USED = ()     # just to show that here it is not used
KWARGS_FINAL__NOT_USED = {}   # just to show that here it is not used

ARGS_FINAL__BLANK = ()     # just to show that here it is not used
KWARGS_FINAL__BLANK = {}   # just to show that here it is not used


# =====================================================================================================================
TYPE__DICT_ANY = dict[Any, Any]                         # just to show - dict could be any!
TYPE__JSON_DICT = dict[str, TYPE__ELEMENTARY]           # just to show - parsed by json - dict
TYPE__JSON_ANY = TYPE__ELEMENTARY | TYPE__JSON_DICT     # just to show - parsed by json - any object


# =====================================================================================================================
