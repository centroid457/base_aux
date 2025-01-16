from typing import Union, Any, Callable, NoReturn
from base_aux.base_argskwargs.m0_novalue import TYPE__NOVALUE


# =====================================================================================================================
TYPE__VALID_EXCEPTION = Union[Exception, type[Exception]]
TYPE__VALID_RESULT = Union[
    Any,
    TYPE__VALID_EXCEPTION,  # as main idea! instead of raise
]
# BOOL --------------------------------
TYPE__VALID_SOURCE_BOOL = Union[
    Any,                                # fixme: hide? does it need? for results like []/{}/()/0/"" think KEEP! it mean you must know that its expecting boolComparing in further logic!
    bool,                               # as main idea! as already final generic
    Callable[[...], bool | Any | NoReturn],   # as main idea! to get final generic
    # TYPE__VALID_EXCEPTION,
    TYPE__NOVALUE
]
TYPE__VALID_RESULT_BOOL = Union[
    # this is when you need get only bool! raise - as False!
    bool,  # as main idea! instead of raise/exx
]
# FIXME: TODO: solve idea of BOOL!!! cant understand about Exx in here!
TYPE__VALID_RESULT_BOOL__EXX = Union[
    bool,
    TYPE__VALID_EXCEPTION,
]

# ---------------------------------------------------------------------------------------------------------------------
TYPE__VALID_VALIDATOR = Union[
    Any,    # generic final instance as expecting value - direct comparison OR comparison instance like Valid!
    # Type,   # Class as validator like Valid? fixme
    TYPE__VALID_EXCEPTION,  # direct comparison
    Callable[[Any, ...], bool | NoReturn]     # func with first param for validating source
]


# =====================================================================================================================
TYPES_ELEMENTARY_SINGLE: tuple[type, ...] = (
    type(None), bool,
    str, bytes,
    int, float,
)
TYPES_ELEMENTARY_COLLECTION: tuple[type, ...] = (
    tuple, list,
    set, dict,
)
TYPES_ELEMENTARY: tuple[type, ...] = (*TYPES_ELEMENTARY_SINGLE, *TYPES_ELEMENTARY_COLLECTION, )
TYPE__ELEMENTARY = Union[*TYPES_ELEMENTARY]


# =====================================================================================================================
