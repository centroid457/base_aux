from typing import *
from base_aux.testplans.devices import DutBase
from base_aux.buses.m1_serial2_client_derivatives import *


# =====================================================================================================================
class Device(SerialClient_FirstFree_AnswerValid, DutBase):
    LOG_ENABLE = True
    RAISE_CONNECT = False
    BAUDRATE = 115200
    EOL__SEND = b"\n"

    REWRITEIF_READNOANSWER = 0
    REWRITEIF_NOVALID = 0

    # MODEL INFO --------------------------------
    __sn_start: str = "SN"
    NAME: str = "PSU"
    DESCRIPTION: str = "Power Supply Unit"

    @property
    def SN(self) -> str:
        return f"{self.__sn_start}_{self.INDEX+1}"

    @SN.setter
    def SN(self, value: Any) -> None:
        self.__sn_start = str(value).upper()
    # MODEL INFO --------------------------------

    @property
    def DEV_FOUND(self) -> bool:
        return True
        return self.address_check__resolved()

    @property
    def PREFIX(self) -> str:
        return f"PTB:{self.INDEX+1:02d}:"

    def address__validate(self) -> bool:
        return True
        result = (
                self.write_read__last_validate("get name", f"PTB", prefix="*:")
                and
                self.write_read__last_validate("get addr", [f"{self.INDEX+1}", f"0{self.INDEX+1}"], prefix="*:")
                # and
                # self.write_read__last_validate("get prsnt", "0")
        )
        return result

    def connect__validate(self) -> bool:
        return True
        result = (
                self.write_read__last_validate("get prsnt", "0")
        )
        return result

    def __init__(self, index: int, **kwargs):
        if index is not None:
            self.INDEX = index
        super().__init__(**kwargs)

    @property
    def VALUE(self) -> bool:
        return self.INDEX % 2 == 0

    def connect(self):
        return True


# =====================================================================================================================
if __name__ == "__main__":
    pass

    # emu = Ptb_Emulator()
    # emu.start()
    # emu.wait()

    dev = Device(1)
    print(f"{dev.connect()=}")
    print(f"{dev.ADDRESS=}")

    # dev.write_read__last("get sn")
    # dev.write_read__last("get fru")
    # dev.write_read__last("test sc12s")
    # dev.write_read__last("test ld12s")
    # dev.write_read__last("test gnd")
    # dev.write_read__last("test")
    # dev.write_read__last("get status")
    dev.write_read__last("get vin")


# =====================================================================================================================
