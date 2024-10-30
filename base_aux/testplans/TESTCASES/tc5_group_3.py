from testplans import *
from funcs_aux import *
from .tc0_groups import TcGroup_ATC220220

from testplans import TYPE__RESULT_W_NORETURN


# =====================================================================================================================
class TestCase(TcGroup_ATC220220, TestCaseBase):
    ASYNC = True
    DESCRIPTION = "TcGroup_ATC220220 3"
    def startup__wrapped(self) -> TYPE__RESULT_W_NORETURN:
        return ValidSleep(1)


# =====================================================================================================================
