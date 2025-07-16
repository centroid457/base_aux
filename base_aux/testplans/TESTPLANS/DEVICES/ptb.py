from typing import *
from base_aux.testplans.devices_base import *
from base_aux.buses.m1_serial2_client_derivatives import *


# =====================================================================================================================
class Device(Base__DeviceUart_ETech):  # IMPORTANT! KEEP Serial FIRST Nesting!
    NAME: str = "PTB"
    DESCRIPTION: str = "PTB for PSU"

    def dev__load_info(self) -> None:
        if not self.SN:
            self.SN = self.write_read__last("get SN")
            self.FW = self.write_read__last("get FW")
            self.MODEL = self.write_read__last("get MODEL")

            self.DUT_SN = self.write_read__last("get PSSN")
            self.DUT_FW = self.write_read__last("get PSFW")
            self.DUT_MODEL = self.write_read__last("get PSMODEL")


# =====================================================================================================================
class DeviceDummy(Device, Base_DeviceDummy):
    pass


# =====================================================================================================================
def _explore():
    pass

    # emu = Ptb_Emulator()
    # emu.start()
    # emu.wait()

    dev = Device(0)
    print(f"{dev.connect()=}")
    print(f"{dev.ADDRESS=}")
    print(f"{dev.address_check__resolved()=}")

    if not dev.address_check__resolved():
        return

    # dev.write_read__last("get sn")
    # dev.write_read__last("get fru")
    # dev.write_read__last("test sc12s")
    # dev.write_read__last("test ld12s")
    # dev.write_read__last("test gnd")
    # dev.write_read__last("test")
    # dev.write_read__last("get status")
    # dev.write_read__last("get vin")


if __name__ == "__main__":
    _explore()


# =====================================================================================================================
