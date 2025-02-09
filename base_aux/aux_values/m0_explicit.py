from typing import *

from base_aux.base_inits.m1_source import *


# =====================================================================================================================
# TODO: use as ValueExplicit
# FIXME: deprecate???

@final
class Explicit(Init_Source):
    """
    GOAL
    ----
    1. solve NONE-VALUE as ambiguity by simple way
    2. show/pass explicitly the EXACT VALUE like None/[]/()

    RULES (when apply as funcResult)
    -----
    return object if you get final result!
    return None if there are any errors withing execution

    OLD ----

    WHY NOT-1: NamedTuple
    ----------------
    cause of we need to be able to compare different aux_types by values.
    maybe we need just add __eq__ method instead of it!!!

    USAGE
    -----
    to get exact value - just CALL instance! dont use .VALUE attr-access by attribute!

        from funcs import *

        def func(a, b) -> Optional[Explicit]:
            if a in b:
                return Explicit(a)
            else:
                return

        result = func("None", [None, ])
        assert result is None

        result = func(None, [None, ])
        assert result == Explicit(None)

        if result:
            print(result())         # None
    """
    SOURCE: Any   # dont use SOURCE access by attribute

    def __call__(self, *args, **kwargs) -> Any:
        return self.SOURCE

    def __str__(self):
        return f"{self.__class__.__name__}({self.SOURCE})"

    # -----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.SOURCE == other()
        else:
            return self.SOURCE == other


# =====================================================================================================================
