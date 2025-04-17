from typing import *
from base_aux.testplans.tp_manager import Base_TestCase
from base_aux.testplans.tc_types import *
from .tc0_groups import *


# =====================================================================================================================
class TestCase(Base_TestCase):
    ASYNC = True
    DESCRIPTION = "fail TeardownCls"

    @classmethod
    @property
    def _EQ_CLS__VALUE(cls) -> Enum_TcGroup:
        return Enum_TcGroup.G1

    # RUN -------------------------------------------------------------------------------------------------------------
    @classmethod
    def teardown__cls__wrapped(cls) -> TYPING__RESULT_W_EXX:
        return False


# =====================================================================================================================
