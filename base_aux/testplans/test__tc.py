import pytest

from base_aux.testplans.devices import *


# =====================================================================================================================
class DevicesLines_Example(DevicesKit):
    ATC: TableLine = TableLine(Base_Device)


# =====================================================================================================================
class Test__TC:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = Base_TestCase

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
    def test__cls(self):
        # EXISTS IN CLS --------------
        assert self.Victim.TCS__LIST == []
        assert self.Victim.DEV_LINES is None

        assert self.Victim.result__startup_cls is None
        assert self.Victim.result__teardown_cls is None

        # EXISTS IN INSTANCE --------------
        assert not hasattr(self.Victim, "INDEX")
        # assert not hasattr(self.Victim, "SETTINGS")
        assert not hasattr(self.Victim, "DEVICES__BREEDER_INST")

        assert not hasattr(self.Victim, "timestamp_start")
        assert not hasattr(self.Victim, "details")
        assert not hasattr(self.Victim, "exx")
        assert not hasattr(self.Victim, "progress")

    def test__cls__devices_apply__NONE(self):
        self.Victim.devices__apply()
        assert self.Victim.TCS__LIST == []

        # EXISTS IN CLS --------------
        assert self.Victim.TCS__LIST == []
        assert self.Victim.DEV_LINES is None

        assert self.Victim.result__startup_cls is None
        assert self.Victim.result__teardown_cls is None

        # EXISTS IN INSTANCE --------------
        assert not hasattr(self.Victim, "INDEX")
        # assert not hasattr(self.Victim, "SETTINGS")
        assert not hasattr(self.Victim, "DEVICES__BREEDER_INST")

        assert not hasattr(self.Victim, "timestamp_start")
        assert not hasattr(self.Victim, "details")
        assert not hasattr(self.Victim, "exx")
        assert not hasattr(self.Victim, "progress")

    def test__cls__devices_apply__example(self):
        self.Victim.DEV_LINES = DevicesLines_Example
        self.Victim.devices__apply()

        # EXISTS IN CLS --------------
        assert self.Victim.TCS__LIST != []
        assert self.Victim.DEV_LINES is not None

        assert self.Victim.result__startup_cls is None
        assert self.Victim.result__teardown_cls is None

        # EXISTS IN INSTANCE --------------
        assert not hasattr(self.Victim, "INDEX")
        # assert not hasattr(self.Victim, "SETTINGS")
        assert not hasattr(self.Victim, "DEVICES__BREEDER_INST")

        assert not hasattr(self.Victim, "timestamp_start")
        assert not hasattr(self.Victim, "details")
        assert not hasattr(self.Victim, "exx")
        assert not hasattr(self.Victim, "progress")

    # -----------------------------------------------------------------------------------------------------------------
    def test__inst(self):
        self.Victim.DEV_LINES = DevicesLines_Example
        self.Victim.devices__apply()

        # EXISTS IN CLS --------------
        assert self.Victim.TCS__LIST != []
        assert len(self.Victim.TCS__LIST) == self.Victim.DEV_LINES.COUNT

        assert self.Victim(0) is self.Victim.TCS__LIST[0]







        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!


# =====================================================================================================================
