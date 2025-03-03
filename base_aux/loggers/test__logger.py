import time
import pytest


# =====================================================================================================================
# KEEP FILES IN ROOT! OR IMPORT PRJ_MODULE WOULD FROM SYSTEM! NOT THIS SOURCE!!!
from base_aux.loggers.m1_logger import *


# =====================================================================================================================
class Test__1:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass
        # self.VICTIM = type("VICTIM", (Logger,), {})

    def teardown_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__maxRecursion(self):
        class Victim(Logger):
            LOG_ENABLE = True
            pass

        victim = Victim()
        for i in range(3):
            victim.LOGGER.debug(f"hello-{i}")

        assert True

    def test__disable(self):
        class VictimDisabled(Logger):
            LOG_ENABLE = False

        victim = VictimDisabled()
        victim.LOGGER.debug(f"VictimDisabled")

        time.sleep(0.2)

        assert not victim.LOG_FILEPATH.exists()

    def test__several_same_creations(self):
        # in case of starting several times like in ClientRequestsItem! see there!
        class Victim(Logger):
            LOG_ENABLE = True

        victim1 = Victim()
        assert len(victim1.LOGGER.handlers) == 1
        victim2 = Victim()
        assert len(victim2.LOGGER.handlers) == 1
        victim3 = Victim()
        assert len(victim3.LOGGER.handlers) == 1


# =====================================================================================================================
