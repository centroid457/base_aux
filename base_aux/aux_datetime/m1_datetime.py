import datetime

from base_aux.aux_attr.m1_attr1_aux import *
from base_aux.aux_cmp_eq.m1_cmp import *
from base_aux.aux_text.m1_text_aux import *


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
    def __init__(self, sep_date: str = None, sep_datetime: str = None, sep_time: str = None):
        """
        INIT separators only like schema
        """
        self.sep_date = sep_date or ""
        self.sep_datetime = sep_datetime or ""
        self.sep_time = sep_time or ""

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def D(self) -> str:                                 # 2025-02-14 20250214 2025.02.14
        return f"%Y{self.sep_date}%m{self.sep_date}%d"

    @property
    def Dw(self) -> str:                                 # 2025-02-14-Mn 20250214Mn 2025.02.14.Mn
        """
        GOAL
        ----
        ensure weekDay
        """
        return f"%Y{self.sep_date}%m{self.sep_date}%d" + f"{self.sep_date}%a"

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def T(self) -> str:                                 # 11:38:48
        return f"%H{self.sep_time}%M{self.sep_time}%S"

    @property
    def Tm(self) -> str:                                 # 11:38:48.442179
        """
        GOAL
        ----
        ensure ms
        """
        return f"%H{self.sep_time}%M{self.sep_time}%S" + ".%f"

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def DT(self) -> str:
        return f"{self.D}{self.sep_datetime}{self.T}"      # 2025-02-14 11:38:48.442179

    @property
    def DTm(self) -> str:
        """
        GOAL
        ----
        ensure ms
        """
        return f"{self.D}{self.sep_datetime}{self.Tm}"      # 2025-02-14 11:38:48.442179

    @property
    def DwT(self) -> str:
        """
        GOAL
        ----
        ensure weekDay
        """
        return f"{self.Dw}{self.sep_datetime}{self.T}"      # 2025-02-14-Пн 11:38:48

    @property
    def DwTm(self) -> str:
        """
        GOAL
        ----
        ensure weekDay+ms
        """
        return f"{self.Dw}{self.sep_datetime}{self.Tm}"      # 2025-02-14-Пн 11:38:48.442179


# =====================================================================================================================
TYPE__DT_FINAL = datetime.datetime | datetime.date | datetime.time  # NOTE: dont use    | datetime.timedelta
TYPE__DT_DRAFT = TYPE__DT_FINAL | str | int | float | None


# =====================================================================================================================
# @final    # select styles
class DateTimeAux(NestCmp):
    SOURCE: TYPE__DT_FINAL = None
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
    def __init__(self, source: TYPE__DT_DRAFT = None, style_tuple: TYPE__TUPLE_DT_STYLE__DRAFT = None) -> None | NoReturn:
        self.init_source(source)

        if style_tuple is not None:
            self.STYLE = style_tuple

        self._PATTS = PatDateTimeFormat(*self.STYLE)

    def init_source(self, source: TYPE__DT_DRAFT = None) -> None | NoReturn:
        if source is None:
            self.SOURCE = datetime.datetime.now()
        else:
            self.SOURCE = source

        # ---------------------------------------
        # FIXME: finish!!! int/float/td/str??? parser??? timestamp + time.time()
        if isinstance(self.SOURCE, datetime.datetime):
            pass
        elif isinstance(self.SOURCE, datetime.date):
            pass
        elif isinstance(self.SOURCE, datetime.time):
            pass
        elif isinstance(self.SOURCE, datetime.timedelta):
            # pass
            raise NotImplementedError()
        elif isinstance(self.SOURCE, int):
            raise NotImplementedError()
        elif isinstance(self.SOURCE, float):
            raise NotImplementedError()
        else:
            raise NotImplementedError()

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
    def __cmp__(self, other: Any) -> int | NoReturn:
        pass    # TODO: FINISH!

        other = self.__class__(other)
        source1 = self.SOURCE
        source2 = other.SOURCE

        if isinstance(self.SOURCE, datetime.datetime) and isinstance(other.SOURCE, datetime.datetime):
            if source1 < source2:
                return -1
            elif source1 == source2:
                return 0
            elif source1 > source2:
                return 1

        elif isinstance(self.SOURCE, datetime.date) or isinstance(other.SOURCE, datetime.date):
            for attr in ["year", "month", "day"]:
                if getattr(source1, attr) < getattr(source2, attr):
                    return -1
                elif getattr(source1, attr) == getattr(source2, attr):
                    pass
                elif getattr(source1, attr) > getattr(source2, attr):
                    return 1
            return 0

        elif isinstance(self.SOURCE, datetime.time) or isinstance(other.SOURCE, datetime.time):
            for attr in ["hour", "minute", "second", "microsecond"]:
                if getattr(source1, attr) < getattr(source2, attr):
                    return -1
                elif getattr(source1, attr) == getattr(source2, attr):
                    pass
                elif getattr(source1, attr) > getattr(source2, attr):
                    return 1
            return 0

    # -----------------------------------------------------------------------------------------------------------------
    def get_str__by_pat(self, pattern: str) -> str:
        """
        NOTE
        ----
        mainly used internal!

        GOAL
        ----
        make str by pat

        EXAMPLES
        --------
        %Y%m%d_%H%M%S -> 20241203_114845
        add_ms -> 20241203_114934.805854
        """
        return self.SOURCE.strftime(pattern)

    def __getattr__(self, item: str) -> str | NoReturn:
        if item in AttrAux(PatDateTimeFormat).iter__not_hidden():
            if isinstance(self.SOURCE, datetime.datetime):
                pass
            elif isinstance(self.SOURCE, datetime.date):
                item = TextAux(item).clear__regexps("T", "m", flags=re.IGNORECASE)
            elif isinstance(self.SOURCE, datetime.time):
                item = TextAux(item).clear__regexps("D", "w", flags=re.IGNORECASE)

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
    print(repr(DateTimeAux()))
    print(str(DateTimeAux()))
    print()

    print(DateTimeAux().T)
    print(DateTimeAux().Tm)
    print()

    print(DateTimeAux().D)
    print(DateTimeAux().DT)
    print(DateTimeAux().DwTm)
    print()

    inst = DateTimeAux(datetime.date(2024, 2, 1))
    print(inst)
    print(inst.DT)
    print(inst.DwTm)

    inst = DateTimeAux(datetime.time(11, 50, 1, 123))
    print(inst)
    print(inst.DT)
    print(inst.DwTm)

    # inst = DateTimeAux(datetime.timedelta(11, 50, 1, 123))
    # print(inst)
    # print(inst.DT)
    # print(inst.DwTm)

    inst = DateTimeAux(datetime.datetime.now().date())
    print(inst)
    print(inst.DT)
    print(inst.DwTm)


# =====================================================================================================================
