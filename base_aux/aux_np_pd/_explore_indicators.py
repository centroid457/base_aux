from datetime import datetime
import MetaTrader5 as mt5
import pytz
import pandas as pd


BARS_COUNT = 154

pd.set_option('display.max_columns', 500)  # сколько столбцов показываем
pd.set_option('display.width', 1500)  # макс. ширина таблицы для показа

if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

rates = mt5.copy_rates_from_pos("SBER", mt5.TIMEFRAME_M10, 0, BARS_COUNT)
mt5.shutdown()

if rates is None:
    print("[FAIL] seems symbol is very old and not accessible! no rates [like for BRV3 -> None, use SBER]")

print("rates as is:")
for rate in rates:
    print(rate)
    # (1675118400, 85.41, 85.43, 85.21, 85.21, 225, 1, 1065)

print(rates)

print(rates[0]["time"])
# exit()







rates_frame = pd.DataFrame(rates)
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
print("\nВыведем датафрейм с данными")
print(rates_frame)
mt5.shutdown()
print()
print()
print()
print()
print()
print(f"*"*100)


# =====================================================================================================================
import pandas_ta as ta  # VERY IMPORTANT!!! even if no used

df = rates_frame


# =====================================================================================================================
def ADX():
    # def adx(self, length=None, lensig=None, mamode=None, scalar=None, drift=None, offset=None, **kwargs):
    indicator = df.ta.adx(length=6, lensig=2)
    print(indicator)
    print(indicator.tail(1))
    """
            ADX_2      DMP_6      DMN_6
    0         NaN        NaN        NaN
    1         NaN        NaN        NaN
    2         NaN        NaN        NaN
    3         NaN        NaN        NaN
    4         NaN        NaN        NaN
    5         NaN        NaN        NaN
    6         NaN  14.183095  41.716404
    7   58.108655   9.765756  42.367588
    8   59.128053   8.595080  34.265241
    9   30.111366  23.026151  25.308395
    10  21.774266  17.365562  22.999863
    11  21.766877  14.751132  22.956125
    12  12.255897  20.654078  19.492429
    13   7.556354  18.303381  17.273941
    14  18.484665  25.888921  14.134057
    15  35.570215  35.400260  10.989079
    16  45.410875  33.062720   9.532371
    17  50.327601  29.766578   8.582055
    18  55.172890  30.519074   7.625717
    19  57.595091  29.625643   7.402477
    
            ADX_2      DMP_6     DMN_6
    19  57.595091  29.625643  7.402477
    57.59509093254269
    """
    print()
    print()
    print(df.ta.adx(length=2, lensig=1).iloc[BARS_COUNT-1]["ADX_1"])   # 57.59509093254269
    print(df.ta.adx(length=6, lensig=2).iloc[BARS_COUNT-1]["ADX_2"])   # 57.59509093254269
    print(df.ta.adx(length=10, lensig=7).iloc[BARS_COUNT-1]["ADX_7"])   # 57.59509093254269
    print(df.ta.adx(length=14, lensig=14).iloc[BARS_COUNT-1]["ADX_14"])   # 57.59509093254269


