import pytest
from base_aux.breeders.m3_table_inst import *
from base_aux.testplans.devices_base import *
from base_aux.testplans.devices_kit import DeviceKit


# =====================================================================================================================
class Test__DeviceBase:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = type("Victim", (Base_Device,), {})

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

        # victim = self.Victim(2)
        # assert victim.INDEX == 2


# =====================================================================================================================
@pytest.mark.skip    # FIXME: ref or not!
class Test__DevicesLines:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass
        self.Victim: DeviceKit = type("Victim", (DeviceKit,), {})

    def teardown_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__DUT_COUNT(self):
        # 1 -----------------------------------------------------
        self.Victim.COUNT = 1

        victim = self.Victim(DUT=TableLine(0))
        assert victim.DUT == self.Victim.DUT[0]

        # 2 ------------------------------------------------------
        self.Victim.COUNT = 2
        #
        # # INSTANCE ----------------------
        victim = self.Victim(0)
        assert victim.DUT.INDEX == 0
        assert victim.DUT == self.Victim.DUT[0]
        assert victim.DUT == victim.DUT[0]

        victim = self.Victim(1)
        assert victim.DUT.INDEX == 1
        assert victim.DUT == self.Victim.DUT[1]
        assert victim.DUT == victim.DUT[1]

        assert victim.DUT[0] != victim.DUT[1]
        assert self.Victim.DUT[0] != self.Victim.DUT[1]

    # -----------------------------------------------------------------------------------------------------------------
    def test__CLS_SINGLE__CLS(self):
        self.Victim.COUNT = 2
        self.Victim.ATC = Base_Device

        assert hasattr(self.Victim, "DUT") is True
        assert hasattr(self.Victim, "ATC") is False

        assert self.Victim["DUT"] is not None
        assert self.Victim["ATC"] is not None
        assert self.Victim["PTB"] is not None

        # DISCONNECT
        self.Victim.disconnect()

    def test__CLS_SINGLE__INSTANCE(self):
        self.Victim.COUNT = 2
        self.Victim.ATC = Base_Device

        victim = self.Victim(1)    # FIXME: IS IN BROKEN?????

        assert victim.DUT == victim.DUT[1]
        try:
            victim.PTB
        except:
            pass
        else:
            assert False

        assert hasattr(victim, "DUT") is True
        try:
            hasattr(victim, "ATC")
        except:
            pass
        else:
            assert False

        assert victim["DUT"] is not None
        assert victim["DUT"] is not None
        assert victim["PTB"] is not None

    # -----------------------------------------------------------------------------------------------------------------
    def test__CLS(self):
        self.Victim.COUNT = 2
        self.Victim.PTB = Base_Device

        assert hasattr(self.Victim, "DUT") is True
        assert hasattr(self.Victim, "PTB") is True

        assert len(self.Victim.DUT) == 2
        assert len(self.Victim.PTB) == 2

        assert self.Victim["DUT"] is not None
        assert self.Victim["ATC"] is not None
        assert self.Victim["PTB"] is not None

    def test__INSTANCE(self):
        self.Victim.COUNT = 2
        self.Victim.CLS_PTB = Base_Device

        victim = self.Victim(1)

        assert victim.DUT == victim.DUT[1]
        assert victim.PTB == victim.PTB[1]
        try:
            victim.ATC
        except:
            pass
        else:
            assert False

        assert hasattr(victim, "DUT") is True
        assert hasattr(victim, "TB") is True

        assert len(victim.DUT) == 2
        assert len(victim.PTB) == 2

        assert victim["DUT"] is not None
        assert victim["ATC"] is not None
        assert victim["PTB"] is not None

    # -----------------------------------------------------------------------------------------------------------------
    def test__double_init(self):
        # insts is the same!
        pass

    # def reconnect


# =====================================================================================================================
