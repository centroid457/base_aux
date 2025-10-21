from typing import *

from enum import Enum
from base_aux.base_values.m2_value_special import NoValue


# =====================================================================================================================
# TODO: make own class! EnumIc with metaclass!
class NestEq_EnumAdj(Enum):
    """
    # NOTE
    # ----
    # DEL=work IC only on Eq! not working with Contains and Init!!! need edit Metaclass!

    CONSTRAINTS
    -----------
    1/ USE EqEnum: ONLY at SETTINGS values! and params values! so it is PARAMS using!!!
    2/ DONT USE: with result values! (for this case see Base_ValueSpecial specially created!)

    GOAL
    ----
    add user friendly cmp objects with final values

    for std object it is False but here its is correct!
    assert Enum(1) != 1
    assert NestEq_EnumAdj(1) == 1
    """
    # FIXME: cant create! - not work!!!
    # def __new__(cls, value_druft: Any):
    #     value_final = cls._value__get_original(value_druft)
    #     return cls(value_final)

    @classmethod
    def _value__get_original(cls, value_druft: Any) -> Any | NoValue:
        for item in cls:
            value_original = item.value
            if isinstance(value_druft, str):
                if value_druft.lower() == str(value_original).lower():
                    return value_original
            if value_druft == value_original:
                return value_original

        return NoValue

    # def __eq__(self, other) -> bool:
    #     if isinstance(other, self.__class__):
    #         return self.value == other.value        # or str(self.value).lower() == str(other.value).lower()    # NO!!!
    #
    #     else:
    #         for enum_i in self.__class__:
    #             if isinstance(other, str):
    #                 if str(enum_i.value).lower() == str(other).lower():
    #                     return True
    #             else:
    #                 try:
    #                     if enum_i.value == other or other == enum_i.value:
    #                         return True
    #                 except:
    #                     pass
    #     return False

    def __eq__(self, other) -> bool:
        # OBVIOUS -----------
        if isinstance(other, self.__class__):
            return self.value == other.value

        # CMP AVAILABLE -----
        cmp_available = False

        try:
            if other in self.__class__:
                cmp_available = True
        except:
            pass

        try:
            if other in self:
                cmp_available = True
        except:
            pass

        if cmp_available:
            return other == self.value or self == self.__class__(other)
        else:
            return False

    # TODO: add Contain classmeth???  cant understand! need metaclass!
    # @classmethod
    # def __contains__(cls, other) -> bool:
    #     if isinstance(other, cls):
    #         other = other.value
    #
    #     for enum_i in cls:
    #         if enum_i.value == other or str(enum_i.value).lower() == str(other).lower():
    #             return True
    #     else:
    #         return False

    @classmethod
    def as_dict__all(cls):
        """
        GOAL
        ----
        get all existed items in class
        """
        return {member.name: member.value for member in cls}


# =====================================================================================================================
