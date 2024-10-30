from typing import *
from testplans import TestCaseBase, TYPE__RESULT_W_EXX
from funcs_aux import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "PSU exist"

    # RUN -------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPE__RESULT_W_EXX:
        result = Valid(
            value_link=self.DEVICES__BREEDER_INST.DUT.connect,
            # args__value="get PRSNT",
        )
        return result


# =====================================================================================================================
