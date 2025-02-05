"""
GOAL
----
try keep all patterns for life!
"""
from typing import *
from base_aux.base_enums.m0_enums import *


# =====================================================================================================================
class Patterns:
    """
    STYLE
    -----
    PNAME: str = r""
    """


# =====================================================================================================================
class PatNumberSingle(Patterns):
    """
    NOTE
    ----
    All patts ready to get value as group!
    """
    INT_EXACT: str = r"(-?\d+)"
    INT_COVERED: str

    # @property ---
    FLOAT_EXACT: str
    FLOAT_COVERED: str

    BOTH_EXACT: str
    BOTH_COVERED: str

    # aux ---------
    _fpoint: FPoint = FPoint.DOT
    _cover: tuple[str, str] = (r"\D*(?!-)", r"\D*")

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, fpoint: TYPE__FPOINT_DRAFT = None) -> None | NoReturn:
        if fpoint is None:
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
