from typing import *

from .tc0__base import *


# =====================================================================================================================
class TestCase(TestCaseBase_Psu):
    ATC_VOUT: int | None = 0
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = False
    PTB_SET_PSON: bool = False

    _DESCRIPTION = "присутствие БП"

    # -----------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXX:
        result = Valid(
            value_link=self.DEVICES__BREEDER_INST.DUT.GET,
            args__value="PRSNT",
            validate_link=1,
            name="GET",
        )
        return result


# =====================================================================================================================
