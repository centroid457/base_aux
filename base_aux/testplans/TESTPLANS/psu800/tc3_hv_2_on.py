from typing import *

from .tc0__base import *


# =====================================================================================================================
class TestCase(Base_TcAtcPtb):
    ATC_VOUT: int | None = 220
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = True
    PTB_SET_PSON: bool = True

    _DESCRIPTION = "\nпроверка значений параметров во ВКЛ состоянии"


# =====================================================================================================================
