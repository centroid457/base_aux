from typing import *
from base_aux.testplans.devices import *
from base_aux.buses.m1_serial2_client_derivatives import *
from base_aux.aux_cmp_eq.m3_eq_valid3_derivatives import *


# =====================================================================================================================
class Device(SerialClient_FirstFree_AnswerValid, Base_Device):
    LOG_ENABLE = True
    RAISE_CONNECT = False
    BAUDRATE = 115200
    EOL__SEND = b"\n"

    REWRITEIF_READNOANSWER = 0
    REWRITEIF_NOVALID = 0

    # MODEL INFO --------------------------------
    __sn_start: str = "SN"

    NAME: str = "PTB"
    DESCRIPTION: str = "PTB for PSU"

    # @property
    # def DUT_SN(self) -> str:      # TODO: USE DIRECT FINDING!!!???
    #     return f"SN_{self.INDEX}"

    def __init__(self, index: int = None, **kwargs):    # FIXME: decide to delete this!!!
        """
        :param index: None is only for SINGLE!
        """
        if index is not None:
            self.INDEX = index
        super().__init__(**kwargs)

    # MODEL INFO --------------------------------
    def load__INFO(self) -> None:
        pass

        if not self.SN:
            self.SN = self.write_read__last("get SN")

        if not self.FW:
            self.FW = self.write_read__last("get FW")

        if not self.MODEL:
            self.MODEL = self.write_read__last("get MODEL")

    # DETECT --------------------------------
    @property
    def DEV_FOUND(self) -> bool:
        return self.address_check__resolved()

    @property
    def PREFIX(self) -> str:
        return f"PTB:{self.INDEX+1:02d}:"

    def address__validate(self) -> bool:
        result = (
                self.write_read__last_validate("get name", self.NAME, prefix="*:")
                and
                self.write_read__last_validate("get addr", EqValid_NumParsedSingle(self.INDEX+1), prefix="*:")
                # and
                # self.write_read__last_validate("get prsnt", "0")
        )
        if result:
            self.load__INFO()

        return result

    def connect__validate(self) -> bool:
        result = (
            self.address_check__resolved()  # fixme: is it really need here???
            and
            self.write_read__last_validate("get prsnt", "1")
        )
        return result

    @property
    def VALUE(self) -> bool:
        return self.INDEX % 2 == 0


# =====================================================================================================================
class DeviceDummy(SerialClient_FirstFree_AnswerValid, Base_Device):
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
