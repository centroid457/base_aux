from enum import Enum


# =====================================================================================================================
# TODO: make own class! EnumIc with metaclass!
class NestEq_Enum(Enum):
    """
    # NOTE
    # ----
    # DEL=work IC only on Eq! not working with Contains and Init!!! need edit Metaclass!

    GOAL
    ----
    add user friendly cmp objects with final values

    VictimEq(1) == 1    # for std object it is False
    """
    # TODO: add Contain classmeth???  cant understand! need metaclass!

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
        result = False
        if isinstance(other, self.__class__):
            return self.value == other.value

        if other in self.__class__:
            result = True
        try:
            if other in self:
                result = True
        except:
            pass

        if result:
            return other == self.value or self == self.__class__(other)
        else:
            return False

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
