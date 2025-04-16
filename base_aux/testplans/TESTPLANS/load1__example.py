from typing import *

from base import Base_TpInput
from base_aux.testplans.devices import DevicesBreeder_WithDut

from DEVICES import atc, ptb

from Example import (
    tc1_direct,
    tc2_reverse,
)

# =====================================================================================================================
class DevicesBreeder__Example(DevicesBreeder_WithDut):
    COUNT = 2     # setup later???
    CLS_SINGLE__ATC = atc.Device
    CLS_LIST__DUT = ptb.Device
    # CLS_LIST__DUT = dut.Device


# =====================================================================================================================
class Tp_Example(Base_TpInput):
    NAME = "Example"
    DEVS = DevicesBreeder__Example
    TCS_CLS = {
        tc1_direct.TestCase,
        tc2_reverse.TestCase,
    }


# =====================================================================================================================
if __name__ == "__main__":
    print()
    for item in Tp_Example.TCS_CLS:
        print(item)


# =====================================================================================================================
