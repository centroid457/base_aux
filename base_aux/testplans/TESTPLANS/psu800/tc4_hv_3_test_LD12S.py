from typing import *

from .tc0__base import *


# =====================================================================================================================
class TestCase(Base_TcAtcPtb):
    ATC_VOUT: int | None = 220
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = True
    PTB_SET_PSON: bool = True

    _DESCRIPTION = "тест нагрузочный\nшины ожидания (STANDBY)"

    # -----------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXX:
        result_chain = ValidChains(
            chains=[
                ValidNoCum(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="V12S",
                    validate_link=EqValid_LGTE_NumParsedSingle(ge=11, le=13).resolve,
                    name="GET+valid diapason",
                ),
                ValidFailContinue(
                    value_link=self.DEV_COLUMN.DUT.TEST,
                    args__value="LD12S",
                    kwargs__value={"__timeout": 20},
                    validate_link="PASS",
                    name="TEST",
                ),
                ValidSleep(1),
                ValidNoCum(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="V12S",
                    validate_link=EqValid_LGTE_NumParsedSingle(ge=11, le=13).resolve,
                    name="GET+valid diapason",
                ),
            ]
        )
        return result_chain


# =====================================================================================================================
