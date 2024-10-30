from typing import *


# =====================================================================================================================
class CmpInst:
    """
    GOAL
    ----
    TEMPLATE FOR APPLYING COMPARISON WITH SELF INSTANCE

    CREATED SPECIALLY FOR
    ---------------------

    BEST USAGE
    ----------
    just redefine one method __cmp__!

    WHY NOT: JUST USING ONE BY ONE EXACT METHODS?
    ---------------------------------------------
    it is more complicated then just one explicit __cmp__()!
    __cmp__ is not directly acceptable in Python! this is not a buildIn method!

    """
    __eq__ = lambda self, other: self.__cmp__(other) == 0
    __ne__ = lambda self, other: self.__cmp__(other) != 0

    __lt__ = lambda self, other: self.__cmp__(other) < 0
    __gt__ = lambda self, other: self.__cmp__(other) > 0
    __le__ = lambda self, other: self.__cmp__(other) <= 0
    __ge__ = lambda self, other: self.__cmp__(other) >= 0

    ltgt = lambda self, other1, other2: self > other1 and self < other2
    ltge = lambda self, other1, other2: self > other1 and self <= other2

    legt = lambda self, other1, other2: self >= other1 and self < other2
    lege = lambda self, other1, other2: self >= other1 and self <= other2

    # CMP -------------------------------------------------------------------------------------------------------------
    def __cmp__(self, other) -> int | NoReturn:
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
