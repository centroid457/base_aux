from . import atc, ptb
from base_aux.testplans.devices import DevicesBreeder_WithDut


# =====================================================================================================================
class DevicesBreeder__Example(DevicesBreeder_WithDut):
    COUNT = 2
    CLS_SINGLE__ATC = atc.Device
    CLS_LIST__DUT = ptb.Device
    # CLS_LIST__DUT = dut.Device


# =====================================================================================================================
