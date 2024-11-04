from typing import *
import pytest

from trade_alerts import *


# =====================================================================================================================
class Test_mt5:
    VICTIM: Union[MT5, MT5] = type("VICTIM", (MT5,), {})

    # @classmethod
    # def setup_class(cls):
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     # self.VICTIM = type("VICTIM", (888888888888,), {})

    # CONNECT ---------------------------------------------------------------------------------------------------------
    def test__mt5_connect(self):
        # DOUBLE CONNECT
        victim1 = self.VICTIM()
        result = mt5.last_error()
        assert result == (1, 'Success')
        assert result[0] == 1
        assert result[1] == "Success"

        victim2 = self.VICTIM()
        result = mt5.last_error()
        assert result == (1, 'Success')

        self.VICTIM.SYMBOL = "Нефть Brent"
        victim = self.VICTIM()
        assert isinstance(victim.SYMBOL, mt5.SymbolInfo)

        self.VICTIM.SYMBOL = "Нефть Brent 1234"
        try:
            victim = self.VICTIM()
        except Exception as exx:
            assert isinstance(exx, Exx_Mt5SymbolName)
        else:
            assert False

    # SORTED ---------------------------------------------------------------------------------------------------------
    def test__symbol_volume_price_get__last_day_finished(self):
        victim = self.VICTIM()
        result = victim._symbol_volume_price_get__last_day_finished(_symbol="SBER")
        print(result)

    def test__symbols_get_sorted_volume_price(self):
        victim = self.VICTIM()
        victim._symbols_get_sorted_volume_price()

    # HISTORY ---------------------------------------------------------------------------------------------------------
    def test__bars_np(self):
        victim = MT5()

        bars1 = victim.bars_get__count()
        print(bars1)            # [(1695763200, 93.89, 93.91, 93.75, 93.84, 527, 1, 2116)]
        assert bars1.shape == (1, )
        assert isinstance(bars1, np.ndarray)
        assert isinstance(bars1[0], np.void)

        print()
        print()
        print()
        print(f"{bars1[0]=}")       # (1695844800, 96.69, 96.73, 96.53, 96.56, 452, 1, 1542)
        print(f"{type(bars1[0])=}")     #<class 'numpy.void'>
        print(f"{bars1[0]['time']=}")   #1695845400
        # print(f"{bars1[0].time=}")      #AttributeError: 'numpy.void' object has no attribute 'time'
        print()
        print()
        print()

        print(bars1.dtype.fields)
        assert list(bars1.dtype.fields) == ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']

        for elem in bars1[0]:
            print(f"{elem=}/{type(elem)}")
            """
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
            assert isinstance(elem, (np.int64, np.float64, np.uint64, np.intc, ))

        bars2 = victim.bars_get__count(2)
        print(bars2)
        assert bars2.shape == (2, )
        assert isinstance(bars2, np.ndarray)
        assert isinstance(bars2[0], np.void)

    def test__steps(self):
        victim = MT5()
        assert victim.bars_get__count(1, tf_split=1).shape == (1,)
        assert victim.bars_get__count(1, tf_split=2).shape == (1,)
        assert victim.bars_get__count(1, tf_split=3).shape == (1,)

        assert victim.bars_get__count(2, tf_split=1).shape == (2,)
        assert victim.bars_get__count(2, tf_split=2).shape == (2,)
        assert victim.bars_get__count(2, tf_split=3).shape == (2,)

    # INDICATORS ------------------------------------------------------------------------------------------------------
    def test__indicator_get__TYPE(self):
        victim = MT5()
        result = victim._indicator_get_by_obj(IndicatorParams_ADX(2, 1), return_tail=1)
        print(f"[{result=}]")
        print(f"[{type(result)=}]")
        assert isinstance(result, (int, float))

        result = victim._indicator_get_by_obj(IndicatorParams_ADX(2, 1), return_tail=2)
        print(f"[{result=}]")
        print(f"[{type(result)=}]")
        assert isinstance(result, (Type_PdSeries))

    def test__indicator_get__WMA(self):
        victim = MT5()
        results = set()
        for params in [(1, ), (10, ), (20, ), ]:
            print(f"[{params=}]")
            result = victim._indicator_get_by_obj(IndicatorParams_WMA(*params))
            print(f"[    {result=}]")
            assert isinstance(result, (int, float))
            results.add(result)
        assert len(results) > 1

        for params in [(1, ), ]:
            assert victim.indicator_WMA(params) == victim._indicator_get_by_obj(IndicatorParams_WMA(*params))

    @pytest.mark.xfail
    def test__indicator_get__STOCH(self):
        """
        it will fail because of stoch func not working correctly! always on 14/3/3!!!
        """
        victim = MT5()
        results = set()
        for params in [(14, 3, 3), (5, 1, 1), ]:
            print(f"[{params=}]")
            result = victim._indicator_get_by_obj(IndicatorParams_STOCH(*params))
            print(f"[    {result=}]")
            assert isinstance(result, (int, float))
            results.add(result)
        assert len(results) > 1

        for params in [(14, 3, 3), ]:
            assert victim.indicator_STOCH(params) == victim._indicator_get_by_obj(IndicatorParams_STOCH(*params))

    def test__indicator_get__ADX(self):
        victim = MT5()
        results = set()
        for params in [(10, 5), (5, 1), ]:
            print(f"[{params=}]")
            result = victim._indicator_get_by_obj(IndicatorParams_ADX(*params))
            print(f"[    {result=}]")
            assert isinstance(result, (int, float))
            results.add(result)
        assert len(results) > 1

        for params in [(5, 1, ), ]:
            assert victim.indicator_ADX(params) == victim._indicator_get_by_obj(IndicatorParams_ADX(*params))

    def test__indicator_get__MACD(self):
        victim = MT5()
        results = set()
        for params in [(20, 10, 20), (10, 1, 10), ]:
            print(f"[{params=}]")
            result = victim._indicator_get_by_obj(IndicatorParams_MACD(*params))
            print(f"[    {result=}]")
            assert isinstance(result, (int, float))
            results.add(result)
        assert len(results) > 1


# =====================================================================================================================
class Test_strategy:
    VICTIM: Union[MT5, MT5] = type("VICTIM", (MT5,), {})

    def test__ADX(self):
        victim = MonitorADX()
        victim.join()


# =====================================================================================================================
