from typing import *
import pytest

from base_aux.aux_pytester import *
from base_aux.classes import *


# =====================================================================================================================
class Victim(NumberArithmTranslateToAttr):
    NUMBER_ARITHM__GETATTR_NAME = "VAL"

    def __init__(self, val):
        self.VAL = val


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, EXPECTED",
    argvalues=[
        (Victim(0), "0"),
        (Victim(0.0), "0"),

        (Victim(1), "1"),
        (Victim(1.1), "1.1"),
        (Victim(1.1) + 0.1, "1.2"),
        (Victim(1.111222) + 0.000111222, "1.111333"),

        (Victim(0.000000111), "0"),
        (Victim(0.000002111), "0.000002"),

        ((Victim(0.000002111), 6), "0.000002"),
        ((Victim(0.000002111), 3), "0"),
    ]
)
def test__precision_str(args, _EXPECTED):
    func_link = NumberArithmTranslateToAttr.number__get_string_no_zeros
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, EXPECTED",
    argvalues=[
        (0, 0),
        (1, 1),
        (1.0, 1),
        (1.1, 1.1),
        (None, None),
        ("1.0", 1),
        ("0001.0", 1),
        ("1.1", "1.1"),

        (Victim(0), 0),
        (Victim(0.0), 0),

        (Victim(1), 1),
        (Victim(1.1), 1.1),

        (Victim(0.000000111), 0.000000111),
    ]
)
def test__precision_str(args, _EXPECTED):
    func_link = NumberArithmTranslateToAttr.number__try_int_if_same
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
class Test__Number:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #     cls.Victim = Victim
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
    def test__arithm(self):
        victim = Victim(1)
        # ObjectInfo(victim).print()
        assert victim.VAL == 1

        victim = victim + 1
        assert victim.VAL == 2

        victim += 1
        assert victim.VAL == 3

        victim = -victim
        assert victim.VAL == -3

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="expr",
        argvalues=[
            (Victim(1) == 1),
            (Victim(0.9) < 1),
            (Victim(0.9) > -1),
            (Victim(0.9) > 0.8),
            (Victim(-0.9) < 0.8),
        ]
    )
    def test__cmp(self, expr):
        pytest_func_tester__no_args_kwargs(expr)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="expr, EXPECTED",
        argvalues=[
            (Victim(0.001), 0.001),
            (Victim(0.001) - 0.001, 0),

            (round(Victim(0.001) - 0.0001, 3), 0.001),
            (round(Victim(0.001) + 0.0001, 3), 0.001),
            (round(Victim(0.001) + 0.0005, 3), 0.002),
        ]
    )
    def test__precision(self, expr, _EXPECTED):
        pytest_func_tester__no_args_kwargs(expr, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="expr, EXPECTED",
        argvalues=[
            (Victim(0), "0"),
            (Victim(0.0), "0"),

            (Victim(1), "1"),
            (Victim(1.1), "1.1"),
            (Victim(1.1) + 0.1, "1.2"),
            (Victim(1.111222) + 0.000111222, "1.111333"),

            (Victim(0.000000111), "0"),
            (Victim(0.000002111), "0.000002"),
        ]
    )
    def test__str(self, expr, _EXPECTED):
        func_link = str(expr)
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
