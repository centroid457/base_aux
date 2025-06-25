from typing import *

from base_aux.base_values.m3_exceptions import *


# =====================================================================================================================
ARGS_FINAL__BLANK = ()
KWARGS_FINAL__BLANK = {}


# =====================================================================================================================
class Base_ValueSpecial:
    """
    GOAL
    ----
    BASE for result values like class (dont use instances!)
    using exact values wich can be directly compared and using as special universal values/states.
    values with Special meaning!

    NOTE
    ----
    never instantiate it! use value only as Class!

    SPECIALLY CREATED FOR
    ---------------------
    DictDiff instead of Enum values! - in there we have __Eq which cause incorrect usage/results!
    """
    def __init__(self) -> NoReturn:
        msg = f"Base_ValueSpecial NEVER INITTIATE! use direct CLASS!"
        raise Exx__WrongUsage(msg)

    # def __bool__(self):     # CANT USE!!! it works only on instance!!!
    #     return False

    # todo: add classmethod! - not working!!!
    # def __str__(self):
    #     return f"{self.__class__.__name__}"


# =====================================================================================================================
class NoValue(Base_ValueSpecial):
    """
    DOUPTS
    ------
    1. DEPRECATE???=====NO! used in valid/value
    2. use direct ArgsEmpty???/ArgsKwargs()??

    GOAL
    ----
    it is different from Default!
    there is no value!
    used when we need to change logic with not passed value!

    SPECIALLY CREATED FOR
    ---------------------
    Valid as universal validation object under cmp other base_types!

    USAGE
    -----
    class Cls:
        def __init__(self, value: Any | type[NoValue] | NoValue = NoValue):
            self.value = value

        def __eq__(self, other):
            if self.value is NoValue:
                return other is True
                # or
                return self.__class__(other).run()
            else:
                return other == self.value

        def run(self):
            return bool(self.value)
    """


# =====================================================================================================================
class Raised(Base_ValueSpecial):
    """
    GOAL
    ----
    just a mirror for GA_NotExists
    """
    # todo: add Meta EqCls with Exx??? to cmp with exact values??? - no! use special logic when do cmp!


# =====================================================================================================================
class _ValueSpecial:
    """
    GOAL
    ----
    just a collection for special values!

    USE instance!
    """
    NOVALUE: type[NoValue] = NoValue
    RAISED: type[Raised] = Raised

    def __iter__(self) -> Iterable[type]:
        """
        GOAL
        ----
        iter values
        """
        for name in self.__annotations__:
            yield getattr(self, name)

    def __contains__(self, item: Any) -> bool:
        """
        GOAL
        ----
        check value is special!
        """
        return item in self


# =====================================================================================================================
VALUE_SPECIAL = _ValueSpecial()


# =====================================================================================================================
