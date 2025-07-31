from typing import *
import sys

import numpy as np
from numpy import dtype

from base_aux.base_values.m3_exceptions import *
from base_aux.aux_np_pd.m0_typing import *
from base_aux.base_nest_dunders.m1_init1_source import *


# =====================================================================================================================
# @final    # DONT USE FINAL!!! it used as base!
class NdArrayAux(NestInit_Source):
    SOURCE: TYPING__NP__FINAL

    # -----------------------------------------------------------------------------------------------------------------
    DEF__DTYPE_DICT: dict[str, str | dtype] = dict(  # template for making dtype
        # time='<i8',
        # open='<f8',
        # high='<f8',
        # low='<f8',
        # close='<f8',
        # tick_volume='<u8',
        # spread='<i4',
        # real_volume='<u8',
    )

    @property
    def DEF__DTYPE_ITEMS(self) -> list[tuple[str, str | dtype]]:
        """
        GOAL
        ----
        ref source final from draft if data struct is exact expected! like for TimeSeries!

        SPECIALLY CREATED FOR
        ---------------------
        NpTimeSeriesAux
        """
        return list(self.DEF__DTYPE_DICT.items())

    # -----------------------------------------------------------------------------------------------------------------
    def init_post(self) -> None:
        self.set_printoptions()
        self.unsure__ndarray_dtype()

    @classmethod
    def set_printoptions(cls):
        np.set_printoptions(threshold=sys.maxsize, linewidth=300)

    def unsure__ndarray_dtype(self) -> TYPING__NP__FINAL:
        """
        GOAL
        ----
        remake source if it not ndarray with names
        """
        if isinstance(self.SOURCE, (list, tuple)):
            if self.DEF__DTYPE_ITEMS:
                self.SOURCE = np.array(self.SOURCE, dtype=self.DEF__DTYPE_ITEMS)

        if not isinstance(self.SOURCE, np.ndarray):
            self.SOURCE = np.array(self.SOURCE)

        # TODO: make copy???
        return self.SOURCE  # return exact values just for tests!

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
    def d2_get_compact_str(
        self,
        values_translater: dict[Any, Any] = None,
        separate_rows_blocks: int = None,
        wrap: bool = None,
        use_rows_num: bool = None
    ) -> str:
        """
        :param values_translater: dictionary to change exact elements
        :param separate_rows_blocks: add blank line on step
        :param wrap: add additional strings before and after data
        :param use_rows_num: add row num in
        """
        values_translater = values_translater or {}
        count_rows = len(self.SOURCE)
        count_columns = len(self.SOURCE[0])
        row_pos = 0
        result: str = ""

        # tab_row_nums = (count_rows +1)//10 + 1
        # if (count_rows+1)%10 > 0:
        #     tab_row_nums += 1

        tab_row_nums = 4

        if wrap:
            if use_rows_num:
                result += " " * tab_row_nums
            result += "=" * count_columns + "\n"

        for row in self.SOURCE:
            row_pos += 1
            if separate_rows_blocks and row_pos > 1 and (row_pos - 1) % separate_rows_blocks == 0:
                result += f"\n"

            if use_rows_num:
                result += "{:{width}}".format(str(row_pos), width=tab_row_nums)
            for value in row:
                replaced = values_translater.get(value)
                if replaced is not None:
                    value = replaced
                result += f"{value}"

            if row_pos != count_rows:
                result += f"\n"

        if wrap:
            result += "\n"
            if use_rows_num:
                result += " " * tab_row_nums
            result += "=" * count_columns

        return result

    # -----------------------------------------------------------------------------------------------------------------
    def split_groups(self, group_len: int) -> TYPING__NP__FINAL:
        """
        GOAL
        ----
        split array to arrays with exact elements count
        NOT INLINE! and dont do it!

        SPECIALLY CREATED FOR
        ---------------------
        FOR WHAT? --- delete????  it was trying to make windows and now not used????
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
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!

    # SHRINK ----------------------------------------------------------------------------------------------------------
    def shrink(self, divider: int) -> TYPING__NP__FINAL:
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

    def shrink_simple(self, divider: int, column: str = None) -> TYPING__NP_TS__FINAL:
        """
        FIXME: DEPRECATE COLUMNS!!! - not need!!!

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
    def _windows_get(self, divider: int) -> TYPING__NP_TS__FINAL:
        bars_windows = np.lib.stride_tricks.sliding_window_view(x=self.SOURCE, window_shape=divider)
        bars_windows_stepped = bars_windows[::divider]
        return bars_windows_stepped

    def _windows_shrink(self, windows: np.ndarray) -> TYPING__NP_TS__FINAL:
        result: Optional[np.ndarray] = None
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
