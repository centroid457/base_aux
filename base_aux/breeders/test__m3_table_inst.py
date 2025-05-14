import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.breeders.m3_table_inst import *


# =====================================================================================================================
class Value:
    VALUE: Any

    def __init__(self, value: Any):
        self.VALUE = value

    def echo(self, echo: Any = None):
        return echo

    def return_value(self):
        return self.VALUE


# =====================================================================================================================
class Test__TableLine:
    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="tline, _EXPECTED",
        argvalues=[
            (TableLine(11), 1),
            (TableLine(11, 22), 2),
            (TableLine(11, 22, 33), 3),
        ]
    )
    def test__count(self, tline, _EXPECTED):
        ExpectAux(getattr(tline, "COUNT")).check_assert(_EXPECTED)
        ExpectAux(len(tline)).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="tline, index, _EXPECTED",
        argvalues=[
            (TableLine(11), 0, 11),
            (TableLine(11), 1, 11),
            (TableLine(11), 2, 11),

            (TableLine(11, 22), 0, 11),
            (TableLine(11, 22), 1, 22),
            (TableLine(11, 22), 2, Exception),

            (TableLine(11, 22, 33), 0, 11),
            (TableLine(11, 22, 33), 1, 22),
            (TableLine(11, 22, 33), 2, 33),
            (TableLine(11, 22, 33), 3, Exception),
        ]
    )
    def test__gi(self, tline, index, _EXPECTED):
        func_link = lambda i: tline[i]
        ExpectAux(func_link, index).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="tline, index, _EXPECTED",
        argvalues=[
            (TableLine(11), 0, 11),
            (TableLine(11), 1, 11),

            (TableLine(0, Value(11), Value(22)), 0, 11),
        ]
    )
    def test__call(self, tline, index, _EXPECTED):
        func_link = lambda i: tline[i]
        ExpectAux(func_link, index).check_assert(_EXPECTED)







# =====================================================================================================================
