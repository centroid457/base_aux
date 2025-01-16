import pytest

from base_aux.aux_argskwargs.m0_novalue import *

from base_aux.aux_pytester.m1_pytest_aux import PytestAux
from base_aux.valid.value_2_unit import ValueUnit


# =====================================================================================================================
class Test__WithUnit:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #     cls.Victim = type("Victim", (ValueUnit,), {})
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (-0, True),
            (0, True),
            (-1, True),
            (1, True),
            (1.1, True),
            ("1", True),
            ("1.1", True),
            ("1,0", True),
            ("1,0V", True),
            ("1, 0V", False),
            ("1 ,0V", False),
            ("1,,0V", False),
            ("1,.0V", False),

            ("1мк", True),
            ("1мкB", True),
            ("1мкV", True),
            ("1vV", True),
            ("1vHello", True),
            ("1vПривет", True),
            ("1v Привет", False),

            ("  -  1,0   mV   ", True),
            ("  --  1,0   mV   ", False),

            ("1.1.1", False),
            ("hello", False),
        ]
    )
    def test__validate(self, args, _EXPECTED):
        func_link = ValueUnit.validate
        PytestAux(func_link, args).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, val_orig, val_pure, mult, unit, unit_mult, unit_base",
        argvalues=[
            # minus/plus/space ------------------
            ("  - 1   k   ", -1, -1000, 1000, "k", "k", ""),
            ("-0", 0, 0, 1, "", "", ""),
            (" + 1 ", 1, 1, 1, "", "", ""),

            # DOTS ------------------------
            ("1,0", 1, 1, 1, "", "", ""),
            ("1.0", 1, 1, 1, "", "", ""),
            ("1.1", 1.1, 1.1, 1, "", "", ""),

            # mult ------------------------
            ("1k", 1, 1000, 1000, "k", "k", ""),
            ("1мк", 1, 10 ** (-6), 10 ** (-6), "мк", "мк", ""),
            ("-1k", -1, -1000, 1000, "k", "k", ""),

            # UNIT ------------------------
            ("1kHELLO", 1, 1000, 1000, "kHELLO", "k", "HELLO"),
            ("1kПРИВЕТ", 1, 1000, 1000, "kПРИВЕТ", "k", "ПРИВЕТ"),
        ]
    )
    def test__parse(self, source, val_orig, val_pure, mult, unit, unit_mult, unit_base):
        victim = ValueUnit(source)
        assert victim.VALUE == val_orig
        assert victim.VALUE_PURE == val_pure
        assert victim.MULT == mult
        assert victim.UNIT == unit
        assert victim.UNIT_MULT == unit_mult
        assert victim.UNIT_BASE == unit_base

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (1, "1"),
            (1.1, "1.1"),
            ("1", "1"),
            ("1.1", "1.1"),
            ("1,1", "1.1"),
            ("1,0", "1"),
            ("1,0V", "1V"),

            ("1.1.1", Exception),
            ("hello", Exception),
        ]
    )
    def test__str(self, args, _EXPECTED):
        func_link = lambda: str(ValueUnit(args))
        PytestAux(func_link).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (1, 1),
            (1.1, 1),
            ("1", 1),
            ("1.1", 1),
            ("1,0V", 1),
            ("1,0mV", 10 ** (-3)),
            ("1,0 mV", 10 ** (-3)),
            ("0 mV", 10 ** (-3)),
            ("0MV", 10 ** (+6)),

            ("0M", 10 ** (+6)),

            ("0M V", Exception),
        ]
    )
    def test__multiplier(self, args, _EXPECTED):
        func_link = lambda: ValueUnit(args).MULT
        PytestAux(func_link).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source1, source2, _EXPECTED",
        argvalues=[
            (0, 0, 0),

            # minus/plus -----------------
            ("-1", 1, -1),
            ("- 1", 1, -1),
            ("-  1", -1, 0),
            ("+1", -1, 1),
            ("+1", +1, 0),

            # unit -----------------------
            ("1", 1, 0),
            ("1.0", 1, 0),
            ("1.0V", 1, 0),
            ("1.0V", "1 V", 0),

            ("1.0HELLO", 1, 0),
            ("1.0kHELLO", 1000, 0),
            ("1.0kHELLO", '1k', 0),

            ("1V", "1A", Exception),

            # multiplier ------------------
            ("0.001V", "1mV", 0),
            ("0.002V", "1mV", 1),
            ("0.001V", "11 mV", -1),
            ("0.001V", "1,1mV", -1),

            ("hello", 2, Exception),

            # baseWoUnit ------------------
            ("0.001V", "1m", 0),
            ("0.001", "1m", 0),
            ("1k", "1000", 0),

            # RUS/ENG ------------
            ("1d", "1д", 0),

            # VALUENOTEXISTS ------------
            ("1", NoValue, 0),
            ("1", NoValue, 0),
            (NoValue, "1", 0),
        ]
    )
    def test__cmp_1__as_func(self, source1, source2, _EXPECTED):
        func_link = lambda: ValueUnit(source1).__cmp__(source2)
        PytestAux(func_link).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source1, obj2, _EXPECTED",
        argvalues=[
            # unit -----------------------
            (1, ValueUnit(1), True),
            ("1.0", ValueUnit(1), True),
            ("1.0V", ValueUnit(1), True),
            ("1.0V", ValueUnit("1 V"), True),

            ("1.0HELLO", ValueUnit(1), True),
            ("1.0kHELLO", ValueUnit(1000), True),
            ("1.0kHELLO", ValueUnit("1k"), True),

            ("1V", ValueUnit("1A"), Exception),

            # multiplier ------------------
            ("0.001V", ValueUnit("1mV"), True),
            ("0.002V", ValueUnit("1mV"), False),
            ("0.001V", ValueUnit("11 mV"), False),
            ("0.001V", ValueUnit("1,1mV"), False),

            ("hello", ValueUnit(2), Exception),

            # baseWoUnit ------------------
            ("0.001V", ValueUnit("1m"), True),
            ("0.001", ValueUnit("1m"), True),
            ("1k", ValueUnit("1000"), True),

            # RUS/ENG ------------
            ("1d", ValueUnit("1д"), True),

            # VALUENOTEXISTS ------------
            ("1", ValueUnit(NoValue), True),
            ("1V", ValueUnit(NoValue), True),
            ("1V", ValueUnit(NoValue, unit="V"), True),
            ("1V", ValueUnit(NoValue, unit="A"), False),
            ("1", ValueUnit(NoValue, unit="A"), True),
            ("1m", ValueUnit(NoValue, unit="A"), True),
            (ValueUnit(NoValue), "1", True),
        ]
    )
    def test__cmp_2__eq(self, source1, obj2, _EXPECTED):
        func_link = lambda: source1 == obj2
        PytestAux(func_link).assert_check(_EXPECTED)


