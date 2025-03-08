import pytest

from base_aux.buses.m1_serial2_client_derivatives import *


# =====================================================================================================================
# @pytest.mark.skip
class Test__Shorted_validateModel_InfinitRW:
    """
    VALIDATE ADAPTERS fro DECODУ ERRORS
    """
    Victim: type[SerialClient_FirstFree_Shorted] = SerialClient_FirstFree_Shorted
    victim: SerialClient_FirstFree_Shorted

    # @classmethod
    # def setup_class(cls):
    #     pass
    #
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
    @pytest.mark.skip
    def test__shorted(self):
        """
        connect shorted port and start this code!
        wait for first error and see the step number
        write as result in SerialClient docstring
        """
        # PREPARE ------------------------
        self.Victim.BAUDRATE = 115200
        self.victim = self.Victim()
        self.victim.test__shorted()

    @pytest.mark.skip
    def test__real_device(self):    # TODO: fix it!!!
        """
        in case of validate real device like ATC/PTB
        DONT FORGET TO CHANGE address__validate for your device!!!
        """
        # PREPARE ------------------------
        VALIDATION_CMD, VALIDATION_ANSWER = ("GET NAME", "ATC 03")

        class Victim(SerialClient_FirstFree_Shorted):
            def address__validate(self) -> bool:
                return self.write_read__last_validate(*VALIDATION_CMD)

        self.victim = Victim()
        if not self.victim.connect():
            msg = f"[ERROR] not found PORT validated"
            print(msg)
            raise Exception(msg)

        # START WORKING ------------------
        index = 0
        while True:
            index += 1
            load = f"step{index}"
            print(load)
            assert self.victim.address__validate() is True


# =====================================================================================================================
if __name__ == "__main__":
    Test__Shorted_validateModel_InfinitRW().test__shorted()


# =====================================================================================================================
