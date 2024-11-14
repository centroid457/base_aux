import pytest
from typing import *
from base_aux.bits import *


# =====================================================================================================================
class Test__Bitfield:
    VICTIM: type[Bitfield] = type("VICTIM", (Bitfield,), {})

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        self.VICTIM = type("VICTIM", (Bitfield,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__0_bits(self):
        try:
            self.VICTIM(0)
        except Exx_BitsNoSize:
            assert True
        else:
            assert False

    def test__1_bits(self):
        victim: Bitfield = self.VICTIM(1)
        assert victim.field_size == 1
        assert len(victim) == 1
        assert victim._field_bytearray == bytearray(1)

        # [0] -------------------------------------------
        victim[0] = 0

        assert victim[0] == 0
        assert victim.int() == 0
        assert victim.count_activated() == 0

        assert victim.field_str == "0"
        assert victim._bin_str() == "0"
        assert victim._hex_str() == "00"
        assert str(victim) == "field[0]"
        assert victim.size_get_active() == 0

        assert victim.list_bits() == [0, ]
        assert victim.list_activated_indexes() == []
        assert victim.list_activated_values() == []

        # [1] -------------------------------------------
        victim[0] = 1

        assert victim[0] == 1
        assert victim.int() == 1
        assert victim.count_activated() == 1

        assert victim.field_str == "1"
        assert victim._bin_str() == "1"
        assert victim._hex_str() == "01"
        assert str(victim) == "field[1]"
        assert victim.size_get_active() == 1

        assert victim.list_bits() == [1, ]
        assert victim.list_activated_indexes() == [0, ]
        assert victim.list_activated_values() == [1, ]

    def test__2_bits(self):
        victim: Bitfield = self.VICTIM(2)
        assert victim.field_size == 2
        assert len(victim) == 2
        assert victim._field_bytearray == bytearray(1)

        # [00] -------------------------------------------
        victim[0] = 0
        victim[1] = 0

        assert victim[0] == 0
        assert victim.int() == 0
        assert victim.count_activated() == 0

        assert victim.field_str == "00"
        assert victim._bin_str() == "00"
        assert victim._hex_str() == "00"
        assert str(victim) == "field[00]"
        assert victim.size_get_active() == 0

        assert victim.list_bits() == [0, 0, ]
        assert victim.list_activated_indexes() == []
        assert victim.list_activated_values() == []

        # [01] -------------------------------------------
        victim[0] = 1
        victim[1] = 0

        assert victim[0] == 1
        assert victim.int() == 1
        assert victim.count_activated() == 1

        assert victim.field_str == "01"
        assert victim._bin_str() == "01"
        assert victim._hex_str() == "01"
        assert str(victim) == "field[01]"
        assert victim.size_get_active() == 1

        assert victim.list_bits() == [0, 1, ]
        assert victim.list_activated_indexes() == [0, ]
        assert victim.list_activated_values() == [1, ]

        # [10] -------------------------------------------
        victim[0] = 0
        victim[1] = 1

        assert victim[0] == 0
        assert victim[1] == 1
        assert victim.int() == 2
        assert victim.count_activated() == 1

        assert victim.field_str == "10"
        assert victim._bin_str() == "10"
        assert victim._hex_str() == "02"
        assert str(victim) == "field[10]"
        assert victim.size_get_active() == 2

        assert victim.list_bits() == [1, 0, ]
        assert victim.list_activated_indexes() == [1, ]
        assert victim.list_activated_values() == [2, ]

    def test__index(self):
        pass


# =====================================================================================================================
