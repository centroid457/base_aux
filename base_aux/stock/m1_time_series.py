from typing import *
import numpy as np
import pandas as pd

from base_aux.base_statics.m2_exceptions import *


# =====================================================================================================================
class HistoryShifted_Shrink:
    """
    GOAL
    ----
    remake TS to shifted TF
    """
    SOURCE: np.array
    SHIFT: int

    def __init__(self, source: np.array, shift: int = 1):
        self.SOURCE = source
        self.SHIFT = shift

        if shift < 1:
            raise Exx__WrongUsage(f"{shift=}")

    # FIELDS ----------------------------------------------------------------------------------------------------------
    def _get_fields(self) -> dict[str, Any]:
        """
        GOAL
        ----
        just as help info!

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
    def shrink(self) -> np.array:
        if self.SHIFT == 1:
            return self.SOURCE
        windows = self._windows_get()
        result = self._windows_shrink(windows)
        return result

    # ------------------------------------------------------------------------------------------------------
    def _windows_get(self) -> np.array:
        bars_windows = np.lib.stride_tricks.sliding_window_view(x=self.SOURCE, window_shape=self.SHIFT)
        bars_windows_stepped = bars_windows[::self.SHIFT]
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
class HistoryShifted_Simple:
    """History manager when important only one column in calculations!
    such as RSI/WMA typically use only close values from timeSeries!
    """
    SOURCE: np.array = None
    COLUMN: str = "close"
    SHIFT: int = None

    def __init__(self, source: np.array, shift: int = 1, column: Optional[str] = None):
        self.SOURCE = source
        self.COLUMN = column
        self.SHIFT = shift

        if shift < 1:
            raise Exx__WrongUsage(f"{shift=}")


# =====================================================================================================================
