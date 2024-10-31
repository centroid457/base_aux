from typing import *
import pytest
from base_aux.testplans import *
from base_aux.buses import *


# =====================================================================================================================
class Test__DeviceBase:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = type("Victim", (DeviceBase,), {})

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
    def test__1(self):
        victim = self.Victim()

    def test__2(self):
        victim = self.Victim()
        assert victim.INDEX is None

        victim = self.Victim(2)
        assert victim.INDEX == 2


# =====================================================================================================================
class Test__DevicesBreeder_WithDut:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass
        self.Victim: Type[DevicesBreeder_WithDut] = type("Victim", (DevicesBreeder_WithDut,), {})

    def teardown_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__DUT_COUNT(self):
        # 1 -----------------------------------------------------
        self.Victim.COUNT = 1
        self.Victim.generate__objects()

        victim = self.Victim(0)
        assert victim.DUT == self.Victim.LIST__DUT[0]
        assert victim.DUT == victim.LIST__DUT[0]

        # 2 ------------------------------------------------------
        self.Victim.COUNT = 2
        self.Victim.generate__objects(force=True)
        #
        # # INSTANCE ----------------------
        victim = self.Victim(0)
        assert victim.DUT.INDEX == 0
        assert victim.DUT == self.Victim.LIST__DUT[0]
        assert victim.DUT == victim.LIST__DUT[0]

        victim = self.Victim(1)
        assert victim.DUT.INDEX == 1
        assert victim.DUT == self.Victim.LIST__DUT[1]
        assert victim.DUT == victim.LIST__DUT[1]

        assert victim.LIST__DUT[0] != victim.LIST__DUT[1]
        assert self.Victim.LIST__DUT[0] != self.Victim.LIST__DUT[1]

    # -----------------------------------------------------------------------------------------------------------------
    def test__CLS_SINGLE__CLS(self):
        self.Victim.COUNT = 2
        self.Victim.CLS_SINGLE__ATC = DeviceBase
        self.Victim.generate__objects()

        assert hasattr(self.Victim, "LIST__DUT") is True
        assert hasattr(self.Victim, "LIST__ATC") is False

        assert self.Victim.group_check__exists("DUT") is True
        assert self.Victim.group_check__exists("ATC") is True
        assert self.Victim.group_check__exists("PTS") is False

        # DISCONNECT
        self.Victim.disconnect__cls()

        self.Victim.generate__objects()

    def test__CLS_SINGLE__INSTANCE(self):
        self.Victim.COUNT = 2
        self.Victim.CLS_SINGLE__ATC = DeviceBase
        self.Victim.generate__objects()

        victim = self.Victim(1)

        assert victim.DUT == victim.LIST__DUT[1]
        try:
            victim.PTS
            assert False
        except:
            pass

        assert hasattr(victim, "LIST__DUT") is True
        try:
            hasattr(victim, "LIST__ATC")
            assert False
        except:
            pass

        assert victim.group_check__exists("DUT") is True
        assert victim.group_check__exists("ATC") is True
        assert victim.group_check__exists("PTS") is False

    # -----------------------------------------------------------------------------------------------------------------
    def test__CLS_LIST__CLS(self):
        self.Victim.COUNT = 2
        self.Victim.CLS_LIST__PTS = DeviceBase
        self.Victim.generate__objects()

        assert hasattr(self.Victim, "LIST__DUT") is True
        assert hasattr(self.Victim, "LIST__PTS") is True

        assert len(self.Victim.LIST__DUT) == 2
        assert len(self.Victim.LIST__PTS) == 2

        assert self.Victim.group_check__exists("DUT") is True
        assert self.Victim.group_check__exists("ATC") is False
        assert self.Victim.group_check__exists("PTS") is True

    def test__CLS_LIST__INSTANCE(self):
        self.Victim.COUNT = 2
        self.Victim.CLS_LIST__PTS = DeviceBase
        self.Victim.generate__objects()

        victim = self.Victim(1)

        assert victim.DUT == victim.LIST__DUT[1]
        assert victim.PTS == victim.LIST__PTS[1]
        try:
            victim.ATC
            assert False
        except:
            pass

        assert hasattr(victim, "LIST__DUT") is True
        assert hasattr(victim, "LIST__PTS") is True

        assert len(victim.LIST__DUT) == 2
        assert len(victim.LIST__PTS) == 2

        assert victim.group_check__exists("DUT") is True
        assert victim.group_check__exists("ATC") is False
        assert victim.group_check__exists("PTS") is True

    # -----------------------------------------------------------------------------------------------------------------
    def test__double_init(self):
        # insts is the same!
        pass

    # def reconnect


# =====================================================================================================================
