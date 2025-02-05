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
    INT_EXACT: str = r"(\d+)"
    INT_COVERED: str

    # @property ---
    FLOAT_EXACT: str
    FLOAT_COVERED: str

    BOTH_EXACT: str
    BOTH_COVERED: str

    # aux ---------
    _fsep: FPoint = FPoint.DOT
    _cover: str = r"\D*"

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, fsep: FPoint = None) -> None | NoReturn:
        if fsep is None:
            pass
        elif fsep in FPoint:
            self._fsep = FPoint(fsep)
        else:
            raise TypeError(f"{fsep=}")

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    @property
    def INT_COVERED(cls) -> str:
        return cls._cover + cls.INT_EXACT + cls._cover

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def FLOAT_EXACT(self) -> str:
        if self._fsep == FPoint.DOT:
            return r"(\d+\.\d+)"
        if self._fsep == FPoint.COMMA:
            return r"(\d+\,\d+)"

    @property
    def FLOAT_COVERED(self) -> str:
        return self._cover + self.FLOAT_EXACT + self._cover

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def BOTH_EXACT(self) -> str:
        return r"(" + self.FLOAT_EXACT + r"|" + self.INT_EXACT + r")"

    @property
    def BOTH_COVERED(self) -> str:
        return self._cover + self.BOTH_EXACT + self._cover


# =====================================================================================================================
