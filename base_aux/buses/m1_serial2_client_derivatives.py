from typing import *

from base_aux.buses.m1_serial1_client import SerialClient, Enum__AddressAutoAcceptVariant
from base_aux.buses.m1_serial3_server import SerialServer_Base, SerialServer_Example


# =====================================================================================================================
class SerialClient_FirstFree(SerialClient):
    _ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE

    def address_forget(self) -> None:
        """
        see BaseCls!
        """
        self.ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE

class SerialClient_FirstFree_Shorted(SerialClient):
    _ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE__SHORTED

    def address_forget(self) -> None:
        """
        see BaseCls!
        """
        self.ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE__SHORTED


class SerialClient_FirstFree_Paired(SerialClient):
    _ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE__PAIRED

    def address_forget(self) -> None:
        """
        see BaseCls!
        """
        self.ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE__PAIRED


class SerialClient_FirstFree_AnswerValid(SerialClient):
    _ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID

    def address_forget(self) -> None:
        """
        see BaseCls!
        """
        self.ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID


# =====================================================================================================================
class SerialClient_Emulated(SerialClient_FirstFree_Paired):
    _EMULATOR__CLS = SerialServer_Example
    _EMULATOR__START = True


# =====================================================================================================================
if __name__ == '__main__':
    victim = SerialClient_FirstFree_Shorted()
    victim.connect()


# =====================================================================================================================
