from base_aux.valid.m2_valid_base2_derivatives import *
from base_aux.testplans.tc import *
from .tc0_groups import *


# =====================================================================================================================
class TestCase(Base_TestCase):
    ASYNC = True
    DESCRIPTION = "TcGroup_ATC220220 3"

    @classmethod
    @property
    def _EQ_CLS__VALUE(cls) -> Enum_TcGroup:
        return Enum_TcGroup.G4

    def startup__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return ValidSleep(1)


# =====================================================================================================================
