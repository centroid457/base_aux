from typing import *

import pandas as pd
import numpy as np


# =====================================================================================================================
TYPING__NP_TS__LINE = tuple[int,   float, float, float, float,   int, int, int]

TYPING__NP__FINAL = np.ndarray
TYPING__NP__DRAFT = np.ndarray | list[TYPING__NP_TS__LINE]

TYPING__NP_TS__FINAL = TYPING__NP__FINAL
TYPING__NP_TS__DRAFT = TYPING__NP__DRAFT

TYPING__PD_SERIES = pd.core.series.Series       # NOTE: dont use [pd.Series] it is not actually TYpe!=<class 'pandas.core.series.Series'>
TYPING__PD_DATAFRAME = pd.core.frame.DataFrame  # NOTE: dont use [pd.DataFrame] it is not actually TYpe!=<class 'pandas.core.frame.DataFrame'>


# =====================================================================================================================
