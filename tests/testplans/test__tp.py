from typing import *
import pytest

from base_aux.testplans import *


# =====================================================================================================================
class Test__Tp:
    @classmethod
    def setup_class(cls):
        pass

        class Victim(TpMultyDutBase):
            pass

        cls.Victim = Victim

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     passtest__tc.py
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.skip
    def test__1(self):
        victim = self.Victim()
        assert not victim.DEVICES__BREEDER_CLS
        assert not victim.DEVICES__BY_INDEX
        assert not victim.INDEX
        assert not victim.TCS__INST

        assert not victim.result
        assert not victim.details
        assert not victim.exx
        assert victim.progress == 0

        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!


# =====================================================================================================================
