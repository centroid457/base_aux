import pytest

from base_aux.buses.serial_client import *
from base_aux.buses.serial_derivatives import *


# =====================================================================================================================
@pytest.mark.skipif(condition=not SerialClient.addresses_paired__detect(), reason="NO addresses_paired__detect====FIXME!!!")
class Test__Paired:
    Victim: type[SerialClient_FirstFree_Paired]
    victim: SerialClient_FirstFree_Paired

    SETUP_CLS__CONNECT: bool = False
    TEARDOWN__DISCONNECT: bool = True

    @classmethod
    def setup_class(cls):
        print(SerialClient_FirstFree_Paired.addresses_paired__detect())

        class Victim(SerialClient_FirstFree_Paired):
            LOG_ENABLE = True

            # def address__validate(self) -> Union[bool, NoReturn]:
            #     return self.write_read_line_last("echo") == "echo"

        cls.Victim = Victim
        cls.victim = cls.Victim()

        class Victim(SerialClient_FirstFree_Shorted):
            RAISE_CONNECT = False

        cls.Victim = Victim
        cls.victim = cls.Victim()
        if cls.SETUP_CLS__CONNECT and not cls.victim.connect():
            msg = f"[ERROR] not found PORTs PAIRED"
            print(msg)
            raise Exception(msg)

    @classmethod
    def teardown_class(cls):
        pass
        if hasattr(cls, "victim") and cls.victim:
            cls.victim._addresses__release()
            cls.victim.disconnect()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass
        if self.TEARDOWN__DISCONNECT and hasattr(self, "victim") and self.victim:
            self.victim._addresses__release()
            self.victim.disconnect()

    # -----------------------------------------------------------------------------------------------------------------
    def test__ADDRESS__PAIRED(self):
        # self.victim.disconnect()

        assert self.victim.addresses_paired__count() > 0    # HERE YOU NEED CONNECT/CREATE/COMMUTATE ONE PAIR!
        print(f"{self.victim.ADDRESSES__PAIRED=}")

        assert self.victim.connect() is True

        addr_paired = self.victim.address_paired__get()
        assert addr_paired is not None

        victim_pair = SerialClient()
        assert victim_pair.connect(address=addr_paired)

        assert self.victim._write("LOAD1")
        assert victim_pair.read_line() == "LOAD1"

        assert victim_pair._write("LOAD2")
        assert self.victim.read_line() == "LOAD2"


# =====================================================================================================================
