from typing import *

from base_aux.aux_np_pd.m3_indicators import *


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
