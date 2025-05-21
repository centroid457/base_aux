from typing import *

from base_aux.testplans.devices import *
from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
class Base_TpItem:
    NAME: str = "[DEF] STAND NAME"
    DESCRIPTION: str = "[DEF] STAND DESCRIPTION"
    SN: str = "[DEF] STAND SN"

    DEV_LINES: DeviceKit
    TCS_CLS: dict[type, bool]   # TODO: use TableLine??? - NO! KEEP DICT! with value like USING! so we can use one


# =====================================================================================================================
# if __name__ == "__main__":
#     print(load__tcs())


# =====================================================================================================================
