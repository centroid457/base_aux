from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_base2_derivatives import *

from .tc0_groups import TcGroup_ATC220220


# =====================================================================================================================
class TestCase(TcGroup_ATC220220, TestCaseBase):
    ASYNC = True
    DESCRIPTION = "TcGroup_ATC220220 1"

    def startup__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return ValidSleep(0.5)


# =====================================================================================================================
