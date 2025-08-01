from typing import *
from base_aux.base_lambdas.m1_lambda import *

from base_aux.aux_np_pd.m0_typing import *
import numpy as np
from numpy import dtype

from base_aux.aux_np_pd.m1_np import *
from base_aux.base_types.m0_static_typing import *
from base_aux.base_types.m2_info import *


# =====================================================================================================================
class TS_EXAMPLE:
    """
    GOAL
    ----
    just a set of all example variants
    """
    ZERO_LINE: TYPING__NP_TS__LINE = (0, .0,.0,.0,.0, 0,0,0)

    ZERO_LIST: TYPING__NP_TS__DRAFT = [
        ZERO_LINE,
    ]
    LOAD_LIST_1: TYPING__NP_TS__DRAFT = [
        (1741993200, 70.54, 70.54, 70.49, 70.51, 163, 1, 254),
        (1741993800, 70.52, 70.55, 70.52, 70.54,  56, 1,  82),
        (1741994400, 70.54, 70.56, 70.52, 70.55, 176, 1, 201),
        (1741995000, 70.54, 70.56, 70.54, 70.56, 137, 1, 162),
        (1741995600, 70.56, 70.57, 70.5 , 70.51, 146, 1, 172),

        (1741996200, 70.51, 70.59, 70.51, 70.59, 222, 1, 361),
        (1741996800, 70.6 , 70.61, 70.58, 70.61,  16, 1,  35),
        (1741998000, 70.59, 70.59, 70.59, 70.59,   4, 3,   4),
        (1741998600, 70.61, 70.62, 70.61, 70.62,   7, 3,   7),
        (1741999200, 70.62, 70.62, 70.62, 70.62,  10, 3,  10),
    ]
    LOAD_LIST_2: TYPING__NP_TS__DRAFT = [
        (1741993200, 10.0, 10.9, 10.0, 10.0, 163, 1, 100),
        (1741993200, 10.1, 10.9, 10.0, 10.0, 163, 1, 101),
        (1741993200, 10.2, 10.9, 10.0, 10.0, 163, 1, 102),
        (1741993200, 10.3, 10.9, 10.0, 10.0, 163, 1, 103),
        (1741993200, 10.4, 10.9, 10.0, 10.0, 163, 1, 104),

        (1741993200, 10.5, 10.9, 10.0, 10.0, 163, 1, 105),
        (1741993200, 10.6, 10.9, 10.0, 10.0, 163, 1, 106),
        (1741993200, 10.7, 10.9, 10.0, 10.0, 163, 1, 107),
        (1741993200, 10.8, 10.9, 10.0, 10.0, 163, 1, 108),
        (1741993200, 10.9, 10.9, 10.0, 10.0, 163, 1, 109),
    ]


# =====================================================================================================================
class NpTimeSeriesAux(NdArray2dAux):
    """
    TODO: seems exists DfTsAux ???? )))) decide what to do with it!

    GOAL
    ----
    EXACT methods expecting ndarray as timeSeries
    """
    SOURCE: TYPING__NP_TS__FINAL = TS_EXAMPLE.ZERO_LIST

    DEF__DTYPE_DICT: dict[str, str | dtype] = dict(       # template for making dtype with correct expected elements
        # dtype from mt5
        time='<i8',
        open='<f8',
        high='<f8',
        low='<f8',
        close='<f8',
        tick_volume='<u8',  # count ticks withing one bar!
        spread='<i4',       # WHAT IT IS???
        real_volume='<u8',
    )

    @classmethod
    def _window_shrink(cls, window: np.ndarray) -> np.void | np.ndarray:   # NOTE: np.void - is acually! np.ndarray - just for IDE typeChecking!
        # get any item as template
        void_new = window[0].copy()

        # recalculate all values
        void_new["time"] = window["time"].max()
        void_new["open"] = window["open"][-1]
        void_new["high"] = window["high"].max()
        void_new["low"] = window["low"].min()
        void_new["close"] = window["close"][0]
        void_new["tick_volume"] = window["tick_volume"].sum()
        void_new["spread"] = void_new["high"].max() - void_new["low"].min()     # may be incorrect ???
        void_new["real_volume"] = window["real_volume"].sum()

        return void_new


# =====================================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================


def _explore_init():
    obj = NpTimeSeriesAux()
    print(obj.get_fields())
    print(obj.get_fields()["time"])
    print(obj.get_fields()["time"][1])
    print(type(obj.SOURCE.dtype.fields["time"][1]))

    obj = NpTimeSeriesAux(TS_EXAMPLE.LOAD_LIST_1)
    ObjectInfo(obj.SOURCE).print()

    exit()
    print(obj.get_fields()["time"][1])


    exit()
    obj = NpTimeSeriesAux(TS_EXAMPLE.LOAD_LIST_1)
    # print(obj.SOURCE)
    # ObjectInfo(obj.SOURCE).print()

    print(obj.get_fields())

    assert obj.SOURCE.ndim == 1

    print(obj.SOURCE["close"])
    assert obj.SOURCE["close"] is not None
    assert obj.SOURCE["close"].ndim == 1

    try:
        obj = NpTimeSeriesAux(TS_EXAMPLE.LOAD_LIST_1[0])
        assert False
        print(obj.SOURCE)
    except:
        pass


def _explore_split():
    obj = NpTimeSeriesAux(TS_EXAMPLE.LOAD_LIST_1)
    print(obj.SOURCE.shape)
    assert obj.SOURCE.size == len(TS_EXAMPLE.LOAD_LIST_1)


    # ObjectInfo(obj.SOURCE).print()

    # obj2 = np.split(obj.SOURCE, 2)
    # ObjectInfo(obj2).print()


# =====================================================================================================================
if __name__ == "__main__":
    _explore_init()


# =====================================================================================================================
