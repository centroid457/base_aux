from typing import *
from base_aux.testplans import TestCaseBase, TYPE__RESULT_W_EXX
from base_aux.classes import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "fail TeardownCls"

    # RUN -------------------------------------------------------------------------------------------------------------
    @classmethod
    def teardown__cls__wrapped(self) -> TYPE__RESULT_W_EXX:
        return False


# =====================================================================================================================