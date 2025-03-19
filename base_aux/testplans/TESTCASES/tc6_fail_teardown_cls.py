from typing import *
from base_aux.testplans.main import TestCaseBase
from base_aux.testplans.tc_types import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "fail TeardownCls"

    # RUN -------------------------------------------------------------------------------------------------------------
    @classmethod
    def teardown__cls__wrapped(cls) -> TYPING__RESULT_W_EXX:
        return False


# =====================================================================================================================