# =====================================================================================================================
def MACD():
    # def macd(self, fast=None, slow=None, signal=None, offset=None, **kwargs):
    # indicator = df.ta.macd(fast=12, slow=26, signal=9)
    # print(indicator)
    # print(indicator.tail(1))
    """
    ИЗ 50 дает только 16!!!!!
    
    
        MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9
0            NaN            NaN            NaN
1            NaN            NaN            NaN
2            NaN            NaN            NaN
3            NaN            NaN            NaN
4            NaN            NaN            NaN
5            NaN            NaN            NaN
6            NaN            NaN            NaN
7            NaN            NaN            NaN
8            NaN            NaN            NaN
9            NaN            NaN            NaN
10           NaN            NaN            NaN
11           NaN            NaN            NaN
12           NaN            NaN            NaN
13           NaN            NaN            NaN
14           NaN            NaN            NaN
15           NaN            NaN            NaN
16           NaN            NaN            NaN
17           NaN            NaN            NaN
18           NaN            NaN            NaN
19           NaN            NaN            NaN
20           NaN            NaN            NaN
21           NaN            NaN            NaN
22           NaN            NaN            NaN
23           NaN            NaN            NaN
24           NaN            NaN            NaN
25           NaN            NaN            NaN
26           NaN            NaN            NaN
27           NaN            NaN            NaN
28           NaN            NaN            NaN
29           NaN            NaN            NaN
30           NaN            NaN            NaN
31           NaN            NaN            NaN
32           NaN            NaN            NaN
33     -0.538086      -0.035338      -0.502749
34     -0.517037      -0.011431      -0.505606
35     -0.504226       0.001104      -0.505330
36     -0.486847       0.014786      -0.501634
37     -0.470077       0.025246      -0.495322
38     -0.447592       0.038185      -0.485776
39     -0.420088       0.052551      -0.472638
40     -0.404920       0.054175      -0.459095
41     -0.371670       0.069940      -0.441610
42     -0.352552       0.071246      -0.423798
43     -0.338342       0.068365      -0.406707
44     -0.326544       0.064130      -0.390675
45     -0.315973       0.059762      -0.375734
46     -0.298505       0.061783      -0.360288
47     -0.283013       0.061820      -0.344833
48     -0.267651       0.061746      -0.329397
49     -0.261339       0.054446      -0.315785
    MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9
49     -0.261339       0.054446      -0.315785
    """
    # indicator = df.ta.macd(fast=10, slow=10, signal=10)
    # print(indicator)
    """
        MACD_10_10_10  MACDh_10_10_10  MACDs_10_10_10
0             NaN             NaN             NaN
1             NaN             NaN             NaN
2             NaN             NaN             NaN
3             NaN             NaN             NaN
4             NaN             NaN             NaN
5             NaN             NaN             NaN
6             NaN             NaN             NaN
7             NaN             NaN             NaN
8             NaN             NaN             NaN
9             NaN             NaN             NaN
10            NaN             NaN             NaN
11            NaN             NaN             NaN
12            NaN             NaN             NaN
13            NaN             NaN             NaN
14            NaN             NaN             NaN
15            NaN             NaN             NaN
16            NaN             NaN             NaN
17            NaN             NaN             NaN
18            0.0             0.0             0.0
19            0.0             0.0             0.0
20            0.0             0.0             0.0
21            0.0             0.0             0.0
22            0.0             0.0             0.0
23            0.0             0.0             0.0
24            0.0             0.0             0.0
25            0.0             0.0             0.0
26            0.0             0.0             0.0
27            0.0             0.0             0.0
28            0.0             0.0             0.0
29            0.0             0.0             0.0
30            0.0             0.0             0.0
31            0.0             0.0             0.0
32            0.0             0.0             0.0
33            0.0             0.0             0.0
34            0.0             0.0             0.0
35            0.0             0.0             0.0
36            0.0             0.0             0.0
37            0.0             0.0             0.0
38            0.0             0.0             0.0
39            0.0             0.0             0.0
40            0.0             0.0             0.0
41            0.0             0.0             0.0
42            0.0             0.0             0.0
43            0.0             0.0             0.0
44            0.0             0.0             0.0
45            0.0             0.0             0.0
46            0.0             0.0             0.0
47            0.0             0.0             0.0
48            0.0             0.0             0.0
49            0.0             0.0             0.0
    """
    # indicator = df.ta.macd(fast=10, slow=10, signal=1)
    # print(indicator)
    """
         MACD_10_10_1  MACDh_10_10_1  MACDs_10_10_1
0             NaN            NaN            NaN
1             NaN            NaN            NaN
2             NaN            NaN            NaN
3             NaN            NaN            NaN
4             NaN            NaN            NaN
5             NaN            NaN            NaN
6             NaN            NaN            NaN
7             NaN            NaN            NaN
8   5.138404e-270  5.138404e-270            0.0
9    0.000000e+00   0.000000e+00            0.0
10   0.000000e+00   0.000000e+00            0.0
11   0.000000e+00   0.000000e+00            0.0
12   0.000000e+00   0.000000e+00            0.0
13   0.000000e+00   0.000000e+00            0.0
14   0.000000e+00   0.000000e+00            0.0
15   0.000000e+00   0.000000e+00            0.0
16   0.000000e+00   0.000000e+00            0.0
17   0.000000e+00   0.000000e+00            0.0
18   0.000000e+00   0.000000e+00            0.0
19   0.000000e+00   0.000000e+00            0.0
20   0.000000e+00   0.000000e+00            0.0
21   0.000000e+00   0.000000e+00            0.0
22   0.000000e+00   0.000000e+00            0.0
23   0.000000e+00   0.000000e+00            0.0
24   0.000000e+00   0.000000e+00            0.0
25   0.000000e+00   0.000000e+00            0.0
26   0.000000e+00   0.000000e+00            0.0
27   0.000000e+00   0.000000e+00            0.0
28   0.000000e+00   0.000000e+00            0.0
29   0.000000e+00   0.000000e+00            0.0
30   0.000000e+00   0.000000e+00            0.0
31   0.000000e+00   0.000000e+00            0.0
32   0.000000e+00   0.000000e+00            0.0
33   0.000000e+00   0.000000e+00            0.0
34   0.000000e+00   0.000000e+00            0.0
35   0.000000e+00   0.000000e+00            0.0
36   0.000000e+00   0.000000e+00            0.0
37   0.000000e+00   0.000000e+00            0.0
38   0.000000e+00   0.000000e+00            0.0
39   0.000000e+00   0.000000e+00            0.0
40   0.000000e+00   0.000000e+00            0.0
41   0.000000e+00   0.000000e+00            0.0
42   0.000000e+00   0.000000e+00            0.0
43   0.000000e+00   0.000000e+00            0.0
44   0.000000e+00   0.000000e+00            0.0
45   0.000000e+00   0.000000e+00            0.0
46   0.000000e+00   0.000000e+00            0.0
47   0.000000e+00   0.000000e+00            0.0
48   0.000000e+00   8.682000e+01            0.0
49   0.000000e+00   8.671000e+01            0.0
    """
    # indicator = df.ta.macd(fast=1, slow=10, signal=10)    # EXCEPTION!!!
    # print(indicator)

    indicator = df.ta.macd(fast=10, slow=77, signal=50)
    print(indicator)

    # print(df.ta.macd(fast=12, slow=26, signal=9).iloc[BARS_COUNT-1]["MACD_12_26_9"])
    # print(df.ta.macd(fast=12, slow=26, signal=9).iloc[BARS_COUNT-1]["MACDh_12_26_9"])
    # print(df.ta.macd(fast=12, slow=26, signal=9).iloc[BARS_COUNT-1]["MACDs_12_26_9"])


