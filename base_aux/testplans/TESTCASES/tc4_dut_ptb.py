from base_aux.testplans.tc import *
from base_aux.valid.m3_valid_chains import *
from .tc0_groups import *


# =====================================================================================================================
class TestCase(Base_TestCase):
    ASYNC = True
    DESCRIPTION = "ptb"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        # return True
        result_chain = ValidChains(
            [
                Valid(value_link=hasattr(cls, "DEVICES__BREEDER_CLS"), name="hasattr DEVICES__CLS"),
                Valid(value_link=hasattr(cls.DEVICES__BREEDER_CLS, "ATC"), name="hasattr ATC"),
                Valid(value_link=cls.DEVICES__BREEDER_CLS.ATC.connect, name="ATC.connect()"),
            ],
        )
        return result_chain

    def startup__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        result = ValidChains(
            [
                Valid(value_link=self.DEVICES__BREEDER_INST.DUT.connect__only_if_address_resolved, name="DUT.connect__only_if_address_resolved"),
            ],
        )
        return result

    def run__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        # time.sleep(0.1)
        result = ValidChains(
            [
                Valid(value_link=self.DEVICES__BREEDER_INST.DUT.connect__only_if_address_resolved, name="DUT.connect__only_if_address_resolved"),
            ],
        )
        return result


# =====================================================================================================================
