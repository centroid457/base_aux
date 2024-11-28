import pytest

from base_aux.funcs import *
from base_aux.classes import *
from base_aux.classes import Translator, AttrInitKwargs


# =====================================================================================================================
class Test__1:
    @pytest.mark.parametrize(
        argnames="rules, validator, notFound, source, _EXPECTED",
        argvalues=[
            ({1:11, 2:22}, None, None, 1, 11),
            ({1:11, 2:22}, None, None, 2, 22),
            ({1:11, 2:22}, None, None, 3, 3),
            ({1:11, 2:22}, None, False, 3, ValueNotExist),
            ({1:11, 2:22}, None, True, "hello", "hello"),
            ({1:11, 2:22}, None, False, "hello", ValueNotExist),
        ]
    )
    def test__direct(self, rules, validator, notFound, source, _EXPECTED):
        func_link = Translator(rules, validator, notFound)
        pytest_func_tester__no_kwargs(func_link, source, _EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="rules, validator, notFound, source, _EXPECTED",
        argvalues=[
            ({1:11, 2:22}, lambda source, var: source.hello == var, None, AttrInitKwargs(**{"hello": 2}), 22),
        ]
    )
    def test__Dots(self, rules, validator, notFound, source, _EXPECTED):
        func_link = Translator(rules, validator, notFound)
        pytest_func_tester__no_kwargs(func_link, source, _EXPECTED)


# =====================================================================================================================