# =====================================================================================================================
def STOCH(fast_k=10, slow_k=3, slow_d=3):
    # def adx(self, length=None, lensig=None, mamode=None, scalar=None, drift=None, offset=None, **kwargs):
    indicator = df.ta.stoch(fast_k=fast_k, slow_k=slow_k, slow_d=slow_d)
    # indicator = ta.stoch(high=df["high"], low=df["low"], close=["close"], fast_k=fast_k, slow_k=slow_k, slow_d=slow_d)

    print(indicator)
    print(indicator.tail(1))

    # ИМЯ STOCHk_14_3_3 не зависит от slow_k!!!!!! оно всегда 3!!!
    """
     STOCHk_14_3_3  STOCHd_14_3_3
13             NaN            NaN
14             NaN            NaN
15       63.710262            NaN
16       56.560081            NaN
17       41.180416      53.816920
..             ...            ...
149      83.597884      88.649490
150      86.111111      85.822647
151      90.851852      86.853616
152      94.122655      90.361873
153      76.265512      87.080006

[141 rows x 2 columns]
     STOCHk_14_3_3  STOCHd_14_3_3
153      76.265512      87.080006
    """
    print()
    print()
    print(indicator.iloc[len(indicator) - 1]["STOCHk_14_3_3"])  # 87.08000641334098
    print(indicator.iloc[len(indicator) - 1]["STOCHd_14_3_3"])  # 87.08000641334098
    print(indicator.shape)  # (141, 2)
    print(f"{type(indicator)=}")    #<class 'pandas.core.frame.DataFrame'>


