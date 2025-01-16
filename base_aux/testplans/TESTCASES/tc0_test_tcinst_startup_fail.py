from base_aux.testplans.tc import *
from base_aux.valid.valid_1_base_derivatives import *
from base_aux.valid.valid_10_chains import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "test TC_inst startup fail"

    # RUN -------------------------------------------------------------------------------------------------------------
    def startup__wrapped(self) -> TYPE__RESULT_W_EXX:
        return False


# =====================================================================================================================
