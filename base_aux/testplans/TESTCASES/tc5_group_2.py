from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_base2_derivatives import *
from .tc0_groups import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "TcGroup_ATC220220 2"

    @classmethod
    @property
    def _EQ_CLS__VALUE(cls) -> Enum_TcGroup:
        return Enum_TcGroup.G3

    def startup__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return ValidSleep(1)


# =====================================================================================================================
