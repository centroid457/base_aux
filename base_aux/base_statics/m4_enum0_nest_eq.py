from enum import Enum


# =====================================================================================================================
class NestEq_Enum(Enum):
    """
    GOAL
    ----
    add user friendly cmp objects with final values

    VictimEq(1) == 1    # for std object it is False
    """
    def __eq__(self, other) -> bool:
        result = False
        if other in self.__class__:
            result = True
        try:
            if other in self:
                result = True
        except:
            pass

        if result:
            return other == self.value or self == self.__class__(other)
        else:
            return False


# =====================================================================================================================
