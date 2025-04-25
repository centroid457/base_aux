from typing import *

from .tc0__base import *


# =====================================================================================================================
class TestCase(Base_TcAtcPtb):
    ATC_VOUT: int | None = 0
    PTB_SET_EXTON: bool = True
    PTB_SET_HVON: bool = False
    PTB_SET_PSON: bool = False

    _DESCRIPTION = "тест PmBus"

    # -----------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXX:
        result_chain = ValidChains(
            chains=[
                ValidNoCum(
                    value_link=self.DEVICES__BREEDER_INST.DUT.TEST,
                    args__value="PMBUS",
                    kwargs__value={"__timeout": 10},
                    validate_link="PASS",
                    name="TEST",
                ),
            ]
        )
        return result_chain


# =====================================================================================================================
