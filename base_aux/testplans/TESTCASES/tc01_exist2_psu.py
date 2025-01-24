from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_base2_derivatives import *
from base_aux.valid.m3_valid_chains import *


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
