from typing import *
from base_aux.base_objects import TypeChecker


# =====================================================================================================================
class Eq:
    @classmethod
    def eq_doublesided_or_exx(cls, obj1: Any, obj2: Any, return_bool: bool = None) -> bool | Exception:
        """
        GOAL
        ----
        just a direct comparing code like
            self.validate_last = self.value_last == self.VALIDATE_LINK or self.VALIDATE_LINK == self.value_last
        will not work correctly

        if any result is True - return True.
        if at least one false - return False
        if both exx - return first exx  # todo: deside return False in here!

        CREATED SPECIALLY FOR
        ---------------------
        manipulate base_objects which have special methods for __cmp__
        for cases when we can switch places

        BEST USAGE
        ----------
            class ClsEq:
                def __init__(self, val):
                    self.VAL = val

                def __eq__(self, other):
                    return other == self.VAL

            assert ClsEq(1) == 1
            assert 1 == ClsEq(1)

            assert compare_doublesided(1, Cls(1)) is True
            assert compare_doublesided(Cls(1), 1) is True

        example above is not clear! cause of comparison works ok if any of object has __eq__() meth even on second place!
        but i think in one case i get ClsException and with switching i get correct result!!! (maybe fake! need explore!)
        """
        if TypeChecker.check__exception(obj1):
            if TypeChecker.check__nested__by_cls_or_inst(obj2, obj1):
                return True
        elif TypeChecker.check__exception(obj2):
            if TypeChecker.check__nested__by_cls_or_inst(obj1, obj2):
                return True

        try:
            result12 = obj1 == obj2
            if result12:
                return True
        except Exception as exx:
            result12 = exx
            # if TypeChecker.check__exception(obj2) and TypeChecker.check__nested__by_cls_or_inst(result12, obj2):
            #     return True

        try:
            result21 = obj2 == obj1
            if result21:
                return True
        except Exception as exx:
            result21 = exx
            # if TypeChecker.check__exception(obj1) and TypeChecker.check__nested__by_cls_or_inst(result21, obj1):
            #     return True

        try:
            result3 = obj2 is obj1
            if result3:
                return True
        except Exception as exx:
            result3 = exx
            pass

        if False in [result12, result21] or return_bool:
            return False
        else:
            return result12

    @classmethod
    def eq_doublesided__bool(cls, obj1: Any, obj2: Any) -> bool:
        """
        same as compare_doublesided_or_exx but
        in case of ClsException - return False

        CREATED SPECIALLY FOR
        ---------------------
        Valid.value_validate
        """
        return cls.eq_doublesided_or_exx(obj1, obj2, return_bool=True)

    @classmethod
    def eq_doublesided__reverse(cls, obj1: Any, obj2: Any) -> bool:
        """
        just reverse result for compare_doublesided__bool
        so never get ClsException, only bool
        """
        return cls.eq_doublesided__bool(obj1, obj2) is not True



# =====================================================================================================================
# class EqByAttrs:
#     pass
#     # for dir


# =====================================================================================================================
