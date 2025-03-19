import time

from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_base2_derivatives import *

from .tc0_groups import *


# =====================================================================================================================
class TestCase(TcGroup_ATC220220, TestCaseBase):
    ASYNC = True
    DESCRIPTION = "atc"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        return True
        result_chain = ValidChains(
            [
                Valid(value_link=hasattr(cls, "DEVICES__BREEDER_CLS"), name="hasattr DEVICES__CLS"),
                Valid(value_link=hasattr(cls.DEVICES__BREEDER_CLS, "ATC"), name="hasattr ATC"),
                Valid(value_link=cls.DEVICES__BREEDER_CLS.ATC.connect, name="ATC.connect()"),
            ],
        )
        return result_chain

    def run__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return True
        time.sleep(0.1)
        result_chain = ValidChains(
            [
                Valid(value_link=self.DEVICES__BREEDER_INST.DUT.VALUE, name="DUT.VALUE"),
                Valid(value_link=self.DEVICES__BREEDER_INST.ATC.address__validate),
            ],
        )
        return result_chain


# =====================================================================================================================
