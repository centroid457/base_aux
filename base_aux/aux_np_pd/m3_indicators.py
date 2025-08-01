import numpy as np
import pandas as pd

from dataclasses import dataclass
from base_aux.aux_np_pd.m0_typing import *

from base_aux.base_nest_dunders.m1_init3_params_dict_kwargs_update import *
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_args_kwargs import *
from base_aux.aux_dict.m2_dict_ic import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# =====================================================================================================================
class ColumnSettings(NamedTuple):
    EQ: str | Base_EqValid | None = None    # none is when you dont know exact
    ROUND: int = 1


# =====================================================================================================================
class Base_Indicator(NestInit_Source, NestInit_ParamsDict_UpdateByKwargs):
    """
    GOAL
    ----
    ON INIT
        1/ init source as PD - dont do smth with source - no shrink! only add new calculations!
        2/ calculate additional exact Indicator PD
    ACCESS
        3/ access to indicator values

    SPECIALLY CREATED FOR
    ---------------------
    input data from mt5
    calculate indicator values
    """
    SOURCE: TYPING__NP_TS__FINAL    # HISTORY input - from MT5
    DF: TYPING__PD_DATAFRAME        # result OUTPUT - from PD_TA

    # ---------------------------
    NAME: str = "DEF_IndNameInfo"                       # just info!
    PARAMS: DictIc_LockedKeys_Ga
    COLUMN_SETINGS: DictIcKeys[str, ColumnSettings]     # if not know what to use - keep blanc str "" or None!!!
    COLUMN_NAME__NONAME: str = "DEF_IndNoNameColumn"    # when TA_METH return pdSeries instead of pdDf

    @property
    def TA_METH(self) -> Callable[..., TYPING__PD_DATAFRAME | TYPING__PD_SERIES]:
        """
        GOAL
        ----
        exact method for making calculations for TA

        NOTE
        ----
        use property! or find solution to use in classmethod!!
        """
        raise NotImplementedError()

    @property
    def HISTORY_ENOUGH_THRESH(self) -> int:
        """
        GOAL
        ----
        calculate (for exact params) history depth wich is enough for correct calculations the indicator

        ORIGINAL IDEA
        -------------
        РАСЧЕТ ДЛИНЫ БАРОВ
            количество влияет на результат!!!!
            при не особо достаточном количестве баров - расчет произойдет НО значения будут отличаться от фактического!!!
            видимо из-за того что будет расчитываться с нулевыми некоторыми начальными значениями!!!

            sum * 2 = это очень мало!!!!!
            sum * 10 = кажется первая, что вообще показала полное совпадение с Tinkoff терминалом!!!

            ADX
                !!! ЭТО ОЧЕНЬ ВАЖНО ДЛЯ ADX !!!!
            STOCH
                вообще не важно - кажется там сколько длина его - столько и баров достаточно!!!
        """
        return sum(self.PARAMS.values()) * 10

    # -----------------------------------------------------------------------------------------------------------------
    # TODO: decide what to do with Series/Tail/Last or use help to direct access after!!! --- use originally indexing

    def __getattr__(self, item: str) -> TYPING__PD_SERIES | NoReturn:
        """
        GOAL
        ----
        return exact Indicator values series from DF!!!

        NOTE
        ----
        result_last_element = df.iloc[len(df) - 1]
        result_full_series = df
        result_tail_cut = df[-return_tail::]
        """
        try:
            column_name = self.COLUMN_SETINGS.key__get_original(item)
            return self.DF[column_name]
        except Exception as exx:
            Warn(f"{item=}/{exx!r}")
            raise exx

    # -----------------------------------------------------------------------------------------------------------------
    def init_post(self) -> None:
        """
        GOAL
        ----
        do all final calculates and fixes on source
        """
        self._init_post0__fix_attrs()
        self._init_post1__warn_if_not_enough_history()
        self._init_post2__calculate_ta()
        self._init_post3__df_ensure_colname_and_df()
        self._init_post4__rename_columns()
        self._init_post5__round_values()
        self.init_post6__calculate_extra_columns()

    def _init_post0__fix_attrs(self) -> None:
        """
        GOAL
        ----
        fix/remake/create all attrs if need
        """
        self.DF = pd.DataFrame(self.SOURCE)
        self.COLUMN_SETINGS = DictIcKeys(self.COLUMN_SETINGS)    # just make a cls COPY to self

    def _init_post1__warn_if_not_enough_history(self) -> None:
        """
        GOAL
        ----
        main goal - Warn if not enough lines to calculate correct values
        """
        len_source = len(self.SOURCE)
        try:
            if len_source < self.HISTORY_ENOUGH_THRESH:
                Warn(f"{len_source=}/{self.HISTORY_ENOUGH_THRESH=}")
        except Exception as exx:
            Warn(f"{len_source=}/{exx!r}")

    def _init_post2__calculate_ta(self) -> None:
        """
        GOAL
        ----
        do exact TA calculations
        """
        self.DF = self.TA_METH(**self.PARAMS)

    def _init_post3__df_ensure_colname_and_df(self) -> None:
        """
        GOAL
        ----
        when indicator calculated into pdSeries instead of pdDataframe
        like for singleDimentional as Wma/Stoch/
        1. reformat into DF
        2. set name if NONAME column
        """
        if isinstance(self.DF, pd.core.series.Series):
            if self.DF.name is None:
                self.DF.name = self.COLUMN_NAME__NONAME
            self.DF = pd.DataFrame(self.SOURCE)

    def _init_post4__rename_columns(self) -> None:
        """
        GOAL
        ----
        rename columns to use finals simple names!
        """
        for col_original in self.DF.columns:
            for col_name, col_settings in self.COLUMN_SETINGS.items():
                if col_settings.EQ == col_original:
                    self.DF.rename({col_original: col_name})

    def _init_post5__round_values(self) -> None:
        """
        GOAL
        ----
        round indicator calculations
        """
        # df = df.iloc[:].round(indicator_obj.ROUND)    # old logic

        for col_name, col_settings in self.COLUMN_SETINGS.items():
            self.DF[col_name].round(col_settings.ROUND)

    def init_post6__calculate_extra_columns(self) -> None:
        """
        GOAl
        ----
        do extra calculations like for geom sums in addition for common indicator
        """
        return NotImplemented()


