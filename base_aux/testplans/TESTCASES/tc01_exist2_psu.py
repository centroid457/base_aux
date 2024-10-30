from typing import *
from base_aux.testplans import TestCaseBase, TYPE__RESULT_W_EXX
from base_aux.classes import *


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
