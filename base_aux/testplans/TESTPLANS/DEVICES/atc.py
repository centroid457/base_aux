from typing import *
from base_aux.buses.m1_serial2_client_derivatives import *


# =====================================================================================================================
class Device(SerialClient_FirstFree_AnswerValid):
    LOG_ENABLE = True
    RAISE_CONNECT = False
    BAUDRATE = 115200
    PREFIX = "ATC:03:"
    EOL__SEND = b"\n"

    REWRITEIF_READNOANSWER = 0
    REWRITEIF_NOVALID = 0

    def address__validate(self) -> bool:
        for _ in range(2):
            if self.write_read__last_validate("get name", "ATC", prefix=self.PREFIX):
                return True

# =====================================================================================================================
if __name__ == "__main__":
    pass

    # emu = Atc_Emulator()
    # emu.start()
    # emu.wait()

    dev = Device()
    print(f"{dev.connect()=}")
    # print(f"{dev.addresses_system__detect()=}")
    print(f"{dev.ADDRESS=}")
    #
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
    # print(f"{dev.ADDRESS=}")


# =====================================================================================================================
