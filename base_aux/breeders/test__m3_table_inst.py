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
    def test__gi_in(self, tline, index, _EXPECTED):
        func_link = lambda i: tline[i]
        ExpectAux(func_link, index).check_assert(_EXPECTED)

        if _EXPECTED is not Exception:
            assert _EXPECTED in tline

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="tline, meth, args, index, _EXPECTED",
        argvalues=[
            (TableLine(11), "echo", (), 0, Exception),
            (TableLine(11, Value(11)), "echo", (), 0, Exception),
            (TableLine(11, Value(11)), "echo", (), 1, None),
            (TableLine(11, Value(11)), "echo", (111, ), 1, 111),
        ]
    )
    def test__call(self, tline, meth, args, index, _EXPECTED):
        func_link = lambda m, a: tline(m, *a)[index]
        ExpectAux(func_link, (meth, args)).check_assert(_EXPECTED)







# =====================================================================================================================
