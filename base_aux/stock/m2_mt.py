from typing import *

import time
import datetime as dt
import re
import json
import threading

import MetaTrader5 as mt5
import pandas as pd
import numpy as np

from base_aux.base_nest_dunders.m1_init3_reinit_lambdas_resolve import *
from base_aux.base_statics.m2_exceptions import *
from base_aux.stock.m0_symbols import *
from base_aux.stock.m1_time_series import *
from base_aux.stock.m3_indicators import *

from base_aux.privates.m1_privates import *
from base_aux.aux_attr.m4_kits import *
from base_aux.alerts.m1_alert0_base import *
from base_aux.aux_types.m2_info import *


# =====================================================================================================================
# TODO: ADD STABILITY STRESSFUL! like in IMAP!!!! connect if lost!


# =====================================================================================================================
TYPING__SYMBOL_FINAL = mt5.SymbolInfo
TYPING__SYMBOL_DRAFT = Union[str, mt5.SymbolInfo]
TYPING__TF = int
TYPING__PD_SERIES = pd.core.series.Series
TYPING__INDICATOR_VALUES = Union[None, float, TYPING__PD_SERIES]


# =====================================================================================================================
class MT5(NestInit_AttrsLambdaResolve):
    CONN_AUTH = PvLoaderIni_AuthServer(keypath=("AUTH_MT5_DEF",))

    SYMBOL: TYPING__SYMBOL_FINAL = Symbols.BRENT_UNIVERSAL
    TF: TYPING__TF = mt5.TIMEFRAME_M10
    __SYMBOLS_AVAILABLE: list[mt5.SymbolInfo] = None

    BAR_LAST: np.ndarray = None
    """
    time
    (1675118400, 85.41, 85.43, 85.21, 85.21, 225, 1, 1065)

    bar["time"] --> 1675118400
    """
    TICK_LAST: mt5.Tick = None
    """
    self.BAR_LAST_TICK=Tick(time=1675468684, bid=83.45, ask=83.51, last=83.5, volume=6, time_msc=1675468684950, flags=30, volume_real=6.0)
    type(self.BAR_LAST_TICK)=<class 'Tick'>
    """

    _symbols__volume_price: dict[str, float] = {}     # collect in threads! dont delete!

    # =================================================================================================================
    def __init__(
            self,
            tf: TYPING__TF = None,
            symbol: TYPING__SYMBOL_DRAFT = None
    ) -> None | NoReturn:
        super().__init__()

        self.TF = tf or self.TF
        self.SYMBOL = symbol or self.SYMBOL

        # self.mt5_connect()

    def __del__(self):
        mt5.shutdown()

    # CONNECT ---------------------------------------------------------------------------------------------------------
    def mt5_connect(self) -> None | NoReturn:
        result = mt5.initialize(login=int(self.CONN_AUTH.NAME), password=self.CONN_AUTH.PWD, server=self.CONN_AUTH.SERVER)
        msg = f"[{result}]initialize[{mt5.last_error()=}]"
        print(msg)
        if not result:
            msg += f"SMTIMES PWD DROPPED_DOWN/CORRUPTED in MT5!!! - you should simply update it in MT5"
            msg += f"\n{self.CONN_AUTH}"
            print(msg)
            raise ConnectionError(msg)

        self._SYMBOL_init()

    # SYMBOL ==========================================================================================================
    def _SYMBOL_init(self) -> None | NoReturn:
        self.SYMBOL = self.SYMBOL__get_active()

    def SYMBOL__get_active(self, _symbol: TYPING__SYMBOL_DRAFT = None) -> Union[mt5.SymbolInfo, NoReturn]:
        _symbol = _symbol or self.SYMBOL
        if isinstance(_symbol, str):
            _symbol = mt5.symbol_info(_symbol)
            last_error = mt5.last_error()
            if last_error[0] != 1:
                msg = f"incorrect {_symbol=}/{last_error=}"
                raise Exx__NotExistsNotFoundNotCreated(msg)

        if not isinstance(_symbol, mt5.SymbolInfo):
            msg = f"incorrect {_symbol=}"
            raise Exx__NotExistsNotFoundNotCreated(msg)

        return _symbol

    def TF__get_active(self, _tf: TYPING__TF = None) -> TYPING__TF:
        return _tf or self.TF

    # AVAILABLE -------------------------------------------------------------------------------------------------------
    @classmethod
    @property
    def SYMBOLS_AVAILABLE(cls) -> list[mt5.SymbolInfo]:
        """
        too much time to get all items! dont use it without special needs!
        """
        if not cls.__SYMBOLS_AVAILABLE:
            cls.__SYMBOLS_AVAILABLE = mt5.symbols_get()
        return cls.__SYMBOLS_AVAILABLE

    def symbols_available__by_mask(
            self,
            mask: str = "",
            only_rus: bool = False
    ) -> list[mt5.SymbolInfo]:
        # count=12976 ALL!!!!
        # count=275 rus!!!!
        count = 0
        result = []

        if not mask:
            symbols = self.SYMBOLS_AVAILABLE
        else:
            symbols = list(filter(lambda x: x.name.startswith(mask), self.SYMBOLS_AVAILABLE))

        print("*"*100)
        for item in symbols:
            # FILTER LONG NAMES like for Options
            if len(item.name) > 5:
                continue

            # FILTER RUS
            if only_rus:
                if any([
                    item.isin != "moex.stock",
                    not re.match(pattern=r"[а-яА-Я]", string=item.description),
                    item.name.startswith("RU00"),
                    # item.currency_base != "RUS",  # always OK!
                    # "-RM" in item.name,     #count=12301
                ]):
                    continue

            # GET
            count += 1
            result.append(item)
            print(item.name)

        print("*"*100)
        print(f"result={[item.name for item in result]}")
        print(f"{count=}")
        print("*"*100)

        return result

    # SHOW ------------------------------------------------------------------------------------------------------------
    def _mt5_symbol_show(self, show: bool = True, _symbol: TYPING__SYMBOL_DRAFT = None) -> bool:
        _symbol = self.SYMBOL__get_active(_symbol)
        result = mt5.symbol_select(_symbol.name, show)
        print(f"[{result}]_mt5_symbol_show({_symbol})={mt5.last_error()=}")
        return result

    def _mt5_symbol_show__check(self, _symbol: TYPING__SYMBOL_DRAFT = None) -> bool:
        _symbol = self.SYMBOL__get_active(_symbol)
        if _symbol:
            return _symbol.select

    # INFO ------------------------------------------------------------------------------------------------------------
    def _symbols_info__print_compare(self, symbols: list[TYPING__SYMBOL_DRAFT] = ["SBER", "AAPL-RM", "PYPL-RM"]):
        """
        since SYMBOL_NAME not added into chart gui list - it will return zero to many attributes!

        ****************************************************************************************************
        INSTRUMENTS                   =['SBER', 'AAPL-RM', 'PYPL-RM']
        ****************************************************************************************************
        custom                        =[False, False, False]
        chart_mode                    =[1, 1, 1]
        select                        =[True, False, False]
        visible                       =[True, False, False]
        session_deals                 =[0, 0, 0]
        session_buy_orders            =[0, 0, 0]
        session_sell_orders           =[0, 0, 0]
        volume                        =[34, 0, 0]
        volumehigh                    =[12811, 0, 0]
        volumelow                     =[1, 0, 0]
        time                          =[1671839399, 0, 0]
        digits                        =[2, 0, 0]
        spread                        =[6, 0, 0]
        spread_float                  =[True, True, True]
        ticks_bookdepth               =[32, 32, 32]
        trade_calc_mode               =[32, 32, 32]
        trade_mode                    =[4, 4, 4]
        start_time                    =[0, 0, 0]
        expiration_time               =[0, 0, 0]
        trade_stops_level             =[0, 0, 0]
        trade_freeze_level            =[0, 0, 0]
        trade_exemode                 =[3, 3, 3]
        swap_mode                     =[0, 0, 0]
        swap_rollover3days            =[3, 3, 3]
        margin_hedged_use_leg         =[False, False, False]
        expiration_mode               =[15, 15, 15]
        filling_mode                  =[3, 3, 3]
        order_mode                    =[63, 63, 63]
        order_gtc_mode                =[2, 2, 2]
        option_mode                   =[0, 0, 0]
        option_right                  =[0, 0, 0]
        bid                           =[137.85, 0.0, 0.0]
        bidhigh                       =[139.01, 0.0, 0.0]
        bidlow                        =[136.81, 0.0, 0.0]
        ask                           =[137.91, 0.0, 0.0]
        askhigh                       =[138.36, 0.0, 0.0]
        asklow                        =[136.82, 0.0, 0.0]
        last                          =[137.94, 0.0, 0.0]
        lasthigh                      =[138.26, 0.0, 0.0]
        lastlow                       =[136.81, 0.0, 0.0]
        volume_real                   =[34.0, 0.0, 0.0]
        volumehigh_real               =[12811.0, 0.0, 0.0]
        volumelow_real                =[1.0, 0.0, 0.0]
        option_strike                 =[0.0, 0.0, 0.0]
        point                         =[0.01, 1.0, 1.0]
        trade_tick_value              =[0.1, 1.0, 1.0]
        trade_tick_value_profit       =[0.1, 1.0, 1.0]
        trade_tick_value_loss         =[0.1, 1.0, 1.0]
        trade_tick_size               =[0.01, 1.0, 1.0]
        trade_contract_size           =[10.0, 1.0, 1.0]
        trade_accrued_interest        =[0.0, 0.0, 0.0]
        trade_face_value              =[0.0, 0.0, 0.0]
        trade_liquidity_rate          =[1.0, 1.0, 1.0]
        volume_min                    =[1.0, 1.0, 1.0]
        volume_max                    =[100000000.0, 100000000.0, 100000000.0]
        volume_step                   =[1.0, 1.0, 1.0]
        volume_limit                  =[0.0, 0.0, 0.0]
        swap_long                     =[0.0, 0.0, 0.0]
        swap_short                    =[0.0, 0.0, 0.0]
        margin_initial                =[0.0, 0.0, 0.0]
        margin_maintenance            =[0.0, 0.0, 0.0]
        session_volume                =[0.0, 0.0, 0.0]
        session_turnover              =[0.0, 0.0, 0.0]
        session_interest              =[0.0, 0.0, 0.0]
        session_buy_orders_volume     =[0.0, 0.0, 0.0]
        session_sell_orders_volume    =[0.0, 0.0, 0.0]
        session_open                  =[137.49, 0.0, 0.0]
        session_close                 =[137.69, 0.0, 0.0]
        session_aw                    =[0.0, 0.0, 0.0]
        session_price_settlement      =[0.0, 0.0, 0.0]
        session_price_limit_min       =[0.0, 0.0, 0.0]
        session_price_limit_max       =[0.0, 0.0, 0.0]
        margin_hedged                 =[0.0, 0.0, 0.0]
        price_change                  =[0.1816, 0.0, 0.0]
        price_volatility              =[0.0, 0.0, 0.0]
        price_theoretical             =[0.0, 0.0, 0.0]
        price_greeks_delta            =[0.0, 0.0, 0.0]
        price_greeks_theta            =[0.0, 0.0, 0.0]
        price_greeks_gamma            =[0.0, 0.0, 0.0]
        price_greeks_vega             =[0.0, 0.0, 0.0]
        price_greeks_rho              =[0.0, 0.0, 0.0]
        price_greeks_omega            =[0.0, 0.0, 0.0]
        price_sensitivity             =[0.0, 0.0, 0.0]
        basis                         =['', '', '']
        category                      =['', '', '']
        currency_base                 =['RUR', 'RUR', 'RUR']
        currency_profit               =['RUR', 'RUR', 'RUR']
        currency_margin               =['RUR', 'RUR', 'RUR']
        bank                          =['', '', '']
        description                   =['Сбербанк России ПАО ао', 'Apple Inc.', 'PayPal Holdings, Inc.']
        exchange                      =['', '', '']
        formula                       =['', '', '']
        isin                          =['moex.stock', 'moex.stock', 'moex.stock']
        name                          =['SBER', 'AAPL-RM', 'PYPL-RM']
        page                          =['', '', '']
        path                          =['MOEX\\SBER', 'MOEX\\AAPL-RM', 'MOEX\\PYPL-RM']
        ****************************************************************************************************
        """
        items = []
        for symbol in list(symbols):
            item = self.SYMBOL__get_active(symbol)
            if item:
                items.append(item._asdict())
            else:
                symbols.remove(symbol)

        if not items:
            return

        print("*"*100)
        key = "ACTIVES"
        print(f"{key:30}={symbols}")
        print("*"*100)
        for key in items[0]:
            value = []
            for item in items:
                value.append(item.get(key))
            print(f"{key:30}={value}")

        print("*"*100)

    # VOLUME_PRICE -----------------------------------------------------
    def _symbol__get_volume_price(self, _symbol: TYPING__SYMBOL_DRAFT = None, _devider: Optional[int] = None) -> float:
        """
        VolumePrice as priceMean * Volume
        +save result into self.symbols_volume_price for threading usage!

        value will be differ from official because i get mean price!
        https://www.moex.com/ru/marketdata/?g=4#/mode=groups&group=4&collection=3&boardgroup=57&data_type=current&category=main
        """
        _devider = _devider or 1000 * 1000
        bar = self.bars__get(_symbol=_symbol, _tf=mt5.TIMEFRAME_D1)
        # print(f"{bar['real_volume']=}")

        item = mt5.symbol_info(_symbol)
        contracts_per_lot = item.trade_contract_size
        contracts = contracts_per_lot * bar["real_volume"]
        volume_price = contracts * (bar["high"] + bar["low"])/2
        # print(f"{volume_price=}")

        result = round(volume_price[0]/_devider)
        self._symbols_volume_price.update({_symbol: result})    # dont delete! collect in threads!
        return result

    def _symbols__get_volume_price__sorted(self, limit_min=None, limit_max=None, _symbols: Optional[list[str]] = None, _devider: Optional[int] = None) -> dict[str, float]:
        """

        (400 * 1000 * 1000)
        ['SBER', 'GAZP', 'LKOH', 'PLZL', 'MGNT', 'NVTK', 'UWGN', 'LQDT', 'VTBR', 'GMKN', 'LSNG', 'SNGS', 'ROSN', 'CHMF']

        :param limit_min:
        :param limit_max:

{
    "GAZP": 18552,
    "SBER": 16418,
    "LQDT": 14222,
    "TCSG": 10671,
    "VTBR": 4788,
    "FIVE": 4602,
    "LKOH": 4085,
    "NVTK": 4052,
    "GMKN": 3677,
    "PLZL": 3272,
    "AFKS": 2283,
    "ROSN": 2160,
    "TATN": 2115,
    "AFLT": 2069,
    "SELG": 1995,
    "MGNT": 1944,
    "MOEX": 1790,
    "OZON": 1661,
    "SMLT": 1563,
    "WUSH": 1341,
    "RUAL": 1313,
    "SBERP": 1304,
    "CHMF": 1266,
    "MTLR": 1199,
    "RNFT": 1162,
    "SNGS": 1143,
    "NLMK": 1092,
    "PIKK": 1079,
    "IRKT": 975,
    "MAGN": 970,
    "TRNFP": 936,
    "SPBE": 889,
    "UPRO": 882,
    "VKCO": 862,
    "ALRS": 788,
    "SNGSP": 788,
    "MTSS": 772,
    "RTKM": 746,
    "GRNT": 745,
    "ENPG": 704,
    "FLOT": 703,
    "SGZH": 697,
    "SIBN": 695,
    "UWGN": 639,
    "AGRO": 589,
    "TRUR": 565,
    "BELU": 557,
    "TATNP": 554,
    "PHOR": 503,
    "TMOS": 497,
    "IRAO": 485,
    "TGLD": 450,
    "SFIN": 445,
    "TRMK": 399,
    "EQMX": 388,
    "DASB": 333,
    "MVID": 330,
    "BSPB": 307,
    "MTLRP": 274,
    "GTRK": 268,
    "POSI": 263,
    "UNAC": 247,
    "HYDR": 235,
    "RENI": 224,
    "AKME": 204,
    "GLTR": 186,
    "RASP": 183,
    "BANEP": 178,
    "FESH": 177,
    "FEES": 158,
    "VSMO": 153,
    "HHRU": 144,
    "AQUA": 125,
    "ISKJ": 122,
    "RBCM": 122,
    "TGKN": 121,
    "SVAV": 118,
    "KMAZ": 111,
    "SBMX": 109,
    "MDMG": 107,
    "CBOM": 104
}
        """
        _devider = _devider or 1000 * 1000
        limit_min = limit_min if limit_min is not None else 100 * 1000 * 1000 / _devider
        _symbols = _symbols or Symbols.SYMBOLS__RUS_FINAM

        # LOAD ---------------------------------------------------
        for symbol in _symbols:
            threading.Thread(target=self._symbol__get_volume_price, kwargs=dict(_symbol=symbol, _devider=_devider)).start()

        while threading.active_count() > 1:
            time.sleep(1)

        # FILTER ---------------------------------------------------
        for symbol, value in dict(self._symbols__volume_price).items():
            if limit_max and limit_max < value:
                self._symbols__volume_price.pop(symbol)
            if limit_min > value:
                self._symbols__volume_price.pop(symbol)

        # SORT -----------------------------------------------------
        self._symbols__volume_price = dict(sorted(self._symbols__volume_price.items(), key=lambda x: x[1], reverse=True))

        # PRINT ----------------------------------------------------
        result_pretty = json.dumps(self._symbols__volume_price, indent=4)
        print(result_pretty)
        return self._symbols__volume_price

    # BAR HISTORY =====================================================================================================
    pass

    # BAR -------------------------------------------------------------------------------------------------------------
    def bars__get(
            self,
            count: int = 1,
            tf_split: int = None,
            shrink: bool = None,
            _start: int = None,
            _symbol: TYPING__SYMBOL_DRAFT = None,
            _tf: TYPING__TF = None
    ) -> Union[np.ndarray]:
        """get history bars
        :param tf_split: correct count of bars in case of using split tf

        :_start: 0 is actual not finished!
        ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']
            [(1695763800, 93.83, 93.88, 93.78, 93.88, 172, 1, 723)]
            elem=1695763800/<class 'numpy.int64'>
            elem=93.83/<class 'numpy.float64'>
            elem=93.88/<class 'numpy.float64'>
            elem=93.78/<class 'numpy.float64'>
            elem=93.88/<class 'numpy.float64'>
            elem=172/<class 'numpy.uint64'>
            elem=1/<class 'numpy.intc'>
            elem=723/<class 'numpy.uint64'>

        returns
            1 bars
                [(1741999200, 70.62, 70.62, 70.62, 70.62, 10, 3, 10)]
                ndim                	int         :1
                size                	int         :1
            2 bars
                [(1741998600, 70.61, 70.62, 70.61, 70.62,  7, 3,  7)
                 (1741999200, 70.62, 70.62, 70.62, 70.62, 10, 3, 10)]
                ndim                	int         :1
                size                	int         :2
        """
        _symbol = self.SYMBOL__get_active(_symbol)
        _tf = self.TF__get_active(_tf)
        tf_split = tf_split or 1

        if _start is None:
            _start = 1

        bars = mt5.copy_rates_from_pos(_symbol.name, _tf, _start, count * tf_split)
        # if not bars:
        #     print(f"{_symbol=}/{bars=}")
        #     return

        # for bar in bars:
        #     print(f"{type(bar)}={bar}")     # <class 'numpy.void'>=(1671753600, 137.49, 138.26, 136.81, 137.94, 53823, 0, 2283422)

        if tf_split > 1 and shrink:
            bars = TimeSeriesAux(bars).shrink(tf_split)

        # if count == 1:
        #     # bars = [(1695729000, 92.3, 92.42, 92.22, 92.23, 944, 1, 3381)]
        #     return bars[0]  # numpy.void
        # else:
        #     # bars = [(1695728400, 92.16, 92.32, 92.1, 92.31, 578, 1, 2764)
        #     #         (1695729000, 92.3, 92.42, 92.22, 92.23, 944, 1, 3381)]
        #     return bars     # numpy.ndarray

        return bars

    def bar_new__wait(self, sleep: int = 10) -> None:
        # TODO: use BarTime to resolve LOST!!!
        count = 0
        while not self.bar_last__update():
            count += 1
            if False:
                self.bar__lost = True
                msg = f"[WARN]bar lost [{count=}]"
                print(msg)
            print(f"bar_new__wait {count=}")
            time.sleep(sleep)
        self.bar__lost = False

    def bar_last__update(self) -> bool:
        bar_new = self.bars__get(count=1)
        if not self.BAR_LAST or bar_new != self.BAR_LAST:
            self.BAR_LAST = bar_new
            return True
        else:
            return False

    def tick_last__update(self, _symbol: TYPING__SYMBOL_DRAFT = None, wait_tick_load: bool = True) -> bool:
        """

        SYMBOL_NAME have to be in terminal! otherwise error
            [False]tick_last__update()=mt5.last_error()=(-4, 'Terminal: Not found')
        """
        _symbol = self.SYMBOL__get_active(_symbol)
        result = False
        while True:
            tick = mt5.symbol_info_tick(self.SYMBOL)
            result = tick != self.TICK_LAST
            if result:
                break

            if not wait_tick_load:
                break
            time.sleep(1)

        if result:
            print(f"update[{self.TICK_LAST=}]{_symbol}/{mt5.last_error()=}")
            # Tick(time=1665770358, bid=62.437, ask=63.312, last=0.0, volume=0, time_msc=1665770358179, flags=6, volume_real=0.0)
            self.TICK_LAST = tick
        return result

    # HISTORY ---------------------------------------------------------------------------------------------------------
    def bars__check_actual(
            self,
            _symbol: TYPING__SYMBOL_DRAFT = None,
            _tf: TYPING__TF = None
    ) -> bool:
        _symbol = self.SYMBOL__get_active(_symbol)
        _tf_td = dt.timedelta(minutes=self.TF__get_active(_tf))

        result = False
        last = self.TICK_LAST
        if last:
            last_dt = dt.datetime.fromtimestamp(last.time)
            result = (last_dt + _tf_td) >= dt.datetime.today()
        return result

    # INDICATOR =======================================================================================================
    def _indicator_get_by_obj(
            self,
            indicator_params: IndicatorParamsBase,
            *,
            return_tail: Optional[int] = 1,
            tf_split: Optional[int] = None,

            _bars: Optional[np.ndarray] = None,
            _add_history: Optional[int] = None,
            _tf: TYPING__TF = None,
            _symbol: TYPING__SYMBOL_DRAFT = None,
    ) -> TYPING__INDICATOR_VALUES:
        # GET -----------------------------
        bars_np = _bars or self.bars__get(
            count=indicator_params.bars_expected__get(),
            tf_split=tf_split,
            shrink=indicator_params.NAME == IndicatorName.ADX,
            _start=_add_history + 1,
            _symbol=_symbol,
            _tf=_tf
        )

        # DF -----------------------------
        df = pd.DataFrame(bars_np)

        # ACTUAL INDICATOR -----------------------------
        params_dict = indicator_params.params_dict__get()
        if indicator_params.NAME == IndicatorName.WMA:
            # df = ta.wma(**df, **params_dict)
            df = df.ta.wma(**params_dict)
        elif indicator_params.NAME == IndicatorName.STOCH:
            df = df.ta.stoch(**params_dict)
            # df = df.ta.stoch(**{"fask_k": 10, "slow_d": 5})
            # df = df.ta.stoch(fast_k=10, slow_k=2, slow_d=2)
        elif indicator_params.NAME == IndicatorName.ADX:
            df = df.ta.adx(**params_dict)
        elif indicator_params.NAME == IndicatorName.MACD:
            df = df.ta.macd(**params_dict)
        else:
            msg = f"cant detect name [{indicator_params.NAME=}]"
            raise Exception(msg)

        # ROUND -----------------------------
        df = df.iloc[:].round(indicator_params.ROUND)

        # FINAL -----------------------------
        name = indicator_params.column_name__get()
        try:        # FIXME: check directly?
            # if result gives only one column - its not have header! so it will raise!
            # like WMA!
            # but it used for others! like ADX/STOCH/MACD!
            df = df[name]
        except:
            pass

        if return_tail == 1:
            result = df.iloc[len(df) - 1]
        elif not return_tail:
            result = df
        else:
            try:
                # if less then need!
                result = df[-return_tail::]
            except:
                pass

        return result

    def indicator_WMA(self, args: Collection[int], **kwargs) -> TYPING__INDICATOR_VALUES:
        return self._indicator_get_by_obj(IndicatorParams_WMA(*args), **kwargs)

    def indicator_STOCH(self, args: Collection[int], **kwargs) -> TYPING__INDICATOR_VALUES:
        return self._indicator_get_by_obj(IndicatorParams_STOCH(*args), **kwargs)

    def indicator_ADX(self, args: Collection[int], **kwargs) -> TYPING__INDICATOR_VALUES:
        return self._indicator_get_by_obj(IndicatorParams_ADX(*args), **kwargs)

    def indicator_MACD(self, args: Collection[int], **kwargs) -> TYPING__INDICATOR_VALUES:
        return self._indicator_get_by_obj(IndicatorParams_MACD(*args), **kwargs)


# =====================================================================================================================
def _explore():
    obj = MT5()
    obj.mt5_connect()
    bar1 = obj.bars__get(1)
    print(bar1)
    ObjectInfo(bar1).print()
    print()
    print()
    print()

    bars2 = obj.bars__get(2)
    print(bars2)
    ObjectInfo(bars2).print()


# =====================================================================================================================
if __name__ == "__main__":
    _explore()


# =====================================================================================================================
