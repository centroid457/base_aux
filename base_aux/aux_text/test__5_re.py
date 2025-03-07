import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_text.m5_re2_attemps import *


# =====================================================================================================================
class Test__sub:
    @pytest.mark.parametrize(
        argnames="source, rule, _EXPECTED",
        argvalues=[
            # NOT ACCEPTED -------------
            ("None123", ("None", "null"), "None123"),
            ("None_123", ("None", "null"), "None_123"),

            # ACCEPTED -------------
            ("null", ("None", "null"), "null"),
            ("None", ("None", "null"), "null"),
            ("None-123", ("None", "null"), "null-123"),

            # CONTAINERS -------------
            ("[null]", ("None", "null"), "[null]"),
            ("[None]", ("None", "null"), "[null]"),
            ("[None, ]", ("None", "null"), "[null, ]"),

            (" None, 123", ("None", "null"), " null, 123"),
            ("[None, null, 123]", ("None", "null"), "[null, null, 123]"),

            ("[None, null, 323]", (r"None.*3", "null"), "[null]"),

            ("[None, null, 3 23]", (r"None.*3", "null"), "[null]"),
            ("[None, null, 3 23]", (r"None.*?3", "null"), "[null 23]"),
        ]
    )
    def _test__1(self, source, rule, _EXPECTED):
        func_link = ReAttemptsFirst(source).search
        ExpectAux(func_link, rule).check_assert(_EXPECTED)


# =====================================================================================================================
