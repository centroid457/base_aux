from .tc0_groups import TcGroup_ATC220220

from base_aux.testplans import *
from base_aux.funcs import *
from base_aux.classes import *

# =====================================================================================================================
class TestCase(TcGroup_ATC220220, TestCaseBase):
    ASYNC = True
    DESCRIPTION = "TcGroup_ATC220220 2"
    def startup__wrapped(self) -> TYPE__RESULT_W_NORETURN:
        return ValidSleep(1)


# =====================================================================================================================
