from typing import *

from base_aux.testplans.devices import *


# =====================================================================================================================
class Base_TpItem:
    NAME: str
    DEV_LINES: DeviceKit
    TCS_CLS: dict[type, bool]   # TODO: use TableLine??? - NO! KEEP DICT! with value like USING! so we can use one


# =====================================================================================================================
# if __name__ == "__main__":
#     print(load__tcs())


# =====================================================================================================================
