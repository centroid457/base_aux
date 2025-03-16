from typing import *
import numpy as np
import pandas as pd

from base_aux.base_statics.m2_exceptions import *
from base_aux.base_nest_dunders.m1_init1_source import *


# =====================================================================================================================
class TimeSeriesAux(NestInit_Source):
    SOURCE: np.array

    # FIELDS ----------------------------------------------------------------------------------------------------------
    def get_fields(self) -> dict[str, Any]:
        """
        GOAL
        ----
        just as help info!

        results
        -------
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

    def shrink_simple(self, divider: int, column: Optional[str] = None) -> np.array:
        """
        DIFFERENCE - from shrink
        ----------
        just drop other data! without calculations

        when important only one column in calculations!
        such as RSI/WMA typically use only close values from timeSeries!
        """
        pass

    # ------------------------------------------------------------------------------------------------------
    def _windows_get(self, divider: int) -> np.array:
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

    def _window_shrink(self, window: np.array) -> np.void:
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
