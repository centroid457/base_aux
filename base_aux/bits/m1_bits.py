from typing import *

from base_aux.base_statics.m2_exceptions import *


# =====================================================================================================================
# TODO: need decision about flags order!!! NEED HUMAN ALWAYS except hex!!!
"""
work with bits (bitfields/flags/bites...)
designed for common work with bitfields-like aux_types
field_bytearray
flags/flags manipulate
bits/bit user/bit work/bits manipulate
"""


# =====================================================================================================================
class Bitfield:
    """
    IMPORTANT: ORDER for any field is NO HUMAN!!! or not???
    YOU NEED TO SEE ALWAYS AS REVERSE IN ANY REPRESENTATION!!!
    but when you indexind by obj[] used human order!!!
    """
    field_size: int = None
    _field_bytearray: bytearray = None

    def __init__(self, field_size: int):
        if field_size < 1:
            raise Exx__Incompatible(f"{field_size=}")

        self.field_size = field_size
        self._field_bytearray = bytearray((field_size + 7) // 8)

    # todo: clear_all+exact+several/setup_all+exact+several/ [by_pos/by_fields]
    # todo: listActiveFlags/list+iter [by_pos/by_fields]

    @classmethod
    def create_from_int(cls, flags: int, field_size: Optional[int] = None) -> 'Bitfield':
        raise NotImplemented
    # todo: FINISH!
    # todo: FINISH!
    # todo: FINISH!
    # todo: FINISH!
    # todo: FINISH!
    # todo: FINISH!
    # todo: FINISH!
    # todo: FINISH!

    def size_get_active(self) -> int:
        """get position of major valued flag
        """
        result = 0
        for pos, value in enumerate(self.list_bits()[::-1], start=1):
            if value == 1:
                result = pos
        return result

    @property
    def field_str(self) -> str:
        """in NOhuman order"""
        return "".join(map(str, self.list_bits()))

    def __getitem__(self, idx: int) -> Union[int, NoReturn]:
        if idx < -self.field_size or idx > self.field_size - 1:
            raise Exx__Addressing
        return self._field_bytearray[idx // 8] >> (idx % 8) & 1

    def __setitem__(self, idx: int, value: Union[int, bool, Any]) -> Optional[NoReturn]:
        mask = 1 << (idx % 8)
        if bool(value):
            self._field_bytearray[idx // 8] |= mask
        else:
            self._field_bytearray[idx // 8] &= ~mask

    def __len__(self) -> int:
        return self.field_size

    def count_activated(self) -> int:
        return bin(self.int()).count('1')

    # LISTS ---------------------------------------------------------------------------
    def list_bits(self) -> list[int]:
        """in NOhuman order
        """
        result = []
        for index in range(self.field_size):
            result.append(self[index])
        result.reverse()
        return result

    def list_activated_indexes(self) -> list[int]:
        """Return activated flag indexes in field!
        in human order (but order is not important!)

        in case of [101] -> [0, 2, ]
        """
        result = []
        for index in range(self.field_size):
            if self[index]:
                result.append(index)
        return result

    def list_activated_values(self) -> list[int]:
        """Return activated flag indexes in field!
        in human order (but order is not important!)

        in case of [101] -> [1, 4, ]
        """
        result = []
        for index in range(self.field_size):
            if self[index]:
                result.append(1 << index)
        return result

    # REPRESENTATIONS ---------------------------------------------------------------
    def __str__(self) -> str:
        return f"field[{self.field_str}]"

    def __repr__(self) -> str:
        return f"field[{self.field_str}]"

    def int(self) -> int:
        """
        print(int(bytearray(2).hex(), 16))
        """
        return int(self._field_bytearray.hex(), 16)

    def _bin_str(self) -> str:
        """common bin-format (without type prefix)

        print(bin(int(bytearray(2).hex())))     # 0b0
        """
        result = bin(self.int())[2:]
        result = "0" * (self.field_size - len(result)) + result
        return result

    def _hex_str(self) -> str:
        """common hex(full bytes)-format (without type prefix)
        print(bytearray(2).hex())
        """
        return self._field_bytearray.hex()


# =====================================================================================================================
class Flags(Bitfield):
    pass


# =====================================================================================================================
class Bits(Bitfield):
    pass


# =====================================================================================================================
