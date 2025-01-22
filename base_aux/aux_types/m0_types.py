from typing import *
from typing import Union, Any, Callable, NoReturn

from base_aux.aux_values.m0_novalue import TYPE__NOVALUE


# =====================================================================================================================
class _Cls:
    def meth(self):
        pass


# =====================================================================================================================
@final
class TYPES:
    """
    GOAL
    ----
    collect all types variants
    """

    # SINGLE ---------------------------
    NONE: type = type(None)
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
TYPE__ELEMENTARY = Union[*TYPES.ELEMENTARY]


# =====================================================================================================================
TYPE__VALID_EXX = Union[Exception, type[Exception]]
TYPE__VALID_RESULT = Union[
    Any,
    TYPE__VALID_EXX,  # as main idea! instead of raise
]
TYPE__VALID_SOURCE_BOOL = Union[
    Any,                                # fixme: hide? does it need? for results like []/{}/()/0/"" think KEEP! it mean you must know that its expecting boolComparing in further logic!
    bool,                               # as main idea! as already final generic
    Callable[[...], bool | Any | NoReturn],   # as main idea! to get final generic
    # TYPE__VALID_EXX,
    TYPE__NOVALUE
]
TYPE__VALID_RESULT_BOOL = Union[
    # this is when you need get only bool! raise - as False!
    bool,  # as main idea! instead of raise/exx
]
TYPE__VALID_RESULT_BOOL__EXX = Union[
    bool,
    TYPE__VALID_EXX,
]
TYPE__VALID_VALIDATOR = Union[
    Any,    # generic final instance as expecting value - direct comparison OR comparison instance like Valid!
    # Type,   # Class as validator like Valid? fixme
    TYPE__VALID_EXX,  # direct comparison
    Callable[[Any, ...], bool | NoReturn]     # func with first param for validating source
]


# =====================================================================================================================
