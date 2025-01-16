import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux
from base_aux.aux_argskwargs import *

from base_aux.aux_attr.m1_attr_0_init_kwargs import *
from base_aux.classes.translator import *


# =====================================================================================================================
class Test__1:
    @pytest.mark.parametrize(
        argnames="rules, notFound, source, _EXPECTED",
        argvalues=[
            ({1:11, 2:22}, None, 1, 11),
            ({1:11, 2:22}, None, 2, 22),
            ({1:11, 2:22}, None, 3, 3),
            ({1:11, 2:22}, False, 3, NoValue),
            ({1:11, 2:22}, True, "hello", "hello"),
            ({1:11, 2:22}, False, "hello", NoValue),

            (AttrsInitByKwArgs(a1=22), False, "a11", NoValue),
            (AttrsInitByKwArgs(a1=22), True, "a11", "a11"),

            (AttrsInitByKwArgs(a1=22), None, "a1", 22),
        ]
    )
    def test__direct(self, rules, notFound, source, _EXPECTED):
        func_link = Translator(rules=rules, return_source_if_not_found=notFound)
        PytestAux(func_link, source).assert_check(_EXPECTED)


# =====================================================================================================================
