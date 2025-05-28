from typing import *
import time

from base_aux.testplans.devices import *
from base_aux.buses.m1_serial2_client_derivatives import *


# =====================================================================================================================
class Device(SerialClient_FirstFree_AnswerValid, Base_Device):  # IMPORTANT! KEEP Serial FIRST Nesting!
    LOG_ENABLE = True
    RAISE_CONNECT = False
    BAUDRATE = 115200
    PREFIX = "ATC:03:"
    EOL__SEND = b"\n"

    REWRITEIF_READNOANSWER = 0
    REWRITEIF_NOVALID = 0

    NAME = "ATC"
    DESCRIPTION: str = "ATC for PSU"

    # def address__validate(self) -> bool:  # NO NEED!
    #     return  self.write_read__last_validate("get name", self.NAME, prefix=self.PREFIX)

    def __init__(self, index: int = None, **kwargs):    # FIXME: decide to delete this!!!
        """
        :param index: None is only for SINGLE!
        """
        if index is not None:
            self.INDEX = index
        super().__init__(**kwargs)

    def dev__load_info(self) -> None:
        if not self.SN:
            self.SN = self.write_read__last("get SN")
            self.FW = self.write_read__last("get FW")
            self.MODEL = self.write_read__last("get MODEL")

    def connect__validate(self) -> bool:
        result = (
            self.address_check__resolved()  # fixme: is it really need here???
        )
        if result:
            self.dev__load_info()

        return result

    # DETECT --------------------------------
    @property
    def DEV_FOUND(self) -> bool:
        return self.address_check__resolved()


# =====================================================================================================================
class DeviceDummy(SerialClient_FirstFree_AnswerValid, Base_Device):  # IMPORTANT! KEEP Serial FIRST Nesting!
    @property
    def DEV_FOUND(self) -> bool:
        return True

    def address__validate(self) -> bool:
        return True

    def connect__validate(self) -> bool:
        return True

    def connect(self, *args, **kwargs) -> bool:
        return True


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
