from enum import Enum

import numpy as np
import pandas as pd

from dataclasses import dataclass
from base_aux.aux_attr.m1_annot_attr1_aux import *

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_nest_dunders.m1_init3_params_dict_kwargs_update import *
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_args_kwargs import *
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_dict.m2_dict_ic import *


# =====================================================================================================================
TYPING__PD_SERIES = pd.core.series.Series
# TYPING__PD_SERIES = pd.Series


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
    """
    SOURCE: np.ndarray      # HISTORY input
    DF: TYPING__PD_SERIES   # OUTPUT

    PARAMS: DictIc_LockedKeys_Ga

    # UNIVERSAl -------------
    NAME: str = "DEF_IndNameInfo"                       # just info!
    ROUND_VALUES: int | tuple[int, ...] = 1             # each for each column! or one for all!
    COLUMN_NAMES: DictIcKeys[str, str | Base_EqValid]   # if not know what to use - keep blanc str "" or None!!!

    # TODO:
    #  - rename columns!!!
    #  - values as EqValid or pattern! not just a simple final values!

    # def __init__(self, source: Any, **kwargs):
    #     pass

    # ANNOTS LAST ----------
    pass    # KEEP ALWAYS ALL LAST!!!

    # ACCESS ---------------
    def __getattr__(self, item: str) -> TYPING__PD_SERIES | NoReturn:   # TODO: use NpNdArray???
        """
        GOAL
        ----
        return exact Indicator values DF!!!
        """
        column_name = self.COLUMN_NAMES[item]
        try:        # FIXME: check directly?
            # if result gives only one column - its not have header! so it will raise!
            # like WMA!
            # but it used for others! like ADX/STOCH/MACD!
            return self.DF[column_name]
        except Exception as exx:
            raise exx

        return self.DF

    # TODO: decide what to do with Series/Tail/Last or use help to direct access after!!!

    # INITS ----------------
    # def __init__(self, source, **kwargs):
    #     pass
    #     super().__init__(**kwargs)

    @property
    def ENOUGH_LINES_THRESH(self) -> int:
        raise NotImplementedError()

    def init_post(self) -> None:
        """
        GOAL
        ----
        do all final calculates and fixes on source
        """
        self._init_post0_fix_attrs()
        self._init_post1_warn_if_not_enough_data()
        self._init_post2_fix_column_templates()
        self.init_post3_calculate_values()
        self._init_post4_rename_columns()
        self._init_post5_round_values()

    def _init_post0_fix_attrs(self) -> None:
        """
        GOAL
        ----
        fix/remake/create all attrs if need
        """
        self.DF = pd.DataFrame(self.SOURCE)
        self.COLUMN_NAMES = DictIcKeys(self.COLUMN_NAMES)    # just make a cls copy to self

        # round
        count_col = len(self.COLUMN_NAMES)
        if isinstance(self.ROUND_VALUES, int):
            self.ROUND_VALUES = (self.ROUND_VALUES, ) * count_col

    def _init_post1_warn_if_not_enough_data(self) -> None:
        """
        GOAL
        ----
        main goal - Warn if not enough lines to calculate correct values
        """
        len_source = len(self.SOURCE)
        if len_source < self.ENOUGH_LINES_THRESH:
            Warn(f"{len_source=}/{self.ENOUGH_LINES_THRESH=}")

    def _init_post2_fix_column_templates(self) -> None:
        """
        GOAL
        ----
        load all params in templates
        """
        attrs_dict = AttrAux_AnnotsLast(self).dump_dict__skip_raised()

        for name, value in self.COLUMN_NAMES.items():
            if isinstance(value, str):
                value = value % attrs_dict
                self.COLUMN_NAMES[name] = value

    def init_post3_calculate_values(self) -> None:
        """
        GOAL
        ----
        do exact calculations
        """
        raise NotImplementedError()

    def _init_post4_rename_columns(self) -> None:
        """
        GOAL
        ----
        rename columns to use finals simple names!
        """

    def _init_post5_round_values(self) -> None:
        """
        GOAL
        ----
        round indicator calculations
        """
        # TODO: use schema for several columns!
        self.DF = self.DF.iloc[:].round(self.ROUND_VALUES)  # FIXME: use only ind calculated values


# ---------------------------------------------------------------------------------------------------------------------
class Indicator_Adx(Base_Indicator):
    NAME = "ADX"
    COLUMN_NAMES = dict(adx="ADX_%(lensig)s", adp=None, adn=None)
    PARAMS: DictIc_LockedKeys_Ga = DictIc_LockedKeys_Ga(length=13, lensig=9)

    # results -----
    ADX: Any
    ADP: Any
    ADN: Any

    def init_post3_calculate_values(self) -> None:
        # self.DF = self.DF.ta.adx(**self.PARAMS)
        self.DF = self.DF.ta.adx(length=self.PARAMS.length, lensig=self.PARAMS.lensig)


# =====================================================================================================================











# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
pass    # TODO: OLD ref!
pass    # TODO: OLD ref!
pass    # TODO: OLD ref!
pass    # TODO: OLD ref!
pass    # TODO: OLD ref!
pass    # TODO: OLD ref!
pass    # TODO: OLD ref!


# =====================================================================================================================
class IndicatorName(Enum):  # TODO: add IC!
    WMA = "WMA"
    STOCH = "STOCH"
    ADX = "ADX"
    MACD = "MACD"
    RSI = "RSI"


# =====================================================================================================================
class Base_IndicatorParams:
    NAME: IndicatorName = None
    COLUMN_NAME__TEMPLATE: str = None
    ROUND: int = None

    def __iter__(self):
        yield from self.params_dict__get().values()

    def column_name__get(self) -> str:
        return self.COLUMN_NAME__TEMPLATE % self.params_dict__get()

    def params_dict__get(self):
        return AttrAux_AnnotsAll(self).dump_dict()

    def bars_expected__get(self) -> int:
        """
        РАСЧЕТ ДЛИНЫ БАРОВ
            количество влияет на результат!!!!
            при не особо достаточном количестве баров - расчет произойдет НО значения будут отличаться от фактического!!!
            видимо из-за того что будет вычитаться с нулевыми некоторыми начальными значениями!!!

            sum * 2 = это очень мало!!!!!
            sum * 10 = кажется первая, что вообще показала полное совпадение с Tinkoff терминалом!!!

            ADX
                !!! ЭТО ОЧЕНЬ ВАЖНО ДЛЯ ADX !!!!
            STOCH
                вообще не важно - кажется там сколько длина его - столько и баров достаточно!!!
        """
        return sum(self) * 10


# =====================================================================================================================
@dataclass
class IndicatorParams_WMA(Base_IndicatorParams):
    length: int

    NAME: IndicatorName = IndicatorName.WMA
    # FUNCTION: Callable = ta.wma     # NOT WORKING!
    COLUMN_NAME__TEMPLATE: str = "WMA_%(length)s"
    ROUND: int = 1


@dataclass
class IndicatorParams_STOCH(Base_IndicatorParams):
    """
    always work with 14/3/3!!!
    """
    fast_k: int
    slow_k: int
    slow_d: int

    NAME: IndicatorName = IndicatorName.STOCH
    COLUMN_NAME__TEMPLATE: str = "STOCHk_%(fast_k)s_%(slow_k)s_%(slow_d)s"
    # COLUMN_NAME__TEMPLATE: str = "STOCHk_14_3_3"
    ROUND: int = 1


@dataclass
class IndicatorParams_ADX(Base_IndicatorParams):
    length: int
    lensig: int

    NAME: IndicatorName = IndicatorName.ADX

    COLUMN_NAME__TEMPLATE: str = "ADX_%(lensig)s"
    ROUND: int = 1


@dataclass
class IndicatorParams_MACD(Base_IndicatorParams):
    fast: int
    slow: int
    signal: int

    NAME: IndicatorName = IndicatorName.MACD
    ROUND: int = 3

    @property
    def COLUMN_NAME__TEMPLATE(self) -> str:
        if self.slow < self.fast:
            return "MACDh_%(slow)s_%(fast)s_%(signal)s"
        else:
            return "MACDh_%(fast)s_%(slow)s_%(signal)s"


@dataclass
class IndicatorParams_RSI(Base_IndicatorParams):
    length: int

    NAME: IndicatorName = IndicatorName.RSI

    COLUMN_NAME__TEMPLATE: str = "RSI_%(length)s"
    ROUND: int = 1


# =====================================================================================================================
