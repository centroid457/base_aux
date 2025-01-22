from typing import *


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