# =====================================================================================================================
class Indicator_Wma(Base_Indicator):
    """
    COLUMN_NAME__TEMPLATE = WMA_%(length)s
    """
    NAME = "WMA"
    COLUMN_SETINGS = dict(
        WMA=ColumnSettings(EqValid_Regexp(r"WMA_\d+"), 1),
    )
    PARAMS: DictIc_LockedKeys_Ga = DictIc_LockedKeys_Ga(
        length=12,
    )
    COLUMN_NAME__NONAME = "WMA"

    # results -----
    WMA: Any

    @property
    def TA_METH(self) -> Callable[..., Any]:
        return self.DF.ta.wma

    @property
    def HISTORY_ENOUGH_THRESH(self) -> int:
        return self.PARAMS.length


# ---------------------------------------------------------------------------------------------------------------------
class Indicator_Rsi(Base_Indicator):
    """
    length: int

    COLUMN_NAME__TEMPLATE: str = "RSI_%(length)s"
    ROUND: int = 1
    """
    NAME = "RSI"
    COLUMN_SETINGS = dict(
        RSI=ColumnSettings(EqValid_Regexp(r"RSI_\d+"), 1),
    )
    PARAMS: DictIc_LockedKeys_Ga = DictIc_LockedKeys_Ga(
        length=12,
    )
    COLUMN_NAME__NONAME = "RSI"

    # results -----
    RSI: Any

    @property
    def TA_METH(self) -> Callable[..., Any]:
        return self.DF.ta.rsi

    @property
    def HISTORY_ENOUGH_THRESH(self) -> int:
        return self.PARAMS.length


# =====================================================================================================================
class Indicator_Adx(Base_Indicator):
    """
    length: int
    lensig: int
    "ADX_%(lensig)s"
    """
    NAME = "ADX"
    COLUMN_SETINGS = dict(
        ADX=ColumnSettings(EqValid_Regexp(r"ADX_\d+"), 1),
        DMP=ColumnSettings(EqValid_Regexp(r"DMP_\d+"), 1),
        DMN=ColumnSettings(EqValid_Regexp(r"DMN_\d+"), 1),
    )
    PARAMS: DictIc_LockedKeys_Ga = DictIc_LockedKeys_Ga(
        length=13,
        lensig=9,
    )

    # results -----
    ADX: Any
    DMP: Any
    DMN: Any

    @property
    def TA_METH(self) -> Callable[..., Any]:
        return self.DF.ta.adx

    @property
    def HISTORY_ENOUGH_THRESH(self) -> int:
        return sum(self.PARAMS.values()) * 10


# ---------------------------------------------------------------------------------------------------------------------
class Indicator_Macd(Base_Indicator):
    """
    fast: int
    slow: int
    signal: int

    ROUND: int = 3

    @property
    def COLUMN_NAME__TEMPLATE(self) -> str:
        if self.slow < self.fast:
            return "MACDh_%(slow)s_%(fast)s_%(signal)s"
        else:
            return "MACDh_%(fast)s_%(slow)s_%(signal)s"
    """
    NAME = "MACD"
    COLUMN_SETINGS = dict(
        MACD=ColumnSettings(EqValid_Regexp(r"MACD(?:_\d+){3}"), 3),     # check
        HIST=ColumnSettings(EqValid_Regexp(r"MACDh(?:_\d+){3}"), 3),
        SIG=ColumnSettings(EqValid_Regexp(r"MACDs(?:_\d+){3}"), 3),  # check
    )
    PARAMS: DictIc_LockedKeys_Ga = DictIc_LockedKeys_Ga(
        fast=12,
        slow=26,
        signal=9,
    )

    # results -----
    MACD: Any
    HIST: Any
    SIG: Any

    @property
    def TA_METH(self) -> Callable[..., Any]:
        return self.DF.ta.macd

    @property
    def HISTORY_ENOUGH_THRESH(self) -> int:
        return sum(self.PARAMS.values()) * 10


# ---------------------------------------------------------------------------------------------------------------------
class Indicator_Stoch(Base_Indicator):
    """
    always work with 14/3/3!!!

    fast_k: int
    slow_k: int
    slow_d: int

    COLUMN_NAME__TEMPLATE: str = "STOCHk_%(fast_k)s_%(slow_k)s_%(slow_d)s"
    COLUMN_NAME__TEMPLATE: str = "STOCHk_14_3_3"
    """
    NAME = "STOCH"
    COLUMN_SETINGS = dict(
        STOCH=ColumnSettings(EqValid_Regexp(r"STOCHk(?:_\d+){3}"), 1),
        STOCHd=ColumnSettings(EqValid_Regexp(r"STOCHd(?:_\d+){3}"), 1),
    )
    PARAMS: DictIc_LockedKeys_Ga = DictIc_LockedKeys_Ga(
        fast_k=3,
        slow_k=14,
        slow_d=3,
    )

    # results -----
    STOCH: Any
    STOCHd: Any

    @property
    def TA_METH(self) -> Callable[..., Any]:
        return self.DF.ta.stoch

    @property
    def HISTORY_ENOUGH_THRESH(self) -> int:
        return self.PARAMS.slow_k


# =====================================================================================================================
