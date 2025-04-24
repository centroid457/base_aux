from typing import *

from .tc0__test_params import *


# =====================================================================================================================
class TestCase(TestParams_Base):
    ATC_VOUT: int = 150
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = True
    PTB_SET_PSON: bool = True

    _DESCRIPTION = "\nграница включения - нижняя (OFF)"


# =====================================================================================================================
