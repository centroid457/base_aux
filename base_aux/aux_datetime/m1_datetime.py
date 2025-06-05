import datetime
import time

from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.aux_cmp_eq.m1_cmp import *
from base_aux.aux_text.m1_text_aux import *
from base_aux.base_statics.m2_exceptions import *
from base_aux.base_nest_dunders.m2_repr_clsname_str import *


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
TYPE__DT_DRAFT = TYPE__DT_FINAL | str | float | None    #  | int    # NOTE: int is not acceptable!


# =====================================================================================================================
# @final    # select styles
class DateTimeAux(NestCmp, NestRepr__ClsName_SelfStr):
    SOURCE: TYPE__DT_FINAL = None
    STYLE: TYPE__TUPLE_DT_STYLE__FINAL = DateTimeStyle_Tuples.DOTS
    UPDATE_ON_STR: bool = None
    DEF_STR_PATTERN: str = "DT"
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
    def __init__(self, source: TYPE__DT_DRAFT = None, style_tuple: TYPE__TUPLE_DT_STYLE__DRAFT = None, update_on_str: bool = None, def_str_pattern: str = None) -> None | NoReturn:
        self.init_source(source)

        if style_tuple is not None:
            self.STYLE = style_tuple
        if update_on_str is not None:
            self.UPDATE_ON_STR = update_on_str
        if def_str_pattern is not None:
            self.DEF_STR_PATTERN = def_str_pattern

        self._PATTS = PatDateTimeFormat(*self.STYLE)

    def init_source(self, source: TYPE__DT_DRAFT = None) -> None | NoReturn:
        if source is None:
            self.SOURCE = datetime.datetime.now()
        elif isinstance(source, (datetime.datetime, datetime.date, datetime.time, )):
            self.SOURCE = source
        elif isinstance(source, datetime.timedelta):
            # pass
            raise NotImplementedError(f"{source=}")
        elif isinstance(source, float):     # time.time()
            self.SOURCE = datetime.datetime.fromtimestamp(source)
        elif isinstance(source, int):
            raise NotImplementedError(f"{source=}")
        elif isinstance(source, str):
            self.SOURCE = self.parse_str(source, _raise=True)
        elif isinstance(source, self.__class__):
            self.SOURCE = source.SOURCE
        else:
            raise Exx__Incompatible(f"{source=}")

    @staticmethod
    def parse_str(source: str, _raise: bool = None) -> TYPE__DT_FINAL | None | NoReturn:
        nums = TextAux(source).findall(r"\d+")
        nums = list(map(int, nums))
        len_nums = len(nums)
        if len_nums in [6, 7]:
            result = datetime.datetime(*nums)
        elif len_nums == 4:
            result = datetime.time(*nums)
        elif len_nums == 3:
            if len(str(nums[0])) == 4:
                result = datetime.date(*nums)
            else:
                result = datetime.time(*nums)
        else:
            try:
                result = datetime.datetime.fromtimestamp(float(source))
            except:
                result = ""

        if not result and _raise:
            raise Exx__Incompatible(f"{source=}")
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self) -> str:
        if self.UPDATE_ON_STR:
            self.SOURCE = datetime.datetime.now()
        return getattr(self, self.DEF_STR_PATTERN)

    def __int__(self):
        raise NotImplementedError()

    def __float__(self) -> float | NoReturn:
        return self.SOURCE.timestamp()

    # -----------------------------------------------------------------------------------------------------------------
    def __cmp__(self, other: Any) -> int | NoReturn:
        """
        GOAL
        ----
        appropriate CMP with time/date parts!
        """
        # todo: DEPRECATE??
        other = self.__class__(other)
        source1 = self.SOURCE
        source2 = other.SOURCE

        if isinstance(self.SOURCE, datetime.datetime) and isinstance(other.SOURCE, datetime.datetime):  # datetime FIRST!!!
            if source1 < source2:
                return -1
            elif source1 == source2:
                return 0
            elif source1 > source2:
                return 1

        elif isinstance(self.SOURCE, datetime.time) or isinstance(other.SOURCE, datetime.time):     # time SECOND!!!
            for attr in ["hour", "minute", "second", "microsecond"]:
                if getattr(source1, attr) < getattr(source2, attr):
                    return -1
                elif getattr(source1, attr) == getattr(source2, attr):
                    pass
                elif getattr(source1, attr) > getattr(source2, attr):
                    return 1
            return 0

        elif isinstance(self.SOURCE, datetime.date) or isinstance(other.SOURCE, datetime.date):     # date LAST!!! cause datetime(date)!
            for attr in ["year", "month", "day"]:
                if getattr(source1, attr) < getattr(source2, attr):
                    return -1
                elif getattr(source1, attr) == getattr(source2, attr):
                    pass
                elif getattr(source1, attr) > getattr(source2, attr):
                    return 1
            return 0

        else:
            raise NotImplementedError()

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
        if item in AttrAux(PatDateTimeFormat).iter__names_filter__not_hidden():
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


# ---------------------------------------------------------------------------------------------------------------------
class TimeStampRenewStr(DateTimeAux):
    """
    SPECIALLY CREATED FOR
    ---------------------
    Alerts Telegram
    1/ parce value
    2/ update value when string
    """
    STYLE: TYPE__TUPLE_DT_STYLE__FINAL = DateTimeStyle_Tuples.DT
    UPDATE_ON_STR: bool = True


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

    print(time.time())  # float!

    # print(datetime.date(2024, 2, 1).timestamp())
    print(DateTimeAux("2025.02.26 17.00.56"))


# =====================================================================================================================
