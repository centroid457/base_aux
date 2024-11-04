from base_aux.stock import *

import time
from typing import *
import datetime as dt
import re
import json
import threading

import MetaTrader5 as mt5

import pandas as pd
import numpy as np

from base_aux.privates import *
from base_aux.alerts import *


# =====================================================================================================================
# TODO: ADD STABILITY STRESSFUL! like in IMAP!!!! connect if lost!


# =====================================================================================================================
Type__Symbol = Union[str, mt5.SymbolInfo]
Type__SymbolOpt = Optional[Type__Symbol]

Type__Tf = int
Type__TfOpt = Optional[Type__Tf]

Type__PdSeries = pd.core.series.Series
Type__IndicatorValues = Union[None, float, Type__PdSeries]


# =====================================================================================================================
class Exx__Mt5Auth(Exception):
    pass


class Exx__Mt5SymbolName(Exception):
    pass


# =====================================================================================================================
class PrivateMT5(PrivateAuthAuto):
    SECTION = "AUTH_MT5_DEF"
    SERVER: str


# =====================================================================================================================
class MT5:
    MT5_AUTH: PrivateMT5 = PrivateMT5()

    SYMBOL: Type__Symbol = "BRX3"
    TF: int = mt5.TIMEFRAME_M10
    __MT5_SYMBOLS_AVAILABLE: List[mt5.SymbolInfo] = None

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

    bar__lost: bool = None        # DONT SET! used only in STRATEGY!!!
    tick__lost: bool = None

    _symbols_volume_price: Dict[str, float] = {}     # used as

    # =================================================================================================================
    def __init__(self, _tf: Optional[int] = None, _symbol: Optional[str] = None):
        super().__init__()

        self.TF = _tf or self.TF
        self.SYMBOL = _symbol or self.SYMBOL

        self.mt5_connect()
        self._SYMBOL_init(exx_if_none=False)

    def __del__(self):
        mt5.shutdown()

    # CONNECT ---------------------------------------------------------------------------------------------------------
    def mt5_connect(self) -> Optional[NoReturn]:
        result = mt5.initialize(login=int(self.MT5_AUTH.USER), password=self.MT5_AUTH.PWD, server=self.MT5_AUTH.SERVER)
        msg = f"[{result}]initialize[{mt5.last_error()=}]"
        print(msg)
        if not result:
            msg += f"БЫВАЕТ СЛЕТАЕТ ПАРОЛЬ!!! становится неверным - нужно просто обновить его в MT5"
            msg += f"\n{self.MT5_AUTH}"

            print(msg)
            raise Exx__Mt5Auth(msg)

    # SYMBOL ==========================================================================================================
    def _SYMBOL_init(self, exx_if_none: bool = True) -> Optional[NoReturn]:
        self.SYMBOL = self.SYMBOL__get_active(exx_if_none=exx_if_none)

    def SYMBOL__get_active(self, _symbol: Type__SymbolOpt = None, exx_if_none: bool = True) -> Union[mt5.SymbolInfo, NoReturn]:
        _symbol = _symbol or self.SYMBOL
        if isinstance(_symbol, str):
            _symbol = mt5.symbol_info(_symbol)
            last_error = mt5.last_error()
            if last_error[0] != 1:
                msg = f"incorrect {_symbol=}/{last_error=}"
                raise Exx__Mt5SymbolName(msg)

        if not isinstance(_symbol, mt5.SymbolInfo):
            msg = f"incorrect {_symbol=}"
            if exx_if_none:
                raise Exx__Mt5SymbolName(msg)

        return _symbol

    def TF__get_active(self, _tf: Type__TfOpt = None):
        return _tf or self.TF

    # AVAILABLE -------------------------------------------------------------------------------------------------------
    @property
    def _MT5_SYMBOLS_AVAILABLE(self) -> List[mt5.SymbolInfo]:
        """
        too much time to get all items! dont use it without special needs!
        """
        if not self.__MT5_SYMBOLS_AVAILABLE:
            self.__MT5_SYMBOLS_AVAILABLE = mt5.symbols_get()
        return self.__MT5_SYMBOLS_AVAILABLE

    def _mt5_symbols_available__find(
            self,
            mask: str = "",
            only_rus: bool = False
    ) -> List[mt5.SymbolInfo]:
        # count=12976 ALL!!!!
        # count=275 rus!!!!
        count = 0
        result: List[mt5.SymbolInfo] = []

        if not mask:
            symbols = self._MT5_SYMBOLS_AVAILABLE
        else:
            symbols = mt5.symbols_get(mask)

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
    def _mt5_symbol_show(self, show: bool = True, _symbol: Type__SymbolOpt = None) -> bool:
        _symbol = self.SYMBOL__get_active(_symbol)
        result = mt5.symbol_select(_symbol.name, show)
        print(f"[{result}]_mt5_symbol_show({_symbol})={mt5.last_error()=}")
        return result

    def _mt5_symbol_show__check(self, _symbol: Type__SymbolOpt = None) -> bool:
        _symbol = self.SYMBOL__get_active(_symbol)
        if _symbol:
            return _symbol.select

    # INFO ------------------------------------------------------------------------------------------------------------
    def _symbols_info__print_compare(self, symbols: List[Type__Symbol] = ["SBER", "AAPL-RM", "PYPL-RM"]):
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
        key = "INSTRUMENTS"
        print(f"{key:30}={symbols}")
        print("*"*100)
        for key in items[0]:
            value = []
            for item in items:
                value.append(item.get(key))
            print(f"{key:30}={value}")

        print("*"*100)

    # VOLUME_PRICE -----------------------------------------------------
    def _symbol_volume_price_get__last_day_finished(self, _symbol: Type__SymbolOpt = None, _devider: Optional[int] = None) -> float:
        """
        VolumePrice as priceMean * Volume
        +save result into self.symbols_volume_price for threading usage!

        value will be differ from official becouse of i get mean price!
        https://www.moex.com/ru/marketdata/?g=4#/mode=groups&group=4&collection=3&boardgroup=57&data_type=current&category=main

        :param _symbol:
        :return:
        """
        _devider = _devider or 1000 * 1000
        bar = self.bars_get__count(_symbol=_symbol, _tf=mt5.TIMEFRAME_D1)
        # print(f"{bar['real_volume']=}")

        item = mt5.symbol_info(_symbol)
        contracts_per_lot = item.trade_contract_size
        contracts = contracts_per_lot * bar["real_volume"]
        volume_price = contracts * (bar["high"] + bar["low"])/2
        # print(f"{volume_price=}")

        result = round(volume_price[0]/_devider)
        self._symbols_volume_price.update({_symbol: result})
        return result

    def _symbols_get_sorted_volume_price(self, limit_min=None, limit_max=None, _symbols: Optional[List[str]] = None, _devider: Optional[int] = None) -> Dict[str, float]:
        """

        (400 * 1000 * 1000)
        ['SBER', 'GAZP', 'LKOH', 'PLZL', 'MGNT', 'NVTK', 'UWGN', 'LQDT', 'VTBR', 'GMKN', 'LSNG', 'SNGS', 'ROSN', 'CHMF']

        :param limit_min:
        :param limit_max:
        :return:
        """
        _devider = _devider or 1000 * 1000
        limit_min = limit_min if limit_min is not None else 100 * 1000 * 1000 / _devider
        _symbols = _symbols or Symbols.SYMBOLS__RUS_FINAM

        # LOAD ---------------------------------------------------
        for symbol in _symbols:
            threading.Thread(target=self._symbol_volume_price_get__last_day_finished, kwargs={"_symbol": symbol, "_devider": _devider}).start()

        while threading.active_count() > 1:
            time.sleep(1)

        # FILTER ---------------------------------------------------
        for symbol, value in dict(self._symbols_volume_price).items():
            if limit_max and limit_max < value:
                self._symbols_volume_price.pop(symbol)
            if limit_min > value:
                self._symbols_volume_price.pop(symbol)

        # SORT -----------------------------------------------------
        self._symbols_volume_price = dict(sorted(self._symbols_volume_price.items(), key=lambda x: x[1], reverse=True))

        # PRINT ----------------------------------------------------
        result_pretty = json.dumps(self._symbols_volume_price, indent=4)
        print(result_pretty)
        return self._symbols_volume_price

    # BAR HISTORY =====================================================================================================
    pass

    # BAR -------------------------------------------------------------------------------------------------------------
    def bar_new__wait(self, sleep: int = 10) -> None:
        # TODO: use BarTime to resolve LOST!!!
        counter = 0
        while not self.bar_last__update():
            counter += 1
            self.bar__lost = True
            msg = f"[WARN]bar lost [{counter=}]"
            print(msg)
            time.sleep(sleep)
        self.bar__lost = False

    def bar_last__update(self) -> Optional[True]:
        bar_new = self.bars_get__count(count=1)
        if not self.BAR_LAST or bar_new != self.BAR_LAST:
            self.BAR_LAST = bar_new
            return True

    def tick_last__update(self, _symbol: Type__SymbolOpt = None, wait_tick_load: bool = True) -> bool:
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
            _symbol: Type__SymbolOpt = None,
            _tf: Type__TfOpt = None
    ) -> bool:
        _symbol = self.SYMBOL__get_active(_symbol)
        _tf_td = dt.timedelta(minutes=self.TF__get_active(_tf))

        result = False
        last = self.TICK_LAST
        if last:
            last_dt = dt.datetime.fromtimestamp(last.time)
            result = (last_dt + _tf_td) >= dt.datetime.today()
        return result

    def bars_get__count(
            self,
            count: int = 1,
            tf_split: Optional[int] = None,
            shrink: Optional[bool] = None,
            _start: Optional[int] = None,
            _symbol: Type__SymbolOpt = None,
            _tf: Type__TfOpt = None
    ) -> Union[np.ndarray]:
        """get history bars

        :param count: get exact count of bars
        :param tf_split: correct count of bars in case of using split tf
        :param shrink: True - if you need in results full correct split bars (for ADX you need new close/open)
            Otherwise, dont use it! for RSI you need only close, which will be accessed directly by steps

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
        """
        _symbol = self.SYMBOL__get_active(_symbol)
        _tf = self.TF__get_active(_tf)
        tf_split = tf_split or 1
        _start = _start or 1

        bars = mt5.copy_rates_from_pos(_symbol.name, _tf, _start, count * tf_split)
        # if not bars:
        #     print(f"{_symbol=}/{bars=}")
        #     return

        # for bar in bars:
        #     print(f"{type(bar)}={bar}")     # <class 'numpy.void'>=(1671753600, 137.49, 138.26, 136.81, 137.94, 53823, 0, 2283422)

        if tf_split > 1 and shrink:
            bars = HistoryShifted_Shrink(bars, tf_split).shrink()

        # if count == 1:
        #     # bars = [(1695729000, 92.3, 92.42, 92.22, 92.23, 944, 1, 3381)]
        #     return bars[0]  # numpy.void
        # else:
        #     # bars = [(1695728400, 92.16, 92.32, 92.1, 92.31, 578, 1, 2764)
        #     #         (1695729000, 92.3, 92.42, 92.22, 92.23, 944, 1, 3381)]
        #     return bars     # numpy.ndarray

        return bars

    # INDICATOR =======================================================================================================
    def _indicator_get_by_obj(
            self,
            indicator_params: IndicatorParamsBase,
            *,
            return_tail: Optional[int] = 1,
            tf_split: Optional[int] = None,

            _bars: Optional[np.ndarray] = None,
            _add_history: Optional[int] = None,
            _tf: Type__TfOpt = None,
            _symbol: Type__SymbolOpt = None,
    ) -> Type__IndicatorValues:
        # GET -----------------------------
        bars_np = _bars or self.bars_get__count(
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

    def indicator_WMA(self, args: Collection[int], **kwargs) -> Type__IndicatorValues:
        return self._indicator_get_by_obj(IndicatorParams_WMA(*args), **kwargs)

    def indicator_STOCH(self, args: Collection[int], **kwargs) -> Type__IndicatorValues:
        return self._indicator_get_by_obj(IndicatorParams_STOCH(*args), **kwargs)

    def indicator_ADX(self, args: Collection[int], **kwargs) -> Type__IndicatorValues:
        return self._indicator_get_by_obj(IndicatorParams_ADX(*args), **kwargs)

    def indicator_MACD(self, args: Collection[int], **kwargs) -> Type__IndicatorValues:
        return self._indicator_get_by_obj(IndicatorParams_MACD(*args), **kwargs)


# =====================================================================================================================
