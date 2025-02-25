"""
GOAL
----
try keep all patterns for life!
"""
from typing import *
from base_aux.base_statics.m4_enums import *
from base_aux.aux_values.m0_novalue import *


# =====================================================================================================================
class Patterns:
    """
    STYLE
    -----
    PNAME: str = r""
    """


# =====================================================================================================================
class PatVersionBlock(Patterns):
    CLEAR = r"[\"' -]*"
    VALIDATE_NEGATIVE = r"\d+[^0-9a-z]+\d+"
    VALID = r"(\d|[a-z])+"
    ITERATE = r"\d+|[a-z]+"


class PatVersion(Patterns):
    """
    GOAL
    ----
    patterns for parse comments
    """
    # VERSION_TUPLE = r"\((\d+\.+(\w+\.?)+)\)"
    # VERSION_LIST = r"\[(\d+\.+(\w+\.?)+)\]"
    VERSION_IN_BRACKETS: list = [r"\((.*)\)", r"\[(.*)\]"]  # get first bracket!!!
    VALID_BRACKETS: list = [r"[^\[].*\]", r"\[.*[^\]]", r"[^\(].*\)", r"\(.*[^\)]"]


# =====================================================================================================================
class PatCmts(Patterns):
    """
    GOAL
    ----
    patterns for parse comments
    """
    SHARP_LINE: str = r"^\#.*$"
    SHARP_INLINE: str = r"\s+\#.*$"

    DSLASH_LINE: str = r"^\/\/.*$"
    DSLASH_INLINE: str = r"\s+\/\/.*$"

    REM_LINE: str = r"^REM +.*$"
    REM_INLINE: str = r"\s+REM +.*$"


# =====================================================================================================================
class PatNumberSingle(Patterns):
    """
    NOTE
    ----
    All patts ready to get result value by first group!

    *Exact - for exact/only number without any cover (suffix-prefix)!
    *COVERED - for any trash cover! used in re.fullmatch
    """
    INT_EXACT: str = r"(-?\d+)"
    INT_COVERED: str

    # @property ---
    FLOAT_EXACT: str
    FLOAT_COVERED: str

    BOTH_EXACT: str
    BOTH_COVERED: str

    # aux ---------
    _fpoint: FPoint = FPoint.AUTO
    _cover: tuple[str, str] = (r"\D*?", r"\D*")

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, fpoint: TYPE__FPOINT_DRAFT = NoValue) -> None | NoReturn:
        if fpoint is NoValue:
            pass
        elif fpoint in FPoint:
            self._fpoint = FPoint(fpoint)
        else:
            raise TypeError(f"{fpoint=}")

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    @property
    def INT_COVERED(cls) -> str:
        return cls._cover[0] + cls.INT_EXACT + cls._cover[1]

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def FLOAT_EXACT(self) -> str:
        if self._fpoint == FPoint.DOT:
            return r"(-?\d+\.\d+)"
        if self._fpoint == FPoint.COMMA:
            return r"(-?\d+\,\d+)"
        if self._fpoint == FPoint.AUTO:
            return r"(-?\d+[,.]\d+)"

    @property
    def FLOAT_COVERED(self) -> str:
        return self._cover[0] + self.FLOAT_EXACT + self._cover[1]

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def BOTH_EXACT(self) -> str:
        return r"(" + self.FLOAT_EXACT + r"|" + self.INT_EXACT + r")"   # float at FIRST PLACE only!

    @property
    def BOTH_COVERED(self) -> str:
        return self._cover[0] + self.BOTH_EXACT + self._cover[1]


# =====================================================================================================================
