from typing import *

from .tc0__base import *


# =====================================================================================================================
class TestCase(Base_TcAtcPtb):
    ATC_VOUT: int | None = 0
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = False
    PTB_SET_PSON: bool = False

    _DESCRIPTION = "тест Заземления"

    # -----------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXC:
        result_chain = ValidChains(
            chains=[
                Valid(
                    value_link=self.DEV_COLUMN.DUT.TEST,
                    args__value="GND",
                    kwargs__value={"__timeout": 10},
                    validate_link="PASS",
                    name="TEST",
                ),
            ]
        )
        return result_chain


# =====================================================================================================================
