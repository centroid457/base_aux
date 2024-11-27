from typing import *
from base_aux.testplans import TestCaseBase, TYPE__RESULT_W_EXX
from base_aux.valid import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "fail TeardownCls"

    # RUN -------------------------------------------------------------------------------------------------------------
    @classmethod
    def teardown__cls__wrapped(cls) -> TYPE__RESULT_W_EXX:
        return False


# =====================================================================================================================
