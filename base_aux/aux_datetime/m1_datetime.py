from typing import *
import datetime

from base_aux.base_inits.m1_nest_init_source import *
from base_aux.aux_attr.m1_attr1_aux import *

# TODO: apply cmp eq!???
from base_aux.numbers.m1_arithm import *
from base_aux.aux_eq.m0_cmp_inst import *

# from enum import Enum, auto


# =====================================================================================================================
TYPE__TUPLE_DT_STYLE__DRAFT = tuple[str|None, str|None, str|None]
TYPE__TUPLE_DT_STYLE__FINAL = tuple[str, str, str]


class DateTimeStyle_Tuples:
    DT: TYPE__TUPLE_DT_STYLE__FINAL = ("-", " ", ":")       # default/standard from DateTime style for datetime.datetime.now()!
    DOTS: TYPE__TUPLE_DT_STYLE__FINAL = (".", " ", ".")     # same as DT but dots for data
    FILE: TYPE__TUPLE_DT_STYLE__FINAL = ("", "_", "")       # useful for filenames


# =====================================================================================================================
@final
class PatDateTimeFormat:
    def __init__(self, sdate: str = None, sdatetime: str = None, stime: str = None):
        """
        INIT separators only like schema
        """
        self.sdate = sdate or ""
        self.sdatetime = sdatetime or ""
        self.stime = stime or ""

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def D(self) -> str:                                 # 2025-02-14 20250214 2025.02.14
        return f"%Y{self.sdate}%m{self.sdate}%d"

    @property
    def Dw(self) -> str:                                 # 2025-02-14-Mn 20250214Mn 2025.02.14.Mn
        """
        GOAL
        ----
        ensure weekDay
        """
        return f"%Y{self.sdate}%m{self.sdate}%d" + f"{self.sdate}%a"

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def T(self) -> str:                                 # 11:38:48
        return f"%H{self.stime}%M{self.stime}%S"

    @property
    def Tm(self) -> str:                                 # 11:38:48.442179
        """
        GOAL
        ----
        ensure ms
        """
        return f"%H{self.stime}%M{self.stime}%S" + ".%f"

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def DT(self) -> str:
        return f"{self.D}{self.sdatetime}{self.T}"      # 2025-02-14 11:38:48.442179

    @property
    def DTm(self) -> str:
        """
        GOAL
        ----
        ensure ms
        """
        return f"{self.D}{self.sdatetime}{self.Tm}"      # 2025-02-14 11:38:48.442179

    @property
    def DwT(self) -> str:
        """
        GOAL
        ----
        ensure weekDay
        """
        return f"{self.Dw}{self.sdatetime}{self.T}"      # 2025-02-14-Пн 11:38:48

    @property
    def DwTm(self) -> str:
        """
        GOAL
        ----
        ensure weekDay+ms
        """
        return f"{self.Dw}{self.sdatetime}{self.Tm}"      # 2025-02-14-Пн 11:38:48.442179


# =====================================================================================================================
TYPE__DT_FINAL = datetime.datetime
TYPE__DT_DRAFT = datetime.datetime | str | int | float | None


# =====================================================================================================================
# @final    # select styles
class DateTimeAux:
    SOURCE: TYPE__DT_FINAL
    STYLE: TYPE__TUPLE_DT_STYLE__FINAL = DateTimeStyle_Tuples.DOTS
    _PATTS: PatDateTimeFormat

    # patterns getattr -----
    D: str
    Dw: str
    T: str
    Tm: str

    DT: str
    DwT: str
    DTm: str
    DwTm: str

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, source: TYPE__DT_DRAFT = None, style_tuple: TYPE__TUPLE_DT_STYLE__DRAFT = None) -> None:
        self.SOURCE = source
        if self.SOURCE is None:
            self.SOURCE = datetime.datetime.now()

        # FIXME: finish!!! int/float/td/str??? parser??? timestamp + time.time()
        if isinstance(self.SOURCE, datetime.datetime):
            pass
        else:
            pass

        if style_tuple is not None:
            self.STYLE = style_tuple

        self._PATTS = PatDateTimeFormat(*style_tuple)

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return self.DT

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

    def __getattr__(self, item) -> str | NoReturn:
        if item in AttrAux(PatDateTimeFormat).iter__not_hidden():
            return self.get_str__by_pat(pattern=getattr(self._PATTS, item))
        else:
            raise AttributeError(item)


# =====================================================================================================================
@final
class DateTimeAuxDT(DateTimeAux):
    STYLE: TYPE__TUPLE_DT_STYLE__FINAL = DateTimeStyle_Tuples.DT


@final
class DateTimeAuxDOTS(DateTimeAux):
    STYLE: TYPE__TUPLE_DT_STYLE__FINAL = DateTimeStyle_Tuples.DOTS


@final
class DateTimeAuxFILE(DateTimeAux):
    STYLE: TYPE__TUPLE_DT_STYLE__FINAL = DateTimeStyle_Tuples.FILE


# =====================================================================================================================
if __name__ == '__main__':
    print(DateTimeAux().T)
    print(DateTimeAux().D)
    print(DateTimeAux().DT)
    print(DateTimeAux().DwTm)
    print(repr(DateTimeAux()))
    print(str(DateTimeAux()))


# =====================================================================================================================
