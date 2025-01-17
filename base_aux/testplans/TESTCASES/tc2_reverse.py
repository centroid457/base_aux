from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_base2_derivatives import *
from base_aux.valid.m4_valid_chains import *

from . import tc1_direct
from .tc0_groups import *


# =====================================================================================================================
class TestCase(TcGroup_ATC220220, tc1_direct.TestCase):
    ASYNC = True
    DESCRIPTION = "reverse1"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
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
