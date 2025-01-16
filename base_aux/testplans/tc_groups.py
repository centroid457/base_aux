from base_aux.classes.middle_group import *

from .tc_types import TYPE__RESULT_BASE, TYPE__RESULT_W_NORETURN, TYPE__RESULT_W_EXX


# =====================================================================================================================
class TcGroup_Base(ClsMiddleGroup):
    """
    make groups by separating startup/teardown
    """
    MIDDLE_GROUP__NAME = None
    MIDDLE_GROUP__CMP_ATTR = None

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

    @classmethod
    def teardown__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

    # @classmethod
    # def middle_group__check_equal__cls(cls, other: type[Self]) -> bool:
    #     """
    #
    #     this is will not work on classmethods!!!
    #     -------------------------
    #         class Cls:
    #             def meth(self):
    #                 pass
    #             @classmethod
    #             def cmeth(cls):
    #                 pass
    #
    #         class Cls2(Cls):
    #             pass
    #
    #         print(Cls.meth is Cls2.meth)
    #         print(Cls.meth == Cls2.meth)
    #         print(Cls.cmeth is Cls2.cmeth)
    #         print(Cls.cmeth == Cls2.cmeth)
    #
    #         print(Cls.meth)
    #         print(Cls2.meth)
    #         print(Cls.cmeth)
    #         print(Cls2.cmeth)
    #
    #         #
    #         True
    #         True
    #         False
    #         False
    #         <function Cls.meth at 0x000002CC6B525940>
    #         <function Cls.meth at 0x000002CC6B525940>
    #         <bound method Cls.cmeth of <class '__main__.Cls'>>
    #         <bound method Cls.cmeth of <class '__main__.Cls2'>>
    #     -------------------------
    #     """
    #     try:
    #         return cls.startup__cls__wrapped is other.startup__cls__wrapped and cls.teardown__cls__wrapped is other.teardown__cls__wrapped
    #     except:
    #         pass
    #     return False


# =====================================================================================================================
