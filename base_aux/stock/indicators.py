from typing import *
from enum import Enum, auto
from dataclasses import dataclass

from base_aux.annots import *


# =====================================================================================================================
class IndicatorName(Enum):
    WMA = 1
    STOCH = 2
    ADX = 3
    MACD = 4
    RSI = 5


# ---------------------------------------------------------------------------------------------------------------------
class IndicatorParams_Base:
    NAME: IndicatorName = None
    COLUMN_NAME__TEMPLATE: str = None
    ROUND: int = None

    def __iter__(self):
        yield from self.params_dict__get().values()

    def column_name__get(self) -> str:
        return self.COLUMN_NAME__TEMPLATE % self.params_dict__get()

    def params_dict__get(self):
        return AnnotAttrs().annots_get_dict(self)

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


# ---------------------------------------------------------------------------------------------------------------------
@dataclass
class IndicatorParams_WMA(IndicatorParams_Base):
    length: int

    NAME: IndicatorName = IndicatorName.WMA
    # FUNCTION: Callable = ta.wma     # NOT WORKING!
    COLUMN_NAME__TEMPLATE: str = "WMA_%(length)s"
    ROUND: int = 1


@dataclass
class IndicatorParams_STOCH(IndicatorParams_Base):
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
class IndicatorParams_ADX(IndicatorParams_Base):
    length: int
    lensig: int

    NAME: IndicatorName = IndicatorName.ADX

    COLUMN_NAME__TEMPLATE: str = "ADX_%(lensig)s"
    ROUND: int = 1


@dataclass
class IndicatorParams_MACD(IndicatorParams_Base):
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
class IndicatorParams_RSI(IndicatorParams_Base):
    length: int

    NAME: IndicatorName = IndicatorName.RSI

    COLUMN_NAME__TEMPLATE: str = "RSI_%(length)s"
    ROUND: int = 1


Type_IndicatorParams = IndicatorParams_Base


# =====================================================================================================================
