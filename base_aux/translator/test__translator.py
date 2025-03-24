import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux

from base_aux.translator.m1_translator import *


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



            # FIXME: need resolve!!!1
            # (NestInit_AttrsOnlyByKwArgs(a1=22), False, "a11", NoValue),
            # (NestInit_AttrsOnlyByKwArgs(a1=22), True, "a11", "a11"),
            #
            # (NestInit_AttrsOnlyByKwArgs(a1=22), None, "a1", 22),
        ]
    )
    def test__direct(self, rules, notFound, source, _EXPECTED):
        func_link = Translator(rules=rules, return_source_if_not_found=notFound)
        ExpectAux(func_link, source).check_assert(_EXPECTED)


# =====================================================================================================================
