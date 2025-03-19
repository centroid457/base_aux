from typing import *

from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.aux_cmp_eq.m2_eq_aux import *
from base_aux.base_statics.m4_enums import *


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
        dont need cmp with only
        """
        # TODO: doublesided! to use all variants|
        try:
            checkable = isinstance(other, Nest_EqCls)
        except:
            checkable = issubclass(other, Nest_EqCls)

        if checkable:
            return cls._EQ_CLS__VALUE == other._EQ_CLS__VALUE

    @classmethod
    @property
    def _EQ_CLS__VALUE(cls) -> Any:
        """
        GOAL
        ----
        REDEFINE TO USE AS CMP VALUE
        """
        return cls.__name__     # just as example and for zero comparing


# =====================================================================================================================
if __name__ == "__main__":
    _explore()


# =====================================================================================================================
