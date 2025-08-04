import numpy as np
import pandas as pd

from dataclasses import dataclass
from base_aux.aux_np_pd.m0_typing import *

from base_aux.base_nest_dunders.m1_init3_params_dict_kwargs_update import *
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_args_kwargs import *
from base_aux.aux_dict.m2_dict_ic import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *

# calculates ta_meth!!!
import pandas_ta as ta  # VERY IMPORTANT!!! even if no used!


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
    SOURCE: TYPING__NP_TS__FINAL    # HISTORY input - from MT5 - todo: update to DF? use with loaded TA data?
    DF: TYPING__PD_DATAFRAME        # result OUTPUT - from PD_TA

    # ---------------------------
    NAME: str = "DEF_IndNameInfo"                       # just info!
    PARAMS: DictIc_LockedKeys_Ga
    COLUMN_SETINGS: DictIcKeys[str, ColumnSettings]     # if not know what to use - keep blanc str "" or None!!!

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
        self._init_post0__pd_set_options()
        self._init_post0__fix_attrs()
        self._init_post1__warn_if_not_enough_history()
        self._init_post2__calculate_ta()
        self._init_post3__ensure_df()
        # self._init_post4__apply_time_indexes()
        self._init_post5__rename_columns()
        self._init_post6__round_values()
        self.init_post7__calculate_extra_columns()

    @staticmethod
    def _init_post0__pd_set_options():
        pd.set_option('display.max_columns', 500)  # сколько столбцов показываем
        pd.set_option('display.width', 1500)  # макс. ширина таблицы для показа

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

    def _init_post3__ensure_df(self) -> None:
        """
        GOAL
        ----
        when indicator calculated into pdSeries instead of pdDataframe
        like for singleDimentional as Wma/Stoch/
        1. reformat into DF
        2. set name if NONAME column
        """
        if isinstance(self.DF, pd.core.series.Series):
            self.DF = pd.DataFrame(self.SOURCE)

    def _init_post4__apply_time_indexes(self) -> None:
        """
        GOAL
        ----
        pd_ta create indexes only as position index!
        so i want to apply original "time" indexes and be able to combine/concatenate several DF expecting same TIME!
        at least for cmp!
        """
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH

    def _init_post5__rename_columns(self) -> None:
        """
        GOAL
        ----
        rename columns to use finals simple names!
        """
        for col_original in self.DF.columns:
            for col_name, col_settings in self.COLUMN_SETINGS.items():
                if col_settings.EQ == col_original:
                    self.DF.rename({col_original: col_name})

    def _init_post6__round_values(self) -> None:
        """
        GOAL
        ----
        round indicator calculations
        """
        # df = df.iloc[:].round(indicator_obj.ROUND)    # old logic

        for col_name, col_settings in self.COLUMN_SETINGS.items():
            # round - did not work INLINE!!! - need resave!
            self.DF[col_name] = self.DF[col_name].round(col_settings.ROUND)

    def init_post7__calculate_extra_columns(self) -> None:
        """
        GOAl
        ----
        do extra calculations like for geom sums in addition for common indicator
        """
        return NotImplemented()


# =====================================================================================================================
