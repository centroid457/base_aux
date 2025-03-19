from base_aux.valid.m3_valid_chains import *
from base_aux.testplans.tc import *

from . import tc1_direct


# =====================================================================================================================
class TestCase(tc1_direct.TestCase):
    ASYNC = True
    DESCRIPTION = "reverse1"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        result_chain = ValidChains(
            [
                Valid(value_link=True, name="TRUE"),
                Valid(value_link=False, name="FALSE"),
                Valid(value_link=None, name="NONE"),
            ],
        )
        return result_chain

    def run__wrapped(self) -> bool:
        time.sleep(0.1)
        self.details_update({"detail_value": not self.DEVICES__BREEDER_INST.DUT.VALUE})
        return not self.DEVICES__BREEDER_INST.DUT.VALUE


# =====================================================================================================================
