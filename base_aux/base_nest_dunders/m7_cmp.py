from typing import *
from abc import ABC, abstractmethod
from base_aux.base_values.m3_exceptions import *
from base_aux.base_types.m0_static_typing import TYPING


# =====================================================================================================================
class NestCmp_GLET_Any:
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
        # NOTE: CANT APPLY ACCURACY!!!
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
class NestCmp_GLET_DigitAccuracy:
    """
    GOAL
    ----
    apply for digital obj
    """
    CMP_ACCURACY: TYPING.DIGIT_FLOAT_INT = 0
    CMP_VALUE: TYPING.DIGIT_FLOAT_INT    # property

    @property
    def CMP_VALUE(self) -> TYPING.DIGIT_FLOAT_INT:
        raise NotImplementedError()

    def __init__(self, *args, cmp_accuracy: TYPING.DIGIT_FLOAT_INT_NONE = None, **kwargs) -> None:
        if cmp_accuracy:
            self.CMP_ACCURACY = cmp_accuracy or 0
        super().__init__(*args, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.CMP_VALUE})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.CMP_VALUE})"

    # -----------------------------------------------------------------------------------------------------------------
    def _cmp_accuracy__get_active(self, accuracy: TYPING.DIGIT_FLOAT_INT_NONE = None) -> TYPING.DIGIT_FLOAT_INT | NoReturn:
        if accuracy is not None:
            result = accuracy
        else:
            result = self.CMP_ACCURACY or 0

        if not isinstance(result, (int, float)):
            raise Exc__WrongUsage(f'{accuracy=}')

        return result

    # DEPENDANTS -------------------
    # NOTE: be careful when get Exc on second cmp with first False!
    cmp_gtlt = lambda self, other1, other2, accuracy=None: self.cmp_gt(other1, accuracy) and self.cmp_lt(other2, accuracy)
    cmp_gtle = lambda self, other1, other2, accuracy=None: self.cmp_gt(other1, accuracy) and self.cmp_le(other2, accuracy)

    cmp_gelt = lambda self, other1, other2, accuracy=None: self.cmp_ge(other1, accuracy) and self.cmp_lt(other2, accuracy)
    cmp_gele = lambda self, other1, other2, accuracy=None: self.cmp_ge(other1, accuracy) and self.cmp_le(other2, accuracy)

    cmp_eq = lambda self, other, accuracy=None: self.cmp_gele(other, other, accuracy)
    cmp_ne = lambda self, other, accuracy=None: not self.cmp_eq(other, accuracy)

    # accuracy DEF ------------------------
    __eq__ = lambda self, other: self.cmp_eq(other)
    # __ne__ = lambda self, other: self.__cmp__(other) != 0

    __lt__ = lambda self, other: self.cmp_lt(other)
    __gt__ = lambda self, other: self.cmp_gt(other)
    __le__ = lambda self, other: self.cmp_le(other)
    __ge__ = lambda self, other: self.cmp_ge(other)

    # BASE ------------------------------------------------------------------------------------------------------------
    def cmp_gt(self, other: TYPING.DIGIT_FLOAT_INT, accuracy: TYPING.DIGIT_FLOAT_INT_NONE = None) -> bool | NoReturn:   # NoReturn is only for bad accuracy and insorrect (nonDigital) other!!!!
        accuracy = self._cmp_accuracy__get_active(accuracy)

        result = (other - accuracy) < self.CMP_VALUE
        return result

    def cmp_ge(self, other: TYPING.DIGIT_FLOAT_INT, accuracy: TYPING.DIGIT_FLOAT_INT_NONE = None) -> bool | NoReturn:
        accuracy = self._cmp_accuracy__get_active(accuracy)

        result = (other - accuracy) <= self.CMP_VALUE
        return result

    def cmp_le(self, other: TYPING.DIGIT_FLOAT_INT, accuracy: TYPING.DIGIT_FLOAT_INT_NONE = None) -> bool | NoReturn:
        accuracy = self._cmp_accuracy__get_active(accuracy)

        result = self.CMP_VALUE <= (other + accuracy)
        return result

    def cmp_lt(self, other: TYPING.DIGIT_FLOAT_INT, accuracy: TYPING.DIGIT_FLOAT_INT_NONE = None) -> bool | NoReturn:
        accuracy = self._cmp_accuracy__get_active(accuracy)

        result = self.CMP_VALUE < (other + accuracy)
        return result


# =====================================================================================================================
