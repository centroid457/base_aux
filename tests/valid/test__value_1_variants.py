import pytest

from base_aux.base_argskwargs import *

from base_aux.aux_pytester import *
from base_aux.valid import *


# =====================================================================================================================
class Test__ValueVariants:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = type("Victim", (ValueVariants,), {})

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
    def test__val_def__reset(self):
        victim = self.Victim(value="var1", variants=["VAR1", "VAR2"])
        assert victim.VALUE == "VAR1"
        assert victim.VALUE != "VAR2"
        assert victim.VALUE_DEFAULT == "VAR1"

        victim.VALUE = "var2"
        assert victim.VALUE != "VAR1"
        assert victim.VALUE == "VAR2"
        assert victim.VALUE_DEFAULT == "VAR1"

        victim.reset()
        assert victim.VALUE == "VAR1"
        assert victim.VALUE != "VAR2"
        assert victim.VALUE_DEFAULT == "VAR1"

    def test__double_objects(self):
        victim1 = self.Victim(value="var1", variants=["VAR1", "VAR11"])
        victim2 = self.Victim(value="var2", variants=["VAR2", "VAR22"])
        assert victim1.VALUE == "VAR1"
        assert victim2.VALUE == "VAR2"

        assert victim1.VALUE != "VAR11"
        assert victim2.VALUE != "VAR22"

        victim1.VALUE = "VAR11"
        victim2.VALUE = "VAR22"

        assert victim1.VALUE != "VAR1"
        assert victim2.VALUE != "VAR2"

        assert victim1.VALUE == "VAR11"
        assert victim2.VALUE == "VAR22"

        try:
            victim1.VALUE = "VAR2"
            assert False
        except:
            assert True

    def test__case(self):
        victim = self.Victim(value="var1", variants=["VAR1", "VAR2"])
        assert victim.VALUE == "VAR1"
        assert str(victim) == "VAR1"

        try:
            victim = self.Victim(value="var1", variants=["VAR1", "VAR2"], case_insensitive=False)
            assert False
        except:
            assert True

    def test__types__None(self):
        victim = self.Victim(variants=["NONE", ])
        assert victim.VALUE == NoValue
        # assert str(victim) == "NONE"

        victim = self.Victim(value=None, variants=["NONE", ])
        assert victim.VALUE == "NONE"
        assert str(victim) == "NONE"

        victim = self.Victim(value="None", variants=[None, ])
        assert victim.VALUE is None
        assert str(victim) == "None"

    def test__types__int(self):
        victim = self.Victim(value=1, variants=["1", ])
        assert victim.VALUE == "1"
        assert str(victim) == "1"

        victim = self.Victim(value="1", variants=[1, ])
        assert victim.VALUE == 1
        assert str(victim) == "1"

    def test__cmp__same_obj(self):
        assert self.Victim(value=None, variants=["NONE", ]) == self.Victim(value="None", variants=["NONE", ])
        assert self.Victim(value="NONE", variants=["NONE", ]) == self.Victim(value="None", variants=["NONE", ])
        assert self.Victim(value=None, variants=["None", ]) == self.Victim(value=None, variants=["NONE", ])

        assert self.Victim(value=None, variants=["None", ], case_insensitive=False) != self.Victim(value=None, variants=["NONE", ])

    def test__cmp__simple_value(self):
        assert self.Victim(value=None, variants=["NONE", ]) == "NONE"
        assert self.Victim(value="NONE", variants=["NONE", ]) == "NONE"
        assert self.Victim(value=None, variants=["None", ]) == "NONE"
        assert self.Victim(value=None, variants=[None, ]) == "NONE"
        assert self.Victim(value=None, variants=[None, ], case_insensitive=False) != "NONE"
        assert self.Victim(value=None, variants=[None, ], case_insensitive=False) == "None"

    def test__contain(self):
        victim = self.Victim(variants=["NONE", ])
        assert None in victim
        assert "None" in victim
        assert "NONE" in victim

    def test__len(self):
        assert len(self.Victim(variants=[0, ])) == 1
        assert len(self.Victim(variants=[0, 1])) == 2

    def test__iter(self):
        assert list(self.Victim(variants=[0, ])) == [0, ]
        assert list(self.Victim(variants=[0, 1])) == [0, 1, ]

    def test__getitem(self):
        assert self.Victim(variants=[0, 1])[0] == 0
        assert self.Victim(variants=[0, 1])[1] == 1
        assert self.Victim(variants=[0, 1])[-1] == 1

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source1, obj2, _EXPECTED",
        argvalues=[
            (0, ValueVariants(0, variants=[0, 1]), True),
            (1, ValueVariants(0, variants=[0, 1]), False),
            (2, ValueVariants(0, variants=[0, 1]), False),

            ("0", ValueVariants(0, variants=[0, 1]), True),
            ("00", ValueVariants(0, variants=[0, 1]), False),

            (ValueUnit(0), ValueVariants(0, variants=[0, 1]), True),
        ]
    )
    def test__cmp_objs__value(self, source1, obj2, _EXPECTED):
        func_link = lambda: source1 == obj2
        PytestAux(func_link).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source1, obj2, _EXPECTED",
        argvalues=[
            (0, ValueVariants(variants=[0, 1]), True),
            (1, ValueVariants(variants=[0, 1]), True),
            (2, ValueVariants(variants=[0, 1]), False),

            ("0", ValueVariants(variants=[0, 1]), True),
            ("00", ValueVariants(variants=[0, 1]), False),

            (ValueVariants(variants=[0, 1]), ValueUnit(0), True),
            (ValueUnit(0), ValueVariants(variants=[0, 1]), True),
        ]
    )
    def test__cmp_objs__no_value(self, source1, obj2, _EXPECTED):
        func_link = lambda: source1 == obj2
        PytestAux(func_link).assert_check(_EXPECTED)


# =====================================================================================================================
def test__0():
    vu = ValueUnit(0)
    vv = ValueVariants(variants=[0, 1])

    assert vv == vu
    assert vu == vv


# =====================================================================================================================
