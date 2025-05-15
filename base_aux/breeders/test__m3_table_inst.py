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
        func_link = lambda: tline(meth, *args)[index]
        ExpectAux(func_link).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="obj1, obj2, _EXPECTED",
        argvalues=[
            (TableLine(11), 11, False),

            (TableLine(11), TableLine(11), True),
            (TableLine(11), TableLine(22), False),

            (TableLine(11), TableLine(11, 11), False),
            (TableLine(11, 11), TableLine(11, 11), True),
            (TableLine(11, 11), TableLine(11), False),

            (TableLine(11), TableLine(11, Value(11)), False),
        ]
    )
    def test__eq(self, obj1, obj2, _EXPECTED):
        func_link = lambda: obj1 == obj2
        ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
class Test__TableLines:
    def test__init__count__size(self):
        # ------------
        class Victim(TableLines):
            SINGLE = TableLine(11)

        victim = Victim()
        assert victim.COUNT_COLUMNS == 1
        assert len(victim) == 1
        assert victim.size() == (1, 1)

        # ------------
        class Victim(TableLines):
            MULTY = TableLine(11, 22, 33)

        victim = Victim()
        assert victim.COUNT_COLUMNS == 3
        assert len(victim) == 1
        assert victim.size() == (1, 3)

        # ------------
        class Victim(TableLines):
            SINGLE = TableLine(11)
            MULTY = TableLine(11, 22, 33)
            SINGLE2 = TableLine(11)

        victim = Victim()
        assert victim.COUNT_COLUMNS == 3
        assert len(victim) == 3
        assert victim.size() == (3, 3)

        # ------------
        class Victim(TableLines):
            SINGLE = TableLine(11)
            MULTY = TableLine(11, 22, 33)
            MULTY2 = TableLine(11, 22, 33, 44)

        try:
            victim = Victim()
            assert False
        except:
            pass

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
