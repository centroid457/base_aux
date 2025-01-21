from typing import *
import numpy as np

from base_aux.base_source.m1_source import InitSource


# =====================================================================================================================
@final
class ArrayAux(InitSource):
    SOURCE: np.ndarray

    def d2_get_compact_str(
        self,
        interpreter: Optional[dict[Any, Any]] = None,
        separate_rows: Optional[int] = None,
        wrap: Optional[bool] = None,
        use_rows_num: Optional[bool] = None
    ) -> str:
        """

        :param array:
        :param interpreter: dictionary to change some elements
        :param separate_rows: add blank line on step
        :param wrap: add additional strings before and after data
        :param use_rows_num: add row num in
        :return:
        """
        interpreter = interpreter or {}
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
            if separate_rows and row_pos > 1 and (row_pos - 1) % separate_rows == 0:
                result += f"\n"

            if use_rows_num:
                result += "{:{width}}".format(str(row_pos), width=tab_row_nums)
            for value in row:
                replaced = interpreter.get(value)
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


# =====================================================================================================================
