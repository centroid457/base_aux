import time

from base_aux.testplans.tc import *
from base_aux.valid.valid_1_base_derivatives import *
from base_aux.valid.valid_10_chains import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "direct1"

    def run__wrapped(self):
        time.sleep(0.1)
        self.details_update({"detail_value": self.DEVICES__BREEDER_INST.DUT.VALUE})
        result_chain = ValidChains(
            [
                Valid(value_link=True, name="TRUE"),
            ],
        )
        return result_chain


# =====================================================================================================================
