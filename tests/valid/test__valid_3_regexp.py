from typing import *
import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux
from base_aux.valid.m3_valid_regexp import *


# =====================================================================================================================
class Test__ReqExp:
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
        argnames="pats, value, _EXPECTED",
        argvalues=[
            (r"\d?", 1, True),
            ([r"\d?", r"\s*\d*"], 1, True),
            ([r"\d?", r"\s*\d*"], 10, True),
            ([r"\d?", r"\s*\d*"], "10.1", False),
        ]
    )
    def test__validate(self, pats, value, _EXPECTED):
        func_link = ValidRegExp(pats).run
        PytestAux(func_link, value).assert_check(_EXPECTED)


# =====================================================================================================================
