from typing import *

from .tc0__test_params import *


# =====================================================================================================================
class TestCase(Base_TcParams):
    ATC_VOUT: int = 260
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = True
    PTB_SET_PSON: bool = True

    _DESCRIPTION = "\nграница включения - верхняя (OFF)"


# =====================================================================================================================
