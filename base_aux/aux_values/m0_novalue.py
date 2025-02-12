from typing import *

from base_aux.base_statics.m2_exceptions import *


# =====================================================================================================================
class NoValue:
    """
    TODO: DEPRECATE???=NO! used in valid/value
    ---------
    use direct ArgsEmpty???/ArgsKwargs()

    NOTE
    ----
    never instantiate it! use value only as Class!

    GOAL
    ----
    it is different from Default!
    there is no value!
    used when we need to change logic with not passed value!

    SPECIALLY CREATED FOR
    ---------------------
    Valid as universal validation object under cmp other aux_types!

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
    def __init__(self) -> NoReturn:
        raise Exx__WrongUsage(NoValue)

    def __bool__(self):
        return False

    # todo: add classmethod! - not working!!!
    def __str__(self):
        return f"{self.__class__.__name__}"


# =====================================================================================================================
