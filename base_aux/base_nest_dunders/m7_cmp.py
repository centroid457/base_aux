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
    # CMP_ACCURACY_VALUE_MIN: TYPING.DIGIT_FLOAT_INT_NONE = None  # TODO: add! in case of Percent!

    CMP_ACCURACY_VALUE: TYPING.DIGIT_FLOAT_INT_NONE = None
    CMP_ACCURACY_PERCENT: TYPING.DIGIT_FLOAT_INT_NONE = None

    CMP_VALUE: TYPING.DIGIT_FLOAT_INT    # property

    @property
    def CMP_VALUE(self) -> TYPING.DIGIT_FLOAT_INT:
        raise NotImplementedError()

    def __init__(
            self,
            *args,
            cmp_accuracy_value: TYPING.DIGIT_FLOAT_INT_NONE = None,
            cmp_accuracy_percent: TYPING.DIGIT_FLOAT_INT_NONE = None,
            **kwargs,
    ) -> None | NoReturn:
        if cmp_accuracy_value is not None:
            self.CMP_ACCURACY_VALUE = cmp_accuracy_value
        if cmp_accuracy_percent is not None:
            self.CMP_ACCURACY_PERCENT = cmp_accuracy_percent

        self._cmp_accuracy__check_correctness(cmp_accuracy_value, cmp_accuracy_percent)
        super().__init__(*args, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.CMP_VALUE}/accuracy_default={self._cmp_accuracy__get_active()})"

    def __repr__(self) -> str:
        return str(self)

    # -----------------------------------------------------------------------------------------------------------------
    def _cmp_accuracy__check_correctness(
            self,
            accuracy_value: TYPING.DIGIT_FLOAT_INT_NONE = None,
            accuracy_percent: TYPING.DIGIT_FLOAT_INT_NONE = None,
            raised: bool = True,
    ) -> bool | NoReturn:
        raised_msg = None
        # step1 --------
        if accuracy_value is not None and accuracy_percent is not None:
            raised_msg = f"dont use both {accuracy_value=}/{accuracy_percent=}"

        elif self.CMP_ACCURACY_VALUE is not None and self.CMP_ACCURACY_PERCENT is not None:
            raised_msg = f"dont use both {self.CMP_ACCURACY_VALUE=}/{self.CMP_ACCURACY_PERCENT=}"

        # step2 --------
        for accuracy in [accuracy_value, accuracy_percent, self.CMP_ACCURACY_VALUE, self.CMP_ACCURACY_PERCENT]:
            if accuracy is not None and not isinstance(accuracy, (int, float)):
                raised_msg = f"inappropriate type {accuracy=}"
                break

        # final --------
        if raised_msg:
            print(raised_msg)
            if raised:
                raise Exc__WrongUsage(raised_msg)

        return raised_msg is None

    def _cmp_accuracy__translate_from_percent(self, accuracy_percent: float | None = None) -> float:
        """
        NOTE
        ----
        CAREFUL for actual values!!!
        when FLOAT+FLOAT - applied additional tailing value!!!
        dont mind it and dont use its result too strong!!!
        """
        if accuracy_percent is None:
            accuracy_percent = self.CMP_ACCURACY_PERCENT or 0

        result = self.CMP_VALUE * accuracy_percent / 100
        return result

    def _cmp_accuracy__get_active(
            self,
            accuracy_value: TYPING.DIGIT_FLOAT_INT_NONE = None,
            accuracy_percent: TYPING.DIGIT_FLOAT_INT_NONE = None
    ) -> TYPING.DIGIT_FLOAT_INT | NoReturn:     # add tests for meth
        """
        GOAL
        ----
        return final accuracy_value VALUE! from
        """
        self._cmp_accuracy__check_correctness(accuracy_value, accuracy_percent)

        result = 0
        # if accuracy_value is not None and accuracy_percent is not None:
        #     raise Exc__WrongUsage(f"dont use both {accuracy_value=}/{accuracy_percent=}")

        if accuracy_value is None and accuracy_percent is None:
            if self.CMP_ACCURACY_VALUE is not None:
                result = self.CMP_ACCURACY_VALUE
            elif self.CMP_ACCURACY_PERCENT is not None:
                result = self._cmp_accuracy__translate_from_percent(self.CMP_ACCURACY_PERCENT)
            else:
                result = 0

        elif accuracy_value is not None:
            result = accuracy_value

        elif accuracy_percent is not None:
            result = self._cmp_accuracy__translate_from_percent(accuracy_percent)

        # final check -------------------------------------
        if not isinstance(result, (int, float)):
            raise Exc__WrongUsage(f'{accuracy_value=}')

        return result

    # DEPENDANTS -------------------
    # NOTE: be careful when get Exc on second cmp with first False!
    cmp_gtlt = lambda self, other1, other2, accuracy_value=None, accuracy_percent=None: self.cmp_gt(other1, accuracy_value, accuracy_percent) and self.cmp_lt(other2, accuracy_value, accuracy_percent)
    cmp_gtle = lambda self, other1, other2, accuracy_value=None, accuracy_percent=None: self.cmp_gt(other1, accuracy_value, accuracy_percent) and self.cmp_le(other2, accuracy_value, accuracy_percent)

    cmp_gelt = lambda self, other1, other2, accuracy_value=None, accuracy_percent=None: self.cmp_ge(other1, accuracy_value, accuracy_percent) and self.cmp_lt(other2, accuracy_value, accuracy_percent)
    cmp_gele = lambda self, other1, other2, accuracy_value=None, accuracy_percent=None: self.cmp_ge(other1, accuracy_value, accuracy_percent) and self.cmp_le(other2, accuracy_value, accuracy_percent)

    cmp_eq = lambda self, other, accuracy_value=None, accuracy_percent=None: self.cmp_gele(other, other, accuracy_value, accuracy_percent)
    cmp_ne = lambda self, other, accuracy_value=None, accuracy_percent=None: not self.cmp_eq(other, accuracy_value, accuracy_percent)

    # accuracy_value DEF ------------------------
    __eq__ = lambda self, other: self.cmp_eq(other)
    # __ne__ = lambda self, other: self.__cmp__(other) != 0

    __lt__ = lambda self, other: self.cmp_lt(other)
    __gt__ = lambda self, other: self.cmp_gt(other)
    __le__ = lambda self, other: self.cmp_le(other)
    __ge__ = lambda self, other: self.cmp_ge(other)

    # BASE ------------------------------------------------------------------------------------------------------------
    def cmp_gt(
            self,
            other: TYPING.DIGIT_FLOAT_INT,
            accuracy_value: TYPING.DIGIT_FLOAT_INT_NONE = None,
            accuracy_percent: TYPING.DIGIT_FLOAT_INT_NONE = None
    ) -> bool | NoReturn:   # NoReturn is only for bad accuracy_value and insorrect (nonDigital) other!!!!
        accuracy_value = self._cmp_accuracy__get_active(accuracy_value=accuracy_value, accuracy_percent=accuracy_percent)

        result = (other - accuracy_value) < self.CMP_VALUE
        return result

    def cmp_ge(
            self,
            other: TYPING.DIGIT_FLOAT_INT,
            accuracy_value: TYPING.DIGIT_FLOAT_INT_NONE = None,
            accuracy_percent: TYPING.DIGIT_FLOAT_INT_NONE = None
    ) -> bool | NoReturn:
        accuracy_value = self._cmp_accuracy__get_active(accuracy_value=accuracy_value, accuracy_percent=accuracy_percent)

        result = (other - accuracy_value) <= self.CMP_VALUE
        return result

    def cmp_le(
            self,
            other: TYPING.DIGIT_FLOAT_INT,
            accuracy_value: TYPING.DIGIT_FLOAT_INT_NONE = None,
            accuracy_percent: TYPING.DIGIT_FLOAT_INT_NONE = None
    ) -> bool | NoReturn:
        accuracy_value = self._cmp_accuracy__get_active(accuracy_value=accuracy_value, accuracy_percent=accuracy_percent)

        result = self.CMP_VALUE <= (other + accuracy_value)
        return result

    def cmp_lt(
            self,
            other: TYPING.DIGIT_FLOAT_INT,
            accuracy_value: TYPING.DIGIT_FLOAT_INT_NONE = None,
            accuracy_percent: TYPING.DIGIT_FLOAT_INT_NONE = None
    ) -> bool | NoReturn:
        accuracy_value = self._cmp_accuracy__get_active(accuracy_value=accuracy_value, accuracy_percent=accuracy_percent)

        result = self.CMP_VALUE < (other + accuracy_value)
        return result


# =====================================================================================================================
