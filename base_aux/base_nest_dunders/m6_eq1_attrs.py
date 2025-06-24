from base_aux.aux_callable.m2_lambda import *


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
            for attr in AttrAux_Existed(self).iter__names_filter__not_private():
                # 1=cmp direct --------
                value_self_direct = getattr(self, attr)
                value_other_direct = getattr(other, attr)
                if EqAux(value_self_direct).check_doubleside__bool(value_other_direct):
                    continue

                # 2=cmp callables --------      # TODO: use Enum_CallResolveStyle.SKIPCALLABLES ???
                value_self = Lambda(getattr, self, attr).resolve__exx()
                value_other = Lambda(getattr, other, attr).resolve__exx()

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
            for attr in AttrAux_Existed(self).iter__names_filter__not_hidden():
                # 1=cmp direct --------
                value_self_direct = getattr(self, attr)
                value_other_direct = getattr(other, attr)
                if EqAux(value_self_direct).check_doubleside__bool(value_other_direct):
                    continue

                # 2=cmp callables --------      # TODO: use Enum_CallResolveStyle.SKIPCALLABLES ???
                value_self = Lambda(getattr, self, attr).resolve__exx()
                value_other = Lambda(getattr, other, attr).resolve__exx()

                if not EqAux(value_self).check_doubleside__bool(value_other):
                    return False

            return True
        except:
            return False


# =====================================================================================================================
