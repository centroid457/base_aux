from typing import *
from base_aux.testplans import TestCaseBase, TYPE__RESULT_W_EXX


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "test TC_inst startup fail"

    # RUN -------------------------------------------------------------------------------------------------------------
    def startup__wrapped(self) -> TYPE__RESULT_W_EXX:
        return False


# =====================================================================================================================
