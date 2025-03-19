from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_base2_derivatives import *
from base_aux.valid.m3_valid_chains import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "test TC_inst startup fail"

    # RUN -------------------------------------------------------------------------------------------------------------
    def startup__wrapped(self) -> TYPING__RESULT_W_EXX:
        return False


# =====================================================================================================================
