from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_derivatives import *
from base_aux.valid.m3_valid_chains import *
from .tc0_groups import *


# =====================================================================================================================
class TestCase(Base_TestCase):
    ASYNC = True
    DESCRIPTION = "PSU exist"

    # RUN -------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXX:
        result = ValidChains([
            time.sleep(1),
            Valid(
                value_link=self.DEV_COLUMN.DUT.connect,
                # args__value="get PRSNT",
            ),
        ])
        return result

# =====================================================================================================================
