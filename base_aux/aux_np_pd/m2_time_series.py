from base_aux.aux_np_pd.m0_typing import *
import numpy as np
from numpy import dtype

from base_aux.aux_np_pd.m1_np import *
from base_aux.base_types.m0_static_typing import *
from base_aux.base_types.m2_info import *


# =====================================================================================================================
TS_EXAMPLE__ZERO_LINE: TYPING__NP_TS__LINE = (0, .0,.0,.0,.0, 0,0,0)

TS_EXAMPLE__ZERO_SET: TYPING__NP_TS__DRAFT = [
    TS_EXAMPLE__ZERO_LINE,
]

TS_EXAMPLE__LOAD_LIST: TYPING__NP_TS__DRAFT = [
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


# =====================================================================================================================
class NpTimeSeriesAux(NdArrayAux):
    """
    TODO: seems exists DfTsAux ???? )))) decide what to do with it!

    GOAL
    ----
    EXACT methods expecting ndarray as timeSeries
    """
    SOURCE: TYPING__NP_TS__FINAL = TS_EXAMPLE__ZERO_SET

    DEF__DTYPE_DICT: dict[str, str | dtype] = dict(       # template for making dtype
        time='<i8',
        open='<f8',
        high='<f8',
        low='<f8',
        close='<f8',
        tick_volume='<u8',
        spread='<i4',
        real_volume='<u8',
    )


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
    ObjectInfo(obj.SOURCE.dtype.fields["time"][1]).print()

    exit()
    print(obj.get_fields()["time"][1])


    exit()
    obj = NpTimeSeriesAux(TS_EXAMPLE__LOAD_LIST)
    # print(obj.SOURCE)
    # ObjectInfo(obj.SOURCE).print()

    print(obj.get_fields())

    assert obj.SOURCE.ndim == 1

    print(obj.SOURCE["close"])
    assert obj.SOURCE["close"] is not None
    assert obj.SOURCE["close"].ndim == 1

    try:
        obj = NpTimeSeriesAux(TS_EXAMPLE__LOAD_LIST[0])
        assert False
        print(obj.SOURCE)
    except:
        pass


def _explore_split():
    obj = NpTimeSeriesAux(TS_EXAMPLE__LOAD_LIST)
    print(obj.SOURCE.shape)
    assert obj.SOURCE.size == len(TS_EXAMPLE__LOAD_LIST)


    # ObjectInfo(obj.SOURCE).print()

    # obj2 = np.split(obj.SOURCE, 2)
    # ObjectInfo(obj2).print()


# =====================================================================================================================
if __name__ == "__main__":
    _explore_init()


# =====================================================================================================================
