from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_derivatives import *
from .tc0_groups import *


# =====================================================================================================================
class TestCase(Base_TestCase):
    ASYNC = True
    DESCRIPTION = "TcGroup_ATC220220 1"

    @classmethod
    @property
    def _EQ_CLS__VALUE(cls) -> Enum_TcGroup:
        return Enum_TcGroup.G2

    def startup__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return ValidSleep(0.5)


# =====================================================================================================================
