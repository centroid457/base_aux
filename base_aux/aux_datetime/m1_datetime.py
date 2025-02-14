from typing import *
import datetime

from base_aux.base_inits.m1_source import *

# TODO: apply cmp eq!???
from base_aux.numbers.m1_arithm import *
from base_aux.aux_eq.m0_cmp_inst import *

# from enum import Enum, auto


# =====================================================================================================================
TYPE__TUPLE_DT_STYLE__DRAFT = tuple[str|None, str|None, str|None, bool|None, bool|None]
TYPE__TUPLE_DT_STYLE__FINAL = tuple[str, str, str, bool, bool]


class DateTimeStyle_Tuples:
    DT: TYPE__TUPLE_DT_STYLE__FINAL = ("-", " ", ":", True, False)       # default standard DateTime style for datetime.datetime.now()!
    HUMAN: TYPE__TUPLE_DT_STYLE__FINAL = (".", " ", ":", True, False)  # same as DT but dots for data
    FILE: TYPE__TUPLE_DT_STYLE__FINAL = ("", "_", "", False, False)  # useful for filenames


@final
class PatDateTimeFormat:
    def __init__(self, sdate: str = None, sdatetime: str = None, stime: str = None, ms: bool = None, wd: bool = None):
        self.sdate = sdate or ""
        self.sdatetime = sdatetime or ""
        self.stime = stime or ""
        self.ms = ms or False
        self.wd = wd or False

    @property
    def D(self) -> str:                                 # 2025-02-14-Пн  20250214Пн 2025.02.14.Пн
        return f"%Y{self.sdate}%m{self.sdate}%d" + (f"{self.sdate}%a" if self.wd else "")

    @property
    def T(self) -> str:                                 # 11:38:48.442179
        return f"%H{self.stime}%M{self.stime}%S" + (".%f" if self.ms else "")

    @property
    def DT(self) -> str:
        return f"{self.D}{self.sdatetime}{self.T}"      # 2025-02-14-Пн 11:38:48.442179


# =====================================================================================================================
TYPE__DT_FINAL = datetime.datetime
TYPE__DT_DRAFT = datetime.datetime | str | int | float | None


@final
class DateTimeAux:
    SOURCE: TYPE__DT_FINAL
    STYLE: TYPE__TUPLE_DT_STYLE__FINAL
    PATTS: PatDateTimeFormat

    def __init__(self, source: TYPE__DT_DRAFT = None, style_tuple: TYPE__TUPLE_DT_STYLE__DRAFT = DateTimeStyle_Tuples.HUMAN) -> None:
        self.SOURCE = source
        if self.SOURCE is None:
            self.SOURCE = datetime.datetime.now()

        # FIXME: finish!!! int/float/td/str??? parser???
        if isinstance(self.SOURCE, datetime.datetime):
            pass
        else:
            pass
        self.STYLE = style_tuple
        self.PATTS = PatDateTimeFormat(*style_tuple)

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return self.DATETIME

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"

    def __int__(self):
        raise NotImplementedError()

    def __float__(self):
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    def get_str__by_pat(self, pattern: str) -> str:
        """
        GOAL
        ----
        use for filenames like dumps/reservations/logs

        SPECIALLY CREATED FOR
        ---------------------

        EXAMPLES
        --------
        %Y%m%d_%H%M%S -> 20241203_114845
        add_ms -> 20241203_114934.805854
        """
        return self.SOURCE.strftime(pattern)

    @property
    def DATE(self) -> str:
        return self.get_str__by_pat(pattern=self.PATTS.D)

    @property
    def TIME(self) -> str:
        return self.get_str__by_pat(pattern=self.PATTS.T)

    @property
    def DATETIME(self) -> str:
        return self.get_str__by_pat(pattern=self.PATTS.DT)


# =====================================================================================================================
if __name__ == '__main__':
    print(DateTimeAux().TIME)
    print(DateTimeAux().DATE)
    print(DateTimeAux().DATETIME)
    print(repr(DateTimeAux()))
    print(str(DateTimeAux()))


# =====================================================================================================================
