from typing import *

from base_aux.aux_attr.m1_attr1_aux import *
from base_aux.aux_cmp_eq.m2_eq_aux import *
from base_aux.base_statics.m4_enums import *


# =====================================================================================================================
class NestEq_AttrsNotPrivate:
    """
    GOAL
    ----
    mainly used for cmp bare attr-kits with no callables!

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

        try:
            for attr in AttrAux(self).iter__attrs_not_private():
                # 1=cmp direct --------
                value_self_direct = AttrAux(self).gai_ic__callable_resolve(attr, CallableResolve.DIRECT)
                value_other_direct = AttrAux(other).gai_ic__callable_resolve(attr, CallableResolve.DIRECT)
                if EqAux(value_self_direct).check_doubleside__bool(value_other_direct):
                    continue

                # 2=cmp callables --------      # TODO: use CallableResolve.SKIPCALLABLES ???
                value_self = AttrAux(self).gai_ic__callable_resolve(attr, CallableResolve.EXX)
                value_other = AttrAux(other).gai_ic__callable_resolve(attr, CallableResolve.EXX)

                if not EqAux(value_self).check_doubleside__bool(value_other):
                    return False

            return True
        except:
            return False


# =====================================================================================================================
class NestEq_AttrsNotHidden:
    def __eq__(self, other: Any) -> bool:
        # if isinstance() NestInit_AnnotsAttrByKwArgs == NestInit_AnnotsAttrByKwArgs:
        #     # check by names

        if other is None:
            return False

        try:
            for attr in AttrAux(self).iter__attrs_not_hidden():
                # 1=cmp direct --------
                value_self_direct = AttrAux(self).gai_ic__callable_resolve(attr, CallableResolve.DIRECT)
                value_other_direct = AttrAux(other).gai_ic__callable_resolve(attr, CallableResolve.DIRECT)
                if EqAux(value_self_direct).check_doubleside__bool(value_other_direct):
                    continue

                # 2=cmp callables --------      # TODO: use CallableResolve.SKIPCALLABLES ???
                value_self = AttrAux(self).gai_ic__callable_resolve(attr, CallableResolve.EXX)
                value_other = AttrAux(other).gai_ic__callable_resolve(attr, CallableResolve.EXX)

                if not EqAux(value_self).check_doubleside__bool(value_other):
                    return False

            return True
        except:
            return False


# =====================================================================================================================
