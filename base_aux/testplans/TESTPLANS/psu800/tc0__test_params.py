from typing import *

from .tc0__base import *


# =====================================================================================================================
class Base_TcParams(Base_TcPsu):
    ATC_VOUT: int | None = 0
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = False
    PTB_SET_PSON: bool = False

    _DESCRIPTION = "[base] for testing params in different states"

    # -----------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXX:
        result_chain = ValidChains(
            chains=self.steps__check_params()
        )
        return result_chain


# =====================================================================================================================
