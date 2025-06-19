from typing import *

from .tc0__base import *


# =====================================================================================================================
class TestCase(Base_TcAtcPtb):
    ATC_VOUT: int | None = 220
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = True
    PTB_SET_PSON: bool = True

    ASYNC = True
    _DESCRIPTION = "тест нагрузочный\nшины главного питания (MAIN)"

    def _gen_chains(self, load: int) -> list[Valid]:
        return [
            ValidFailStop(
                value_link=self.DEV_COLUMN.DUT.SET,
                kwargs__value={"LOAD": load},
                validate_link="OK",
                name="SET",
            ),
            ValidSleep(1),
            ValidNoCum(
                value_link=self.DEV_COLUMN.DUT.GET,
                args__value="VINOK",
                validate_link=1,
            ),
            ValidNoCum(
                value_link=self.DEV_COLUMN.DUT.GET,
                args__value="PWOK",
                validate_link=1,
            ),
            ValidNoCum(
                value_link=self.DEV_COLUMN.DUT.GET,
                args__value="V12S",
                validate_link=EqValid_LGTE_NumParsedSingle(ge=11, le=13).resolve,
                name="GET+valid diapason",
            ),
            ValidNoCum(
                value_link=self.DEV_COLUMN.DUT.GET,
                args__value="V12M",
                validate_link=EqValid_LGTE_NumParsedSingle(ge=11, le=13).resolve,
                name="GET+valid diapason",
            ),
            ValidNoCum(
                value_link=self.DEV_COLUMN.DUT.GET,
                args__value="IOUT",
                validate_link=EqValid_LGTE_NumParsedSingle(ge=load / 12 / 2).resolve,
                name="GET+valid diapason",
            ),
            ValidNoCum(
                value_link=self.DEV_COLUMN.DUT.GET,
                args__value="IIN",
                validate_link=EqValid_LGTE_NumParsedSingle(ge=load / 12 / 2).resolve,
                name="GET+valid diapason",
            ),
        ]

    # -----------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXX:
        result_chain = ValidChains(
            chains=[
                *self._gen_chains(0),
                *self._gen_chains(100),
                *self._gen_chains(300),
                *self._gen_chains(400),
                *self._gen_chains(800),

                *self._gen_chains(0),
                *self._gen_chains(800),
            ]
        )
        return result_chain


# =====================================================================================================================
