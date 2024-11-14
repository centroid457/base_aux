from typing import *


# =====================================================================================================================
# TODO: use as ValueExplicit and VariantsExplicit(*args)
class Explicit:
    """
    GOAL
    ----
    1. solve NONE-VALUE as ambiguity by simple way
    2. show/pass explicitly the EXACT VALUE like None/[]/()

    RULES (when apply as funcResult)
    -----
    return object if you get final result!
    return None if there are any errors withing execution

    OLD ---- WHY: NamedTuple
    ----------------
    cause of we need to be able to compare different objects by values.
    maybe we need just add __eq__ method instead of it!!!

    USAGE
    -----
    to get exact value - just CALL instance! dont use VALUE access by attribute!

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
    __VALUE: Any   # dont use VALUE access by attribute

    def __init__(self, source: Any = None):
        self.__VALUE = source

    def __call__(self, *args, **kwargs) -> Any:
        return self.__VALUE

    def __str__(self):
        return f"{self.__class__.__name__}({self.__VALUE})"

    # -----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__VALUE == other()
        else:
            return self.__VALUE == other


# =====================================================================================================================
class Default(Explicit):
    """
    GOAL
    ----
    just a derivative for Explicit!
    use in funcs as explicitly define for not passed params!

    USAGE
    -----
    1. AUTO_WORK (preferred)
        when get Default instance - call it to get source value!
        if get Default class - get None as value!

        def func(source = Default(1)):
            if isinstance(source, Default):
                source = source()

    2. MANUAL_WORK (not preferred)
        you can apply inside func

        def func(source = Default):
            if source == Default:
                source = 1
    """
    pass


# =====================================================================================================================
TYPE__EXPLICIT = type[Explicit] | Explicit
TYPE__DEFAULT = type[Default] | Default


# =====================================================================================================================
