import time

from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_derivatives import *
from base_aux.valid.m3_valid_chains import *
from .tc0_groups import *


# =====================================================================================================================
class TestCase(Base_TestCase):
    ASYNC = True
    DESCRIPTION = "direct1"

    @classmethod
    @property
    def _EQ_CLS__VALUE(cls) -> Enum_TcGroup:
        return Enum_TcGroup.G1

    def run__wrapped(self):
        time.sleep(0.1)
        self.details_update({"detail_value": self.DEV_COLUMN.DUT.VALUE})
        result_chain = ValidChains(
            [
                Valid(value_link=True, name="TRUE"),
            ],
        )
        return result_chain


# =====================================================================================================================
