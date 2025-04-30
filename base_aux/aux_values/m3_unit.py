from typing import *
import re

from base_aux.base_statics.m2_exceptions import *
from base_aux.aux_values.m0_novalue import NoValue

from base_aux.aux_attr.m2_annot3_cls_keys_as_values import NestGaCls_AnnotNamesAsValuesIc
from base_aux.numbers.m1_arithm import ArithmApplyToAttr

from base_aux.aux_cmp_eq.m2_eq_aux import *


# =====================================================================================================================
class UnitBase(NestGaCls_AnnotNamesAsValuesIc):
    # class UnitBase:
    """
    this is just an example! it will help you to use just strings by Object
    """
    V: str
    A: str
    C: str


UNIT_MULT__VARIANTS: dict[str, float | int] = {
    # ENG/INTERNATIONAL
    "p": 10 ** (-12),
    "n": 10 ** (-9),
    "µ": 10 ** (-6),
    "m": 10 ** (-3),
    "c": 10 ** (-2),
    "d": 10 ** (-1),

    "k": 10 ** 3,
    "M": 10 ** 6,
    "G": 10 ** 9,
    "T": 10 ** 12,

    # RUS
    "п": 10 ** (-12),
    "н": 10 ** (-9),
    "мк": 10 ** (-6),
    "м": 10 ** (-3),
    "с": 10 ** (-2),
    "д": 10 ** (-1),

    "к": 10 ** 3,
    "М": 10 ** 6,
    "Г": 10 ** 9,
    "Т": 10 ** 12,

    # ONE
    "": 10 ** 0,  # keep it last only or just delete!!!
}


# =====================================================================================================================
pass


