from base_aux.testplans.devices_base import *
from base_aux.testplans.tc import *


# =====================================================================================================================
class Victim_DevicesLines(DeviceKit):
    ATC: TableLine = TableLine(Base_Device)


# =====================================================================================================================
@pytest.mark.skip    # FIXME: ref or not!
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
        assert len(self.Victim.TCSi_LINE) == 0
        assert self.Victim.STAND.DEV_LINES is None

        assert self.Victim.result__startup_cls is None
        assert self.Victim.result__teardown_cls is None

        # EXISTS IN INSTANCE --------------
        assert not hasattr(self.Victim, "INDEX")
        # assert not hasattr(self.Victim, "SETTINGS")
        assert hasattr(self.Victim, "DEV_COLUMN")

        assert not hasattr(self.Victim, "details")
        assert not hasattr(self.Victim, "exc")

    def test__cls__devices_apply__NONE(self):
        assert len(self.Victim.TCSi_LINE) == 0

        # EXISTS IN CLS --------------
        assert self.Victim.STAND.DEV_LINES is None

        assert self.Victim.result__startup_cls is None
        assert self.Victim.result__teardown_cls is None

        # EXISTS IN INSTANCE --------------
        assert not hasattr(self.Victim, "INDEX")
        # assert not hasattr(self.Victim, "SETTINGS")
        assert hasattr(self.Victim, "DEV_COLUMN")

        assert not hasattr(self.Victim, "details")
        assert not hasattr(self.Victim, "exc")

    def test__cls__devices_apply__example(self):
        assert len(self.Victim.TCSi_LINE) == 0
        self.Victim.STAND.DEV_LINES = Victim_DevicesLines()

        # EXISTS IN CLS --------------
        assert self.Victim.STAND.DEV_LINES is not None

        assert self.Victim.result__startup_cls is None
        assert self.Victim.result__teardown_cls is None

        # EXISTS IN INSTANCE --------------
        assert not hasattr(self.Victim, "INDEX")
        # assert not hasattr(self.Victim, "SETTINGS")
        assert hasattr(self.Victim, "DEV_COLUMN")

        assert not hasattr(self.Victim, "details")
        assert not hasattr(self.Victim, "exc")

    # -----------------------------------------------------------------------------------------------------------------
    def test__inst(self):
        self.Victim.STAND.DEV_LINES = Victim_DevicesLines()

        # EXISTS IN CLS --------------
        assert len(self.Victim.TCSi_LINE) == self.Victim.STAND.DEV_LINES.COUNT_COLUMNS

        # assert self.Victim(0) is self.Victim.TCSi_LINE[0]


        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!


# =====================================================================================================================
