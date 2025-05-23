from typing import *

from base_aux.testplans.devices import *
from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
class Base_TpItem:
    NAME: str = "[DEF] STAND NAME"
    DESCRIPTION: str = "[DEF] STAND DESCRIPTION"
    SN: str = "[DEF] STAND SN"

    DEV_LINES: DeviceKit = {}

    # TCSc_LINE: dict[type, bool]   # TODO: use TableLine??? - NO! KEEP DICT! with value like USING! so we can use one
    TCSc_LINE: TableLine = TableLine()

    def __init__(self) -> None:
        # PREPARE CLSs ========================================
        for tc_cls in self.TCSc_LINE:
            # init TP_ITEM -----------------------------------
            tc_cls.TP_ITEM = self

            # gen INSTS -----------------------------------
            tcs_insts = []
            for index in range(self.DEV_LINES.COUNT_COLUMNS):
                tc_i = tc_cls(index=index)
                tcs_insts.append(tc_i)
            tc_cls.TCSi_LINE = TableLine(*tcs_insts)    # TODO: move into TC_CLS


# =====================================================================================================================
# if __name__ == "__main__":
#     print(load__tcs())


# =====================================================================================================================