# TODO: rename to ValueUnit_Arithm
class ValueUnit(ArithmApplyToAttr):
    """
    GOAL
    ----
    keep separated/parse VALUE and measure UNIT and compare with any representation

    CREATED SPECIALLY FOR
    ---------------------
    use in UART/SERIAL to get exact inline comparable numeric value!

    NOTE
    ----
    DONT MESS VALUE&VALUE_PURE!!!
        VALUE - is an original number with multiplier not applied
        VALUE_PURE - multiplier applied

    Example:
        SOURCE = 1k
        VALUE = 1
        VALUE_PURE = 1000

    so VALUE - is the most useful representation in your application!!!

    BEST USAGE
    ----------
        assert ValueUnit('0.0k') == 0
        assert ValueUnit('0,01k') == 10

        assert ValueUnit('1нм') == '1n'    #RUS multipliers are acceptable! and mean the same!

        assert ValueUnit('1k') == '1000'
        assert ValueUnit('1kV') == 1000
        assert ValueUnit('1kV') == '1k'
        assert ValueUnit(1000) == '1kV'

        assert ValueUnit(1001) > '1kV'
        assert ValueUnit(1000) < '1.1kV'

        - NoValue - same as object as pattern!

        assert "1" == ValueUnit(NoValue)
        assert "1V" == ValueUnit(NoValue)
        assert "1V" == ValueUnit(NoValue, unit="V")
        assert "1" == ValueUnit(NoValue, unit="V")
        assert "1A" != ValueUnit(NoValue, unit="V")

    """
    # NESTED ----------------------
    NUMBER_ARITHM__ATTR = "VALUE_PURE"

    # SETTINGS -------------------------
    SEPARATOR: str = ""     # when parsed - used pared separator, when

    UNIT_MULT__DISABLE: bool | None = None
    UNIT_MULT__VARIANTS: dict[str, float | int] = UNIT_MULT__VARIANTS

    # NEW -------------------------
    UNIT: str = ""      # final unit with multiplier
    UNIT_MULT: str = ""
    UNIT_BASE: str = ""
    MULT: int = 1

    SOURCE: Any = None
    VALUE: Union[int, float] = 0    # DONT MESS VALUE/VALUE_PURE!!! see NOTES! if UNIT_MULT__DISABLE all are the same!!!

    @property
    def VALUE_PURE(self) -> Union[int, float]:
        return self.number__fix_precision(self.VALUE * self.MULT)

    @VALUE_PURE.setter
    def VALUE_PURE(self, value_pure: Any) -> None:
        value_pure = self._other__get_float(value_pure)
        if int(value_pure) == float(value_pure):
            value_pure = int(value_pure)

        value = value_pure / self.MULT
        value = self.number__fix_precision(value)
        self.VALUE = value

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, source: Union[int, float, str, Any] = NoValue, unit: str = None, separator: str = None, mult_disable: bool = None):
        """
        :param source:
        :param unit: use it only if not exists in source!
        :param separator: if set - would overwrite parsed!
        """
        if mult_disable is not None:
            self.UNIT_MULT__DISABLE = mult_disable

        if self.UNIT_MULT__DISABLE:
            self.UNIT_MULT__VARIANTS = {}

        self.SOURCE = source

        # first parse -----------------
        if source is NoValue:
            pass
        else:
            self.parse(source)

        # second OVERWRITE  -----------------
        if unit is not None:
            self.UNIT = unit
            self.UNIT_BASE = unit
            self.UNIT_MULT = ""
            self.MULT = 1
        if separator is not None:
            self.SEPARATOR = separator

    @classmethod
    def validate(cls, source: Any) -> bool:
        """
        CREATED SPECIALLY FOR
        ---------------------
        if ypu want to decide somewhere return ValueUnit-object or just source
        check source before applying
        """
        try:
            cls(source)
            return True
        except:
            return False

    def clear(self) -> None:
        self.SOURCE = None
        self.VALUE = 0
        self.UNIT = ""
        self.UNIT_MULT = ""
        self.UNIT_BASE = ""
        self.MULT = 1

    def parse(self, source: Any) -> Self | NoReturn:
        self.clear()
        self.SOURCE = source

        if isinstance(source, (int, float)):
            self.VALUE = source
        else:
            source = str(source)
            source = source.strip()
            source = source.replace(',', ".")
            source = re.sub(r'-\s*', '-', source)
            source = re.sub(r'\+\s*', '', source)
            source = re.sub(r'\'\'', '', source)
            source = re.sub(r'\"\"', '', source)

            # WORK ---------------------------
            match = re.fullmatch(r'(-?[0-9.]+)(\s*)([a-zA-Zа-яА-Я]*)', source)
            if match:
                self.VALUE = float(match[1])
                self.SEPARATOR = match[2] or ""
                self.UNIT = match[3] or ""
            else:
                raise Exx__NotExistsNotFoundNotCreated()

            # UNIT_MULT ------------------
            if not self.UNIT_MULT__DISABLE:
                for unit_mult, multiplier in self.UNIT_MULT__VARIANTS.items():
                    if self.UNIT.startswith(unit_mult):
                        self.UNIT_MULT = unit_mult
                        self.UNIT_BASE = self.UNIT.removeprefix(unit_mult)
                        self.MULT = multiplier
                        break

        # PRECISION -----------------------
        self.VALUE = self.number__fix_precision(self.VALUE)

        # INT -----------------------------
        if int(self.VALUE) == self.VALUE:
            self.VALUE = int(self.VALUE)
        else:
            self.VALUE = self.VALUE

        # if not self.UNIT_BASE and self.UNIT:
        #     self.UNIT_BASE = self.UNIT

        # FINISH ---------------------------
        return self

    def __str__(self) -> str:
        return f"{self.VALUE}{self.SEPARATOR}{self.UNIT}"

    def __repr__(self) -> str:
        """
        used as help
        """
        return str(self)

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
        if EqAux(self.VALUE).check_doubleside__bool(other):
            return 0
        if not isinstance(other, self.__class__):
            other = self.__class__(other)

        if self.SOURCE == NoValue or other.SOURCE == NoValue:
            if self.UNIT_BASE == other.UNIT_BASE or self.UNIT == other.UNIT:
                return 0
            elif not self.UNIT and not other.UNIT:
                return 0
            else:
                return -1   # just to show not equel!!!

        # cmp units -----------
        if self.UNIT_BASE and other.UNIT_BASE and self.UNIT_BASE != other.UNIT_BASE:
            msg = f"{self!r}/{other!r}"
            raise Exx__Incompatible(msg)

        # cmp -----------
        if self.VALUE_PURE == other.VALUE_PURE:
            return 0
        elif self.VALUE_PURE > other.VALUE_PURE:
            return 1
        elif self.VALUE_PURE < other.VALUE_PURE:
            return -1


# =====================================================================================================================
class ValueUnit_NoMulty(ValueUnit):
    """
    this is just as parser! when you need only get number near the unit without object arithmetic acceptable.
    but with comparing methods.

    NOTE
    ----
    maybe it is cant be used
    """
    UNIT_MULT__DISABLE = True


# =====================================================================================================================
