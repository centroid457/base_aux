from typing import *

from base_aux.aux_attr.m1_attr1_aux import *
from base_aux.aux_cmp_eq.m2_eq_aux import *
from base_aux.base_statics.m4_enums import *


# =====================================================================================================================
class NestEq_Attrs:
    """
    LOGIC
    -----
    cmp first - direct callables
    cmp second - resolveExx!!!
    """
    def __eq__(self, other: Any) -> bool:
        # if isinstance() NestInit_AnnotsAttrByKwArgs == NestInit_AnnotsAttrByKwArgs:
        #     # check by names

        if other is None:
            return False

        for attr in AttrAux(self).iter__not_private():
            # 1=cmp direct --------
            value_self_direct = AttrAux(self).getattr__callable_resolve(attr, CallableResolve.DIRECT)
            value_other_direct = AttrAux(other).getattr__callable_resolve(attr, CallableResolve.DIRECT)
            if EqAux(value_self_direct).check_doubleside__bool(value_other_direct):
                continue

            # 2=cmp callables --------
            value_self = AttrAux(self).getattr__callable_resolve(attr, CallableResolve.EXX)
            value_other = AttrAux(other).getattr__callable_resolve(attr, CallableResolve.EXX)

            if not EqAux(value_self).check_doubleside__bool(value_other):
                return False

        return True


# =====================================================================================================================
