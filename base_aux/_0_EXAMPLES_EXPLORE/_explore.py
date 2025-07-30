import pandas as pd
from base_aux.base_types.m2_info import ObjectInfo


series_a = pd.Series([1, 2, 3])
print(type(series_a))   # <class 'pandas.core.series.Series'>
ObjectInfo(series_a).print()

# print(series_a)
"""
a    NaN
b    6.0
c    8.0
d    NaN
dtype: float64
"""
