from typing import *

from .tc0__base import *


# =====================================================================================================================
class TestCase(Base_TcPsu):
    ATC_VOUT: int | None = 220
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = True
    PTB_SET_PSON: bool = True

    _DESCRIPTION = "тест КЗ\nшины главного питания (MAIN)"

    # -----------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXX:
        result_chain = ValidChains(
            chains=[
                ValidNoCum(
                    value_link=self.DEVICES__BREEDER_INST.DUT.GET,
                    args__value="V12S",
                    validate_link=EqValid_LeGe_NumParsedSingle(11, 13).validate,
                    name="GET+valid diapason",
                ),
                ValidFailContinue(
                    value_link=self.DEVICES__BREEDER_INST.DUT.TEST,
                    args__value="SC12M",
                    kwargs__value={"__timeout": 40},
                    validate_link="PASS",
                    name="TEST",
                ),
                ValidSleep(1),
                ValidNoCum(
                    value_link=self.DEVICES__BREEDER_INST.DUT.GET,
                    args__value="V12S",
                    validate_link=EqValid_LeGe_NumParsedSingle(11, 13).validate,
                    name="GET+valid diapason",
                ),
            ]
        )
        return result_chain


# =====================================================================================================================
