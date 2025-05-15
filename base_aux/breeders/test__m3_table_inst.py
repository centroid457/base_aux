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


# just keep final INSTANCES to make a memory comparing!
Value11 = Value(11)
Value22 = Value(22)
Value33 = Value(33)

TL_11: TableLine = TableLine(11)
TL_22: TableLine = TableLine(22)
TL_11_22: TableLine = TableLine(11, 22)
TL_11_22_33: TableLine = TableLine(11, 22, 33)


# =====================================================================================================================
class Test__TableLine:
    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="tline, _EXPECTED",
        argvalues=[
            (TL_11, 1),
            (TL_11_22, 2),
            (TL_11_22_33, 3),
        ]
    )
    def test__count(self, tline, _EXPECTED):
        ExpectAux(getattr(tline, "COUNT")).check_assert(_EXPECTED)
        ExpectAux(len(tline)).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="tline, index, _EXPECTED",
        argvalues=[
            (TL_11, 0, 11),
            (TL_11, 1, 11),
            (TL_11, 2, 11),

            (TL_11_22, 0, 11),
            (TL_11_22, 1, 22),
            (TL_11_22, 2, Exception),

            (TL_11_22_33, 0, 11),
            (TL_11_22_33, 1, 22),
            (TL_11_22_33, 2, 33),
            (TL_11_22_33, 3, Exception),
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
            (TL_11, "echo", (), 0, Exception),
            (TableLine(11, Value11), "echo", (), 0, Exception),
            (TableLine(11, Value11), "echo", (), 1, None),
            (TableLine(11, Value11), "echo", (111,), 1, 111),
        ]
    )
    def test__call(self, tline, meth, args, index, _EXPECTED):
        func_link = lambda: tline(meth, *args)[index]
        ExpectAux(func_link).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="obj1, obj2, _EXPECTED",
        argvalues=[
            (TL_11, 11, False),

            (TL_11, TL_11, True),
            (TL_11, TL_22, False),

            (TL_11, TableLine(11, 11), False),
            (TableLine(11, 11), TableLine(11, 11), True),
            (TableLine(11, 11), TL_11, False),

            (TL_11, TableLine(11, Value11), False),
        ]
    )
    def test__eq(self, obj1, obj2, _EXPECTED):
        func_link = lambda: obj1 == obj2
        ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
class TLS_1_1(TableLines):
    SINGLE = TL_11


class TLS_1_3(TableLines):
    MULTY = TL_11_22_33


class TLS_3_3(TableLines):
    SINGLE = TL_11
    MULTY = TL_11_22_33
    SINGLE2 = TL_22


class TLS_Exx(TableLines):
    SINGLE = TL_11
    MULTY = TL_11_22_33
    MULTY2 = TL_11_22


# ---------------------------------------------------------------------------------------------------------------------
class Test__TableLines:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (TLS_1_1, True),
            (TLS_1_3, True),
            (TLS_3_3, True),
            (TLS_Exx, Exception),
        ]
    )
    def test__init_correct(self, source, _EXPECTED):
        func_link = lambda s: isinstance(s(), TableLines)
        ExpectAux(func_link, source).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (TLS_1_1, (1,1)),
            (TLS_1_3, (1,3)),
            (TLS_3_3, (3,3)),
            (TLS_Exx, Exception),
        ]
    )
    def test__size(self, source, _EXPECTED):
        try:
            victim = source()
        except:
            assert _EXPECTED == Exception
            return

        assert len(victim) == _EXPECTED[0]
        assert victim.COUNT_COLUMNS == _EXPECTED[1]
        assert victim.size() == _EXPECTED

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, names, values",
        argvalues=[
            (TLS_1_1, ["SINGLE", ], [TL_11, ]),
            (TLS_1_3, ["MULTY", ], [TL_11_22_33, ]),
            (TLS_3_3, ["MULTY", "SINGLE", "SINGLE2"], [TL_11_22_33, TL_11, TL_22, ]),
        ]
    )
    def test__names_values_items(self, source, names, values):
        func_link = lambda s: s().names()
        ExpectAux(func_link, source).check_assert(names)

        func_link = lambda s: s().values()
        ExpectAux(func_link, source).check_assert(values)

        func_link = lambda s: [*s().items()]
        ExpectAux(func_link, source).check_assert([*zip(names, values)])














    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="tline, meth, args, index, _EXPECTED",
        argvalues=[
            (TL_11, "echo", (), 0, Exception),
            (TableLine(11, Value11), "echo", (), 0, Exception),
            (TableLine(11, Value11), "echo", (), 1, None),
            (TableLine(11, Value11), "echo", (111,), 1, 111),
        ]
    )
    def test__call(self, tline, meth, args, index, _EXPECTED):
        func_link = lambda m, a: tline(m, *a)[index]
        ExpectAux(func_link, (meth, args)).check_assert(_EXPECTED)


# =====================================================================================================================
