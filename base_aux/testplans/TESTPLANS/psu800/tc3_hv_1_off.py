from typing import *

from .tc0__base import *
from .tc0__test_params import *


# =====================================================================================================================
class TestCase(Base_TcParams):
    ATC_VOUT: int | None = 220
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = True
    PTB_SET_PSON: bool = False

    _DESCRIPTION = "\nпроверка значений параметров в ВЫКЛ состоянии"


# =====================================================================================================================
