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
                Valid(value_link=hasattr(cls, "TP_ITEM"), name="hasattr TP_ITEM"),
                Valid(value_link=hasattr(cls.TP_ITEM, "DEV_LINES"), name="hasattr DEV_LINES"),
                Valid(value_link=hasattr(cls.TP_ITEM.DEV_LINES, "ATC"), name="hasattr ATC"),
                Valid(value_link=cls.TP_ITEM.DEV_LINES.ATC[0].connect, name="ATC.connect()"),
            ],
        )
        return result_chain

    def startup__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        result = ValidChains(
            [
                Valid(value_link=self.DEV_COLUMN.DUT.connect__only_if_address_resolved, name="DUT.connect__only_if_address_resolved"),
            ],
        )
        return result

    def run__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        # time.sleep(0.1)
        result = ValidChains(
            [
                Valid(value_link=self.DEV_COLUMN.DUT.connect__only_if_address_resolved, name="DUT.connect__only_if_address_resolved"),
            ],
        )
        return result


# =====================================================================================================================
