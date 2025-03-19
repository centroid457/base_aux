from base_aux.testplans.tc import *
from base_aux.valid.m3_valid_chains import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "PTB exist"

    # RUN -------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXX:
        result = Valid(
            value_link=self.DEVICES__BREEDER_INST.DUT.address_check__resolved,
            name="DUT.address_check__resolved"
        )
        return result


# =====================================================================================================================
