from base_aux.testplans.tc import *
from base_aux.valid.valid_1_base_derivatives import *
from base_aux.valid.valid_10_chains import *


# =====================================================================================================================
class TcGroup_ATC220220(TcGroup_Base):
    MIDDLE_GROUP__NAME = "ATC230220"

    # HERE ARE PLACE CLSMETHs
    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

    @classmethod
    def teardown__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

# =====================================================================================================================
