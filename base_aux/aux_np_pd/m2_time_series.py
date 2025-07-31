import numpy as np

from base_aux.aux_np_pd.m0_typing import *
from numpy import dtype

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_types.m0_static_typing import *
from base_aux.base_values.m3_exceptions import *
from base_aux.base_types.m2_info import *


# =====================================================================================================================
TS_EXAMPLE_LIST = [
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
class TimeSeriesAux(NestInit_Source):
    """
    GOAL
    ----
    EXACT methods expecting ndarray as timeSeries
    """
    SOURCE: TYPING__NP_TS__FINAL = [0, .0,.0,.0,.0, 0,0,0]

    DTYPE_DICT: dict[str, str | type] = dict(       # template for making dtype
        time='<i8',
        open='<f8',
        high='<f8',
        low='<f8',
        close='<f8',
        tick_volume='<u8',
        spread='<i4',
        real_volume='<u8',
    )
    DTYPE_ITEMS: list[tuple[str, str | type]] = list(DTYPE_DICT.items())  # used to create data on Air

    # -----------------------------------------------------------------------------------------------------------------
    def init_post(self) -> None | NoReturn:
        if isinstance(self.SOURCE, (list, tuple)):
            self.SOURCE = np.array(self.SOURCE, dtype=self.DTYPE_ITEMS)
        # TODO: make copy

    # -----------------------------------------------------------------------------------------------------------------
    def get_fields(self) -> dict[str, tuple[dtype, int]]:
        """
        GOAL
        ----
        just as help info!

        results
        -------
        DTYPE
            [('time', '<i8'), ('open', '<f8'), ('high', '<f8'), ('low', '<f8'), ('close', '<f8'), ('tick_volume', '<u8'), ('spread', '<i4'), ('real_volume', '<u8')]
            [
                ('time', '<i8'),
                ('open', '<f8'),
                ('high', '<f8'),
                ('low', '<f8'),
                ('close', '<f8'),
                ('tick_volume', '<u8'),
                ('spread', '<i4'),
                ('real_volume', '<u8')
            ]

        FIELDS
            ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']

            {
                'time': (dtype('int64'), 0),
                'open': (dtype('float64'), 8),
                'high': (dtype('float64'), 16),
                'low': (dtype('float64'), 24),
                'close': (dtype('float64'), 32),
                'tick_volume': (dtype('uint64'), 40),
                'spread': (dtype('int32'), 48),
                'real_volume': (dtype('uint64'), 52)
            }
        """
        return self.SOURCE.dtype.fields

    # -----------------------------------------------------------------------------------------------------------------
    def split_groups(self, group_len: int) -> TYPING__NP_TS__FINAL:
        """
        GOAL
        ----
        split array to arrays with exact elements count
        NOT INLINE! and dont do it!
        """
        # if self.SOURCE.ndim != 1:
        #     raise Exx__Incompatible
        new_shape = []
        shape = self.SOURCE.shape
        a = np.arange(5)
        print(a)
        print(np.array_split(a, 2))
        print(a)
        # TODO: FINISH!





    # SHRINK ----------------------------------------------------------------------------------------------------------
    def shrink(self, divider: int) -> np.array:
        """
        GOAL
        ----
        full remake TS to less TF then actual
        for example - you have 100history lines from tf=1m
        so you can get
            50lines for tf=2m
            10lines for tf=10m
        and it will be actual TS for TF! you dont need wait for finishing exact TF
        """
        if divider == 1:
            return self.SOURCE
        elif divider < 1:
            raise Exx__WrongUsage(f"{divider=}")

        windows = self._windows_get(divider)
        result = self._windows_shrink(windows)
        return result

    def shrink_simple(self, divider: int, column: str = None) -> np.array:
        """
        DIFFERENCE - from shrink
        ----------
        just drop other data! without calculations

        when important only one column in calculations!
        such as RSI/WMA typically use only close values from timeSeries!
        """
        result = self.SOURCE
        if column:
            result = result[column]
        result = result[::divider]
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def _windows_get(self, divider: int) -> np.ndarray:
        bars_windows = np.lib.stride_tricks.sliding_window_view(x=self.SOURCE, window_shape=divider)
        bars_windows_stepped = bars_windows[::divider]
        return bars_windows_stepped

    def _windows_shrink(self, windows: np.array) -> np.array:
        result: Optional[np.array] = None
        for window in windows:
            void_new = self._window_shrink(window)
            try:
                result = np.concatenate([result, [void_new]])
            except Exception as exx:
                # if no elements
                # print(f"{exx!r}")
                result = np.array([void_new])
        return result

    def _window_shrink(self, window: np.ndarray) -> np.void | np.ndarray:   # np.void - is acually! np.ndarray - just for IDE typeChecking!
        void_new = window[0].copy()

        void_new["time"] = window["time"].max()
        void_new["open"] = window["open"][-1]
        void_new["high"] = window["high"].max()
        void_new["low"] = window["low"].min()
        void_new["close"] = window["close"][0]
        void_new["tick_volume"] = window["tick_volume"].sum()    # may be incorrect
        void_new["spread"] = void_new["high"] - void_new["low"]    # may be incorrect
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
    obj = TimeSeriesAux()
    print(obj.get_fields())
    print(obj.get_fields()["time"])
    print(obj.get_fields()["time"][1])
    print(type(obj.SOURCE.dtype.fields["time"][1]))
    ObjectInfo(obj.SOURCE.dtype.fields["time"][1]).print()

    exit()
    print(obj.get_fields()["time"][1])


    exit()
    obj = TimeSeriesAux(TS_EXAMPLE_LIST)
    # print(obj.SOURCE)
    # ObjectInfo(obj.SOURCE).print()

    print(obj.get_fields())

    assert obj.SOURCE.ndim == 1

    print(obj.SOURCE["close"])
    assert obj.SOURCE["close"] is not None
    assert obj.SOURCE["close"].ndim == 1

    try:
        obj = TimeSeriesAux(TS_EXAMPLE_LIST[0])
        assert False
        print(obj.SOURCE)
    except:
        pass


def _explore_split():
    obj = TimeSeriesAux(TS_EXAMPLE_LIST)
    print(obj.SOURCE.shape)
    assert obj.SOURCE.size == len(TS_EXAMPLE_LIST)


    # ObjectInfo(obj.SOURCE).print()

    # obj2 = np.split(obj.SOURCE, 2)
    # ObjectInfo(obj2).print()


# =====================================================================================================================
if __name__ == "__main__":
    _explore_init()


# =====================================================================================================================
