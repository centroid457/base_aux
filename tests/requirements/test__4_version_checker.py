from typing import *
import pytest

from base_aux.requirements import *
from base_aux.funcs import *


# =====================================================================================================================
class Test__ReqCheckVersion_Python:
    Victim: type[CheckVersion_Python]
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = CheckVersion_Python

    # @classmethod
    # def teardown_class(cls):
    #     if cls.victim:
    #         cls.victim.disconnect()
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__cmp_str(self):
        assert self.Victim("1.2rc2.3").check_eq("1.02rc2.3") is True
        assert self.Victim("1.2rc2.3").check_eq("1.2rc2.33") is False

        assert self.Victim("1.2rc2.3").check_ne("1.02rc2.3") is False
        assert self.Victim("1.2rc2.3").check_ne("1.2rc2.33") is True

        assert self.Victim("1.2").check_le("1.2rc2.3") is True
        assert self.Victim("1.2").check_lt("1.2rc2.3") is True

        assert self.Victim("1.2").check_ge("1.2rc2.3") is False
        assert self.Victim("1.2").check_gt("1.2rc2.3") is False

    def test__py(self):
        assert self.Victim().check_eq("1.02rc2.3") is False
        assert self.Victim().check_gt("1.02rc2.3") is True

    def test__raise(self):
        # IF -----------------
        try:
            self.Victim("1.2").raise_if__check_eq("1.02")
        except:
            pass
        else:
            assert False

        self.Victim("1.2").raise_if__check_eq("1.22")

        # IF NOT -----------------
        self.Victim("1.2").raise_if_not__check_eq("1.02")
        try:
            self.Victim("1.2").raise_if_not__check_eq("1.22")
        except:
            pass
        else:
            assert False

    # @pytest.mark.parametrize(
    #     argnames="args, EXPECTED",
    #     argvalues=[
    #         (("1.2rc2.3", "1.2rc2.3"), True),
    #     ]
    # )
    # def test__inst__cmp__eq(self, args, EXPECTED):
    #     func_link = lambda source1, source2: self.Victim().check_eq("1.02rc2.3")
    #     pytest_func_tester__no_kwargs(func_link, args, EXPECTED)


# =====================================================================================================================
