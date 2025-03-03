import pytest

from base_aux.requirements.m2_strings import *


# =====================================================================================================================
class Test_Os:
    def setup_method(self, method):
        self.Victim = type("Victim", (ReqCheckStr_Os,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__bool(self):
        victim = self.Victim()

        assert not hasattr(victim, "WINDOWS")

        assert victim.bool_if__WINDOWS() != victim.bool_if__LINUX()
        if victim._value_actual in ["windows", ]:
            assert victim.bool_if__WINDOWS() is True

    def test__1(self):
        self.Victim.LINUX = True
        self.Victim.WINDOWS = True

        victim = self.Victim()
        assert victim._value_actual in ["windows", "linux"]
        assert victim.check() is True


# =====================================================================================================================
