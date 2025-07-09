# FIXME: USE Base_KwargsEqExpect instead!!!!???? or decide to use smth!



from typing import *

from base_aux.base_values.m2_value_special import NoValue
from base_aux.aux_eq.m3_eq_valid1_base import *


# =====================================================================================================================
class Type__:
    pass


class __EnumEqValid:
    """
    GOAL
    ----
    try create universal class with exact selecting items
    where no needs to create special logic for different cmpring
    """
    # ATTR1: Base_EqValid | Any
    # ATTR2: Base_EqValid | Any

    _SOURCE: Any
    _EQ_VALID__CLS_DEF: Base_EqValid

    def __init__(self, source: Any) -> None | NoReturn:
        for value in self.values():
            if source == self._EQ_VALID__CLS_DEF(value):
                return

        msg = f"{value=} not in {self.values()=}"
        raise Exx__Incompatible(msg)

    @classmethod
    def cls__init_items(cls) -> None:
        for name in ():
            pass

    def find_item(self, item_draft: Any) -> Self:
        pass

    def names(self) -> Iterable[str]:
        pass

    def values(self) -> Iterable[Any]:
        pass

    def exists_in__names(self) -> bool:
        pass

    def exists_in__values(self) -> bool:
        pass















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


# =====================================================================================================================
