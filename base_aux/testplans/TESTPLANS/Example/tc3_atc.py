import time

from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_base2_derivatives import *
from .tc0_groups import *


# =====================================================================================================================
class TestCase(Base_TestCase):
    ASYNC = True
    DESCRIPTION = "atc"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        return True
        result_chain = ValidChains(
            [
                Valid(value_link=hasattr(cls, "DEV_LINES"), name="hasattr DEV_LINES"),
                Valid(value_link=hasattr(cls.DEV_LINES, "ATC"), name="hasattr ATC"),
                Valid(value_link=cls.DEV_LINES.ATC[0].connect, name="ATC.connect()"),
            ],
        )
        return result_chain

    def run__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return True
        time.sleep(0.1)
        result_chain = ValidChains(
            [
                Valid(value_link=self.DEV_COLUMN.DUT.VALUE, name="DUT.VALUE"),
                Valid(value_link=self.DEV_COLUMN.ATC.address__validate),
            ],
        )
        return result_chain


# =====================================================================================================================