# =====================================================================================================================
def test__arithm_x1():
    victim = ValueUnit(1)
    assert victim.VALUE == 1
    victim += 1
    assert victim.VALUE == 2

    # ---------------------------
    victim = ValueUnit("1.1V")

    victim += 0.1
    assert str(victim) == "1.2V"

    victim += 1
    assert str(victim) == "2.2V"

    victim += "1m"
    assert str(victim) == "2.201V"

    victim -= "1"
    assert str(victim) == "1.201V"

    victim -= "1001m"
    assert str(victim) == "0.2V"


def test__arithm_x3():
    victim = ValueUnit("1k")
    assert victim == 1000
    assert victim.VALUE == 1
    assert victim.VALUE_PURE == 1000
    assert int(victim) == 1000
    victim += "1k"
    assert victim.VALUE == 2
    assert victim.VALUE_PURE == 2000
    assert int(victim) == 2000

    victim = ValueUnit("1k")
    assert victim == 1000
    victim += 1
    # assert victim == 1001
    assert victim.VALUE == 1.001
    # assert victim.VALUE_PURE == 1001
    assert round(victim.VALUE_PURE) == 1001
    value = round(victim)
    assert value == 1001
    assert int(victim) == 1001        # int(1.999) == 1!!!!


def test__arithm_x3_EXPLORE():
    victim = ValueUnit("1k") + 1
    assert victim == 1001

    # ---------------------------
    # victim = ValueUnit("1.1V")
    #
    # victim += 0.1
    # assert str(victim) == "1.2V"
    #
    # victim += 1
    # assert str(victim) == "2.2V"
    #
    # victim += "1m"
    # assert str(victim) == "2.201V"
    #
    # victim -= "1"
    # assert str(victim) == "1.201V"
    #
    # victim -= "1001m"
    # assert str(victim) == "0.2V"


# =====================================================================================================================
