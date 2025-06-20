from enum import Enum, auto
from dataclasses import dataclass

from base_aux.aux_attr.m1_annot_attr1_aux import AttrAux_AnnotsAll


# =====================================================================================================================
class IndicatorName(Enum):
    WMA = auto()
    STOCH = auto()
    ADX = auto()
    MACD = auto()
    RSI = auto()


# ---------------------------------------------------------------------------------------------------------------------
class IndicatorParamsBase:
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


# ---------------------------------------------------------------------------------------------------------------------
@dataclass
class IndicatorParams_WMA(IndicatorParamsBase):
    length: int

    NAME: IndicatorName = IndicatorName.WMA
    # FUNCTION: Callable = ta.wma     # NOT WORKING!
    COLUMN_NAME__TEMPLATE: str = "WMA_%(length)s"
    ROUND: int = 1


@dataclass
class IndicatorParams_STOCH(IndicatorParamsBase):
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
class IndicatorParams_ADX(IndicatorParamsBase):
    length: int
    lensig: int

    NAME: IndicatorName = IndicatorName.ADX

    COLUMN_NAME__TEMPLATE: str = "ADX_%(lensig)s"
    ROUND: int = 1


@dataclass
class IndicatorParams_MACD(IndicatorParamsBase):
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
class IndicatorParams_RSI(IndicatorParamsBase):
    length: int

    NAME: IndicatorName = IndicatorName.RSI

    COLUMN_NAME__TEMPLATE: str = "RSI_%(length)s"
    ROUND: int = 1


# =====================================================================================================================
