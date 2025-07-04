from typing import *


# =====================================================================================================================
class NestCmp_LGET:
    """
    GOAL
    ----
    APPLYING COMPARISON WITH SELF INSTANCE

    BEST USAGE
    ----------
    just redefine one method __cmp__!

    WHY NOT: JUST USING ONE BY ONE EXACT METHODS?
    ---------------------------------------------
    it is more complicated then just one explicit __cmp__()!
    __cmp__ is not directly acceptable in Python! this is not a buildIn method!

    """
    __eq__ = lambda self, other: self.__cmp__(other) == 0
    # __ne__ = lambda self, other: self.__cmp__(other) != 0

    __lt__ = lambda self, other: self.__cmp__(other) < 0
    __gt__ = lambda self, other: self.__cmp__(other) > 0
    __le__ = lambda self, other: self.__cmp__(other) <= 0
    __ge__ = lambda self, other: self.__cmp__(other) >= 0

    # USING - for just raiseIf prefix!
    # FIXME: seems need to DEPRECATE? use direct EqValid_LGTE???

    # ------------------------
    check_ltgt = lambda self, other1, other2: self > other1 and self < other2
    check_ltge = lambda self, other1, other2: self > other1 and self <= other2

    check_legt = lambda self, other1, other2: self >= other1 and self < other2
    check_lege = lambda self, other1, other2: self >= other1 and self <= other2

    # ------------------------
    check_eq = lambda self, other: self == other
    check_ne = lambda self, other: self != other

    check_lt = lambda self, other: self < other
    check_le = lambda self, other: self <= other

    check_gt = lambda self, other: self > other
    check_ge = lambda self, other: self >= other

    # CMP -------------------------------------------------------------------------------------------------------------
    def __cmp__(self, other: Any) -> int | NoReturn:
        """
        do try to resolve Exceptions!!! sometimes it is ok to get it!!!

        RETURN
        ------
            1=self>other
            0=self==other
            -1=self<other
        """
        raise NotImplemented()

    # -----------------------------------------------------------------------------------------------------------------
    # def __eq__(self, other):
    #     return self.__cmp__(other) == 0
    #
    # def __ne__(self, other):
    #     return self.__cmp__(other) != 0
    #
    # def __lt__(self, other):
    #     return self.__cmp__(other) < 0
    #
    # def __gt__(self, other):
    #     return self.__cmp__(other) > 0
    #
    # def __le__(self, other):
    #     return self.__cmp__(other) <= 0
    #
    # def __ge__(self, other):
    #     return self.__cmp__(other) >= 0


# =====================================================================================================================
