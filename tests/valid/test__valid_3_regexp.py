from typing import *
import pytest

from base_aux.funcs import *
from base_aux.valid import *


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
        pytest_func_tester__no_kwargs(func_link, value, _EXPECTED)


# =====================================================================================================================
