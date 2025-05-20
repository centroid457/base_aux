import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.breeders.m3_table_inst import *


# =====================================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================


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

TL_None: TableLine = TableLine()
TL_11: TableLine = TableLine(11)
TL_22: TableLine = TableLine(22)
TL_11_22: TableLine = TableLine(11, 22)
TL_11_22_33: TableLine = TableLine(11, 22, 33)


# =====================================================================================================================
class Test__1_TableLine:
    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="tline, _EXPECTED",
        argvalues=[
            (TL_None, 0),
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
            (TL_None, 0, Exception),

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
            (TL_None, "echo", (), 0, Exception),

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
            (TL_None, 11, False),

            (TL_None, TL_None, True),
            (TL_None, TL_11, False),

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

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="insts, _EXPECTED",
        argvalues=[
            ([Value11, Value11], [Value11, ]),
            ([Value11, Value11, Value22], [Value11, Value22]),
            ([Value11, Value22, Value11], [Value11, Value22, Value11]),
        ]
    )
    def test__iter(self, insts, _EXPECTED):
        func_link = lambda: [*TableLine(*insts)]
        ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================


class TLS_1_1(TableKit):
    SINGLE: TableKit = TL_11


class TLS_1_3(TableKit):
    MULTY = TL_11_22_33


class TLS_3_3(TableKit):
    SINGLE = TL_11
    MULTY = TL_11_22_33
    SINGLE2 = TL_22


class TLS_Exx(TableKit):
    SINGLE = TL_11
    MULTY = TL_11_22_33
    MULTY2 = TL_11_22


# ---------------------------------------------------------------------------------------------------------------------
class Test__2_TableLines:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (TLS_1_1, True),
            (TLS_1_3, True),
            (TLS_3_3, True),
            (TLS_Exx, False),
        ]
    )
    def test__init_noRaise__attrs(self, source, _EXPECTED):
        try:
            source()
        except:
            assert not _EXPECTED
        else:
            assert _EXPECTED

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (dict(
                SINGLE = TL_11
            ), True),
            (dict(
                MULTY = TL_11_22_33
            ), True),
            (dict(
                SINGLE = TL_11,
                MULTY = TL_11_22_33,
                SINGLE2 = TL_22,
            ), True),
            (dict(
                SINGLE=TL_11,
                MULTY = TL_11_22_33,
                MULTY2 = TL_11_22,
            ), False),
        ]
    )
    def test__init_noRaise__kwargs(self, source, _EXPECTED):
        try:
            TableKit(**source)
        except:
            assert not _EXPECTED
        else:
            assert _EXPECTED

    @pytest.mark.parametrize(
        argnames="cls, kwargs, _EXPECTED",
        argvalues=[
            (TLS_1_1, dict(
                SINGLE = TL_11
            ), True),
            (TLS_1_3, dict(
                MULTY = TL_11_22_33
            ), True),
            (TLS_3_3, dict(
                SINGLE = TL_11,
                MULTY = TL_11_22_33,
                SINGLE2 = TL_22,
            ), True),
            (TLS_Exx, dict(
                # MULTY=TL_11_22,
            ), False),
            (TLS_Exx, dict(
                MULTY = TL_11_22,
            ), True),
        ]
    )
    def test__init_noRaise__kwargs_overload(self, cls, kwargs, _EXPECTED):
        try:
            cls(**kwargs)
        except:
            assert not _EXPECTED
        else:
            assert _EXPECTED

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
        argnames="source, _EXPECTED",
        argvalues=[
            (TLS_1_1, [11, ]),
            (TLS_1_3, [11, 22, 33]),
            (TLS_3_3, [11, 22, 33, 11, 22]),
        ]
    )
    def test__iter_lines_insts(self, source, _EXPECTED):
        func_link = lambda s: [*s().iter_lines_insts()] == _EXPECTED
        ExpectAux(func_link, source).check_assert()

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
        argnames="source, name, _EXPECTED",
        argvalues=[
            (TLS_1_1, 0, Exception),
            (TLS_1_1, "hello", Exception),
            (TLS_1_1, "SINGLE", TL_11),
            (TLS_1_3, "MULTY", TL_11_22_33),

            (TLS_3_3, 1, Exception),
            (TLS_3_3, "hello", Exception),
            (TLS_3_3, "MULTY", TL_11_22_33),
            (TLS_3_3, "SINGLE", TL_11),
            (TLS_3_3, "SINGLE2", TL_22),
        ]
    )
    def test__gi(self, source, name, _EXPECTED):
        func_link = lambda s: s()[name]
        ExpectAux(func_link, source).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    def test__call(self):
        class Victim(TableKit):
            TL_11 = TableLine(11)
            TL_V88 = TableLine(Value(88))
            TL_11_V99 = TableLine(11, Value(99))

        victim = Victim()
        results = victim("return_value")

        r_TL_11 = results["TL_11"]
        assert isinstance(r_TL_11[0], Exception)

        r_TL_V88 = results["TL_V88"]
        assert r_TL_V88[0] == 88

        r_TL_11_V99 = results["TL_11_V99"]
        assert isinstance(r_TL_11_V99[0], Exception)
        assert r_TL_11_V99[1] == 99


# =====================================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================
pass    # =============================================================================================================


class Test__3_TableColumn:
    @pytest.mark.parametrize(
        argnames="tls, index, _EXPECTED",
        argvalues=[
            (TLS_1_1(), 0, True),
            (TLS_1_1(), 1, False),
            (TLS_1_1(), -1, True),

            # (TLS_1_3(), 0, True),

            (TLS_3_3(), 0, True),
            (TLS_3_3(), 1, True),
            (TLS_3_3(), 2, True),
            (TLS_3_3(), 3, False),
            (TLS_3_3(), -1, True),
        ]
    )
    def test__init_noRaise(self, tls, index, _EXPECTED):
        try:
            victim = TableColumn(lines=tls, index=index)
            assert victim.LINES == tls
        except:
            assert not _EXPECTED
        else:
            assert _EXPECTED

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="tls, index, name, _EXPECTED",
        argvalues=[
            (TLS_1_1(), 0, "SINGLE", 11),
            (TLS_1_1(), -1, "SINGLE", 11),
            (TLS_1_1(), 0, "MULTY", Exception),

            # (TLS_1_3(), 0, True),

            (TLS_3_3(), 0, "SINGLE", 11),
            (TLS_3_3(), 1, "SINGLE", 11),
            (TLS_3_3(), 2, "SINGLE", 11),

            (TLS_3_3(), 0, "SINGLE2", 22),
            (TLS_3_3(), 1, "SINGLE2", 22),
            (TLS_3_3(), 2, "SINGLE2", 22),

            (TLS_3_3(), 0, "MULTY", 11),
            (TLS_3_3(), 1, "MULTY", 22),
            (TLS_3_3(), 2, "MULTY", 33),
            (TLS_3_3(), -1, "MULTY", 33),
        ]
    )
    def test__item_access(self, tls, index, name, _EXPECTED):
        victim = TableColumn(lines=tls, index=index)
        ExpectAux(getattr, (victim, name)).check_assert(_EXPECTED)


# =====================================================================================================================
