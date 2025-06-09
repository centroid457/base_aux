from base_aux.aux_eq.m2_eq_aux import *
from base_aux.aux_values.m5_enums import *


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
            for attr in AttrAux(self).iter__names_filter__not_private():
                # 1=cmp direct --------
                value_self_direct = AttrAux(self).gai_ic__callable_resolve(attr, Enum_CallResolve.DIRECT)
                value_other_direct = AttrAux(other).gai_ic__callable_resolve(attr, Enum_CallResolve.DIRECT)
                if EqAux(value_self_direct).check_doubleside__bool(value_other_direct):
                    continue

                # 2=cmp callables --------      # TODO: use Enum_CallResolve.SKIPCALLABLES ???
                value_self = AttrAux(self).gai_ic__callable_resolve(attr, Enum_CallResolve.EXX)
                value_other = AttrAux(other).gai_ic__callable_resolve(attr, Enum_CallResolve.EXX)

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
            for attr in AttrAux(self).iter__names_filter__not_hidden():
                # 1=cmp direct --------
                value_self_direct = AttrAux(self).gai_ic__callable_resolve(attr, Enum_CallResolve.DIRECT)
                value_other_direct = AttrAux(other).gai_ic__callable_resolve(attr, Enum_CallResolve.DIRECT)
                if EqAux(value_self_direct).check_doubleside__bool(value_other_direct):
                    continue

                # 2=cmp callables --------      # TODO: use Enum_CallResolve.SKIPCALLABLES ???
                value_self = AttrAux(self).gai_ic__callable_resolve(attr, Enum_CallResolve.EXX)
                value_other = AttrAux(other).gai_ic__callable_resolve(attr, Enum_CallResolve.EXX)

                if not EqAux(value_self).check_doubleside__bool(value_other):
                    return False

            return True
        except:
            return False


# =====================================================================================================================
