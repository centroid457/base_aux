from typing import *

from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.aux_cmp_eq.m2_eq_aux import *
from base_aux.base_statics.m4_enums import *
from base_aux.aux_types.m1_type_aux import *


# =====================================================================================================================
def _explore():
    class Cls:
        @classmethod
        def __eq__(cls, other):
            return True

    class Cls2(Cls):
        def __eq__(self, other):
            return True

    print(Cls == Cls2)  # False!
    print(Cls2 == Cls)  # False!


# =====================================================================================================================
class Nest_EqCls:
    """
    GOAL
    ----
    create ability to cmpEQ classes

    NOTE
    ----
    UNACCEPTABLE:
    1/ __eq__ is not working with classmethod!
    2/ meta is not acceptable!!!! in case of class is already Metaclassed like QThread!
        and in future it can become it!

    ACCEPTABLE
    3/ simply create method classmethod to cmp with any class
    4/ if you intend cmp only same classes - create propertyClassmethod

    BEST USAGE
    ----------
    1. create base class (with Nest_EqCls as parent)
    2. define _EQ_CLS__VALUE as classmethod to
    3. when need comparing classes use standard method _eq_cls__check(other) from any of object
    4. if you want cmp not comparring classes like Nest_EqCls-nested and not nested - redefine _eq_cls__check method manually  - but mayby it is not good idea!!!

    SPECIALLY CREATED FOR
    ---------------------
    TC cmp classes instead of MiddleGroup!
    """
    @classmethod
    def _eq_cls__check(cls, other: Any | type[Any]) -> bool:
        """
        show how to cmp clss
        """
        try:
            checkable = issubclass(other, Nest_EqCls)   # keep first!!!
        except:
            checkable = isinstance(other, Nest_EqCls)

        if checkable:
            return EqAux(cls._EQ_CLS__VALUE).check_doubleside__bool(other._EQ_CLS__VALUE)
        else:
            return False

    @classmethod
    @property
    def _EQ_CLS__VALUE(cls) -> Any:
        """
        GOAL
        ----
        REDEFINE TO USE AS CMP VALUE
        """
        return cls.__name__     # just as example and for zero comparing

    @staticmethod
    def _eq_classes__check(obj1: Any | type[Any], obj2: Any | type[Any]) -> bool:
        """
        eqCmp classes as function
        """
        cls1 = TypeAux(obj1).get__class()
        cls2 = TypeAux(obj2).get__class()

        if TypeAux(cls1).check__nested__by_cls_or_inst(Nest_EqCls):
            # cls1: Nest_EqCls
            return cls1._eq_cls__check(cls2)
        elif TypeAux(cls2).check__nested__by_cls_or_inst(Nest_EqCls):
            # cls1: Nest_EqCls
            return cls2._eq_cls__check(cls1)
        else:
            return cls1 == cls2 or cls2 == cls1


# =====================================================================================================================
def _best_usage():
    # with enums!
    from enum import Enum

    class ClsGroup(Enum):
        G1 = 1
        G2 = 2

    class Victim(Nest_EqCls):
        ATTR1 = 0
        @classmethod
        @property
        def _EQ_CLS__VALUE(cls) -> ClsGroup:
            """
            GOAL
            ----
            REDEFINE TO USE AS CMP VALUE
            """
            if cls.ATTR1 == 1:
                return ClsGroup.G1
            else:
                return ClsGroup.G2


# =====================================================================================================================
if __name__ == "__main__":
    _best_usage()


# =====================================================================================================================
