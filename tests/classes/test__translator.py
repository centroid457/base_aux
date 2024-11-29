import pytest

from base_aux.funcs import *
from base_aux.classes import *


# =====================================================================================================================
class Test__1:
    @pytest.mark.parametrize(
        argnames="rules, notFound, source, _EXPECTED",
        argvalues=[
            ({1:11, 2:22}, None, 1, 11),
            ({1:11, 2:22}, None, 2, 22),
            ({1:11, 2:22}, None, 3, 3),
            ({1:11, 2:22}, False, 3, ValueNotExist),
            ({1:11, 2:22}, True, "hello", "hello"),
            ({1:11, 2:22}, False, "hello", ValueNotExist),

            (AttrInitKwargs(**{"a1": 22}), False, "a11", ValueNotExist),
            (AttrInitKwargs(**{"a1": 22}), True, "a11", "a11"),

            (AttrInitKwargs(**{"a1": 22}), None, "a1", 22),
        ]
    )
    def test__direct(self, rules, notFound, source, _EXPECTED):
        func_link = Translator(rules=rules, return_source_if_not_found=notFound)
        pytest_func_tester__no_kwargs(func_link, source, _EXPECTED)


# =====================================================================================================================
