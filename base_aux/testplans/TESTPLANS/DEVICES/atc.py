from typing import *
import time

from base_aux.testplans.devices_base import *
from base_aux.buses.m1_serial2_client_derivatives import *


# =====================================================================================================================
class Device(Base__DeviceUart_ETech):  # IMPORTANT! KEEP Serial FIRST Nesting!
    NAME = "ATC"
    DESCRIPTION: str = "ATC for PSU"


# =====================================================================================================================
class DeviceDummy(Device, Base_DeviceDummy):
    pass


# =====================================================================================================================
if __name__ == "__main__":
    # emu = Atc_Emulator()
    # emu.start()
    # emu.wait()

    dev = Device()
    print(f"=======before {dev.ADDRESS=}")
    print(f"{dev.addresses_system__detect()=}")
    print(f"{dev.connect()=}")
    print(f"{dev.connect__only_if_address_resolved()=}")
    print(f"{dev.addresses_system__detect()=}")
    print(f"=======after {dev.ADDRESS=}")
    exit()

    print(f'{dev.SET(V12="ON")=}')
    print(f'{dev.SET(VIN=230)=}')
    print(f'{dev.SET(VOUT=220)=}')
    time.sleep(0.3)
    print(f'{dev.reset()=}')

    # print(f"{dev.address__validate()=}")
    # print(f"{dev.address__validate()=}")
    # print(f"{dev.address__validate()=}")
    #
    # print(f"{dev.write_read_line_last('get name')=}")
    # print(f"{dev.write_read_line_last('get name')=}")
    # print(f"{dev.write_read_line_last('get name')=}")
    # print(f"{dev.write_read_line_last('get name')=}")
    # print(f"{dev.write_read_line_last('get name')=}")
    # print(f"{dev.disconnect()=}")
    print(f"{dev.ADDRESS=}")


# =====================================================================================================================