# =====================================================================================================================
def WMA():
    # def wma(self, length=None, offset=None, **kwargs):
    indicator = df.ta.wma(length=20)
    print(f"{indicator=}")
    print(indicator.tail(1))

    #
    """
0            NaN
1            NaN
2            NaN
3            NaN
4            NaN
         ...    
149    83.896952
150    83.897190
151    83.896524
152    83.895857
153    83.896238
Name: WMA_20, Length: 154, dtype: float64
153    83.896238
Name: WMA_20, dtype: float64
    """
    print()
    print()
    print(indicator.iloc[len(indicator) - 1])  # 87.08000641334098
    print(indicator.shape)  # (154,)
    print(f"{type(indicator)=}")    # <class 'pandas.core.series.Series'>

    indicator = pd.DataFrame(indicator)
    print(f"{type(indicator)=}")    # <class 'pandas.core.frame.DataFrame'>
    print(f"{indicator=}")
    """
indicator=
             WMA_20
0           NaN
1           NaN
2           NaN
3           NaN
4           NaN
..          ...
149  305.352762
150  305.245619
151  305.141381
152  305.045810
153  304.954333
    """


# =====================================================================================================================
def RSI():
    # def rsi(self, length=None, scalar=None, drift=None, offset=None, **kwargs):
    # def rsi(close, length=None, scalar=None, talib=None, drift=None, offset=None, **kwargs):

    indicator = df.ta.rsi(length=20)
    print(f"{indicator=}")
    """
indicator=
0            NaN
1            NaN
2            NaN
3            NaN
4            NaN
         ...    
149    42.117879
150    45.292848
151    42.820427
152    42.820427
153    46.081662
Name: RSI_20, Length: 154, dtype: float64
153    46.081662
Name: RSI_20, dtype: float64


46.08166200413547
(154,)
    """
    # print(f"[{indicator.tail(1)=}]")
    """
[indicator.tail(1)=153    36.105644
Name: RSI_20, dtype: float64]
    """
    # indicator = indicator.round(1)
    # print(f"[{indicator.tail(1)=}]")

    print()
    print()
    # print(indicator.iloc[len(indicator) - 1])  # 87.08000641334098
    # print(indicator.shape)  # (154,)
    # print(f"{type(indicator)=}")    # <class 'pandas.core.series.Series'>

    # SET NAME
    # print(f"{indicator.name=}")     # indicator.name='RSI_20'
    # indicator.name = "HELLO"
    # print(f"{indicator=}")
    """
indicator=
0            NaN
1            NaN
2            NaN
3            NaN
4            NaN
         ...    
149    32.657488
150    33.353140
151    36.131115
152    37.902101
153    37.648513
Name: HELLO, Length: 154, dtype: float64
    """
    # indicator = pd.DataFrame(indicator)
    # print(f"{type(indicator)=}")    # <class 'pandas.core.frame.DataFrame'>
    # print(f"{indicator.name=}")     # AttributeError: 'DataFrame' object has no attribute 'name'. Did you mean: 'rename'?
    # indicator["RSI_20"] = indicator["RSI_20"].round(1)
    # print(f"{indicator=}")
    """
indicator=
            RSI_20
0          NaN
1          NaN
2          NaN
3          NaN
4          NaN
..         ...
149  33.353338
150  36.131320
151  37.902311
152  37.315832
153  38.178916
    """
    # indicator = indicator.tail(2)
    # print(f"{indicator=}")

    print(f"{len(rates)=}")
    print(f"{len(indicator)=}")
    # indicator = pd.DataFrame(indicator, index=range(20))
    # print(f"{len(indicator)=}")
    # print(f"{indicator=}")

    indicator = pd.DataFrame(indicator, index=rates["time"])
    print(f"{len(indicator)=}")
    print(f"{indicator=}")


# =====================================================================================================================
# ADX()
# MACD()
# WMA()
# STOCH(10,1,1,)
# STOCH(20,5,5,)
RSI()
