import pytest
from typing import *
from base_aux.pyqt import *


# =====================================================================================================================
@pytest.mark.skipif(condition=True, reason="in CICD will not work! just hide (or set False) for manual start!")
class Test__Gui:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        self.VICTIM = type("VICTIM", (Gui,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__START_GUI(self):
        class Gui_1(Gui):
            TITLE = "[GUI] TEST"
            # SIZE = (300, 100)

        with pytest.raises(SystemExit) as exx:
            Gui_1()
        assert exx.type == SystemExit
        assert exx.value.code == 0


# =====================================================================================================================
