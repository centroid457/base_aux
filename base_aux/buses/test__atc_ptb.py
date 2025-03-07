import pytest

from base_aux.buses.m1_serial1_client import *
from base_aux.buses.m1_serial2_client_derivatives import *


# =====================================================================================================================
@pytest.mark.skip
class Test__ATC:
    victim: SerialClient

    @classmethod
    def setup_class(cls):
        pass

        class Atc_SerialClient(SerialClient_FirstFree_AnswerValid):
            LOG_ENABLE = True
            RAISE_CONNECT = False
            BAUDRATE = 115200

            # # ATC ----------------------------
            PREFIX = "ATC:03:"
            EOL__SEND = b"\r"

            def address__validate(self) -> bool:
                return self.write_read__last_validate("get name", "ATC 03")

        cls.victim = Atc_SerialClient()

    # @classmethod
    # def teardown_class(cls):
    #     if cls.victim:
    #         cls.victim.disconnect()
    #
    # def setup_method(self, method):
    #     pass

    def teardown_method(self, method):
        pass
        if self.victim:
            self.victim.disconnect()

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        assert self.victim.connect()
        print(f"{self.victim.connect()=}")
        # print(f"{self.victim.addresses_system__detect()=}")
        print(f"{self.victim.ADDRESS=}")
        assert self.victim.address_check__resolved()


# =====================================================================================================================
@pytest.mark.skip
class Test__PTB(Test__ATC):
    @classmethod
    def setup_class(cls):
        pass

        class Ptb_SerialClient(SerialClient_FirstFree_AnswerValid):
            LOG_ENABLE = True
            RAISE_CONNECT = False
            BAUDRATE = 115200

            # PTB ----------------------------
            PREFIX = "PTB:01:"
            EOL__SEND = b"\n"

            def address__validate(self) -> bool:
                return self.write_read__last_validate("get name", "PTB") and self.write_read__last_validate("get addr", "01")

        cls.victim = Ptb_SerialClient()


# =====================================================================================================================
