import time

from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_base2_derivatives import *
from base_aux.valid.m3_valid_chains import *
from .tc0_groups import *


# =====================================================================================================================
class TestCase(Base_TestCase):
    ASYNC = True
    DESCRIPTION = "PTB exist"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        time.sleep(0.5)
        return True

    @classmethod
    def teardown__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        time.sleep(0.5)
        return True

    # RUN -------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXX:
        result = ValidChains([
            time.sleep(1),
            Valid(
                value_link=self.DEV_COLUMN.DUT.address_check__resolved,
                name="DUT.address_check__resolved",
            ),
        ])
        return result


# =====================================================================================================================
