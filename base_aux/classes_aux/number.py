from typing import *
from object_info import *
import math
from classes_aux import CmpInst


# =====================================================================================================================
TYPE__NUMBER = int | float


class Exx__NumberArithm_NoName(Exception):
    pass


# =====================================================================================================================
class NumberArithmTranslateToAttr(CmpInst):
    """
    GOAL
    ----
    translate all arithmetic operations to exact attribute (expected as number)!

    NOTE
    ----
    1. BE CAREFUL to compare FLOATS!!! it used Precision settings!

    2. MAINLY fom the beginning:
    always return Self for any operation (except direct int/float transform methods).
    So if you need exact NUMBER - just apply float() (int is incorrect!).

    MAYBE IN FUTURE:
    IF FUNC - return number, if operation - return Self.
    I'm not really know what is the best decision but in future it may be changed for real implementation

    CREATED SPECIALLY FOR
    ---------------------
    funcs_aux.ValueUnit and further ising in Uart Responses

    BEST USAGE
    ----------
    see tests!

    REFERENCE
    ---------
    https://docs.python.org/3/library/operator.html
    """

    # SETTINGS --------------------------------------------------------------------------------------------------------
    NUMBER_ARITHM__GETATTR_NAME: str = None     # DEFINE!!! name for ORIGINALVALUE
    NUMBER_ARITHM__PRECISION: int | None = 6

    # AUX -------------------------------------------------------------------------------------------------------------
    @property
    def NUMBER_ARITHM(self) -> Union[TYPE__NUMBER, NoReturn]:
        if not self.NUMBER_ARITHM__GETATTR_NAME:
            raise Exx__NumberArithm_NoName()

        result = getattr(self, self.NUMBER_ARITHM__GETATTR_NAME)
        if TypeChecker.check__callable_func_meth_inst(result):
            result = result()
        return result

    @NUMBER_ARITHM.setter
    def NUMBER_ARITHM(self, other) -> None | NoReturn:
        if not self.NUMBER_ARITHM__GETATTR_NAME:
            raise Exx__NumberArithm_NoName()

        if self.NUMBER_ARITHM__PRECISION is not None:
            other = round(other, self.NUMBER_ARITHM__PRECISION)

        setattr(self, self.NUMBER_ARITHM__GETATTR_NAME, other)

    # precision --------------------------------------
    @classmethod
    def number__fix_precision(cls, source: Any, round_n: int | None = None) -> TYPE__NUMBER:
        source = float(source)
        if round_n is None:
            round_n = cls.NUMBER_ARITHM__PRECISION
        if round_n is not None:
            source = round(source, round_n)

        # final -------
        source = cls.number__try_int_if_same(source)
        return source

    @classmethod
    def number__try_int_if_same(cls, source: Any) -> int | Any:
        """
        GOAL
        ----
        get int value if int()==float()

        USEFUL IDEAS
        ------------
        1. keep short value in str() when we have float value with insignificant zeros (like 1.0)
        2. correct comparing int with float
            assert 1 != 1.0
            assert int(1) == int(1.0)
        3. fix correct comparing strings
            assert int("1.0") == 1  # will get EXX!!!
            assert number__try_int_if_same("1.0") == 1  # will get True

        Created specially for
        ---------------------
        NumberArithm class
        """
        try:
            if int(float(source)) == float(source):
                source = int(float(source))
        except:
            pass
        return source

    @classmethod
    def number__get_string_no_zeros(cls, source: Any, round_n: int | None = None) -> str:
        source = cls.number__fix_precision(source, round_n)
        if isinstance(source, int):
            result = f"{source}"
        else:
            result= f"{source:f}".rstrip("0").rstrip(".")

        # final -------
        return result

    # CONVERT ---------------------------------------------------------------------------------------------------------
    # MAIN --------------------------------------
    def __int__(self) -> int | NoReturn:
        """
        CAUTION
        -------
        BE CAREFUL ABOUT ANY INT!!!
            int(1.999) == 1!!!!
        :return:
        """
        return int(self.NUMBER_ARITHM)

    def __float__(self) -> float:
        return float(self.NUMBER_ARITHM)

    def __hash__(self) -> int:
        return hash(self.NUMBER_ARITHM)

    # OTHER --------------------------------------
    def __bool__(self) -> bool:
        return bool(self.NUMBER_ARITHM)

    def __str__(self) -> str:
        return self.number__get_string_no_zeros(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.NUMBER_ARITHM})"

    # SIGN ------------------------------------------------------------------------------------------------------------
    def __pos__(self) -> Self:
        """
        для унарного плюса (+some_object)
        """
        return self

    def __neg__(self) -> Self:
        """
        для унарного минуса (-some_object)
        """
        self.NUMBER_ARITHM = - self.NUMBER_ARITHM
        return self

    def __abs__(self) -> Self:
        self.NUMBER_ARITHM = abs(self.NUMBER_ARITHM)
        return self

    # PARTS -----------------------------------------------------------------------------------------------------------
    def __round__(self, n=None) -> Self:
        self.NUMBER_ARITHM = round(self.NUMBER_ARITHM, n)
        return self

    def __floor__(self) -> Self:
        self.NUMBER_ARITHM = math.floor(self.NUMBER_ARITHM)
        return self

    def __ceil__(self) -> Self:
        self.NUMBER_ARITHM = math.ceil(self.NUMBER_ARITHM)
        return self

    def __trunc__(self) -> Self:
        self.NUMBER_ARITHM = math.trunc(self.NUMBER_ARITHM)
        return self

    # OTHER ===========================================================================================================
    def _other__get_float(self, other: Any) -> float | NoReturn:
        try:
            other = self.__class__(other)
        except:
            pass
        return float(other)

    # ARITHM ----------------------------------------------------------------------------------------------------------
    def __add__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM + self._other__get_float(other)
        return self

    def __sub__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM - self._other__get_float(other)
        return self

    def __mul__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM * self._other__get_float(other)
        return self

    # def __div__(self, other) -> Self:   # THERE IS NO SUCH MAGICMETH!!! use truediv!
    #     return self.NUMBER_ARITHM/other
    #     return self

    def __truediv__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM / self._other__get_float(other)
        return self

    def __floordiv__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM // self._other__get_float(other)
        return self

    def __mod__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM % self._other__get_float(other)
        return self

    def __divmod__(self, other) -> tuple[int, int | float]:
        return divmod(self.NUMBER_ARITHM, float(other))

    def __pow__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM ** self._other__get_float(other)
        return self

    # INLINE ----------------------------------------------------------------------------------------------------------
    def __iadd__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM + self._other__get_float(other)
        return self

    def __isub__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM - self._other__get_float(other)
        return self

    def __imul__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM * self._other__get_float(other)
        return self

    def __itruediv__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM / self._other__get_float(other)
        return self

    def __ifloordiv__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM // self._other__get_float(other)
        return self

    def __imod__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM % self._other__get_float(other)
        return self

    def __ipow__(self, other) -> Self:
        self.NUMBER_ARITHM = self.NUMBER_ARITHM ** self._other__get_float(other)
        return self

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
        if float(self.NUMBER_ARITHM) == self._other__get_float(other) or other == float(self.NUMBER_ARITHM):
            return 0
        if float(self.NUMBER_ARITHM) > self._other__get_float(other) or other < float(self.NUMBER_ARITHM):
            return 1
        if float(self.NUMBER_ARITHM) < self._other__get_float(other) or other > float(self.NUMBER_ARITHM):
            return -1


# =====================================================================================================================
