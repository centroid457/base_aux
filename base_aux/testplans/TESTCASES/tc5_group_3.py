from .tc0_groups import TcGroup_ATC220220

from base_aux.valid.valid_1_base_derivatives import *
from base_aux.testplans.main import TestCaseBase
from base_aux.testplans.tc_types import TYPE__RESULT_W_EXX, TYPE__RESULT_W_NORETURN




# =====================================================================================================================
class TestCase(TcGroup_ATC220220, TestCaseBase):
    ASYNC = True
    DESCRIPTION = "TcGroup_ATC220220 3"

    def startup__wrapped(self) -> TYPE__RESULT_W_NORETURN:
        return ValidSleep(1)


# =====================================================================================================================
