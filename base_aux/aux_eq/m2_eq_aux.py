from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.base_types.m0_static_typing import TYPING


# =====================================================================================================================
@final
class EqAux(NestInit_Source):
    # FIXME: decide about callables/KwAgs by now NOT USE IT! just direct cmp eq!
    # CALLABLES: bool = None   # NOTE: DONT use callables here in Eq!!!
    # NOTE: dont use Args/Kwargs here in EqAux! - no callables! just final objects!

    # -----------------------------------------------------------------------------------------------------------------
    def check_oneside__exc(self, other: Any, return_bool: bool = None) -> bool | Exception:
        # if self.CALLABLES:
        #     self.SOURCE = CallableAux(self.SOURCE).resolve_exc()
        #
        #     try:
        #         other = CallableAux(other).resolve_raise()
        #     except Exception as exc:
        #         return exc

        # EXC ------
        if TypeAux(other).check__exception():
            if TypeAux(self.SOURCE).check__subclassed_or_isinst__from_cls_or_inst(other):   # CORRECT ORDER!!!
                return True
        # WORK ------
        try:
            result = self.SOURCE == other
            if result:
                return True
        except Exception as exc:
            result = exc
            # if TypeAux(other).check__exception() and TypeAux(result12).check__nested__from_cls_or_inst(other):
            #     return True
            if return_bool:
                result = False

        # FINAL ------
        return result

    def check_oneside__bool(self, other: Any) -> bool:
        return self.check_oneside__exc(other, return_bool=True)

    def check_oneside__reverse(self, other: Any) -> bool:
        return self.check_oneside__bool(other) is not True

    # -----------------------------------------------------------------------------------------------------------------
    def check_doubleside__exc(self, other: Any, return_bool: bool = None) -> bool | Exception:
        """
        GOAL
        ----
        just a direct comparing code like
            self.validate_last = self.value_last == self.VALIDATE_LINK or self.VALIDATE_LINK == self.value_last
        will not work correctly

        if any result is True - return True.
        if at least one false - return False
        if both exc - return first exc  # todo: deside return False in here!

        CREATED SPECIALLY FOR
        ---------------------
        manipulate base_types which have special methods for __cmp__
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
        # ONESIDE ------
        result12 = self.check_oneside__exc(other=other, return_bool=return_bool)
        if result12 is True:
            return True

        result21 = EqAux(other).check_oneside__exc(other=self.SOURCE, return_bool=return_bool)
        if result21 is True:
            return True

        # BOOL TRUE ------
        if return_bool:
            return False

        # BOOL FALSE ------
        if False in [result12, result21]:
            return False

        # FINAL -----------
        return result12

    def check_doubleside__bool(self, other: Any) -> bool:
        """
        same as compare_doublesided_or_exc but
        in case of ClsException - return False

        CREATED SPECIALLY FOR
        ---------------------
        Valid.value_validate
        """
        return self.check_doubleside__exc(other, return_bool=True)

    def check_doubleside__reverse(self, other: Any) -> bool:
        """
        just reverse result for compare_doublesided__bool
        so never get ClsException, only bool
        """
        return self.check_doubleside__bool(other) is not True

    # -----------------------------------------------------------------------------------------------------------------
    def check_by_dict__direct(self, other: TYPING.KWARGS_FINAL) -> bool:
        """
        GOAL
        ----
        cmp direct values

        CREATED SPECIALLY FOR
        ---------------------
        """
        for key, expected in other.items():
            key_real = AttrAux_Existed(self.SOURCE).name_ic__get_original(key)
            if key_real is None:
                if expected is None:
                    continue
                else:
                    return False
            try:
                actual = getattr(self.SOURCE, key)
            except Exception as exc:
                actual = exc

            if actual != expected:
                msg = f"for {key_real=} {actual=}/{expected=}"
                print(msg)
                return False


# =====================================================================================================================
# @final
# class EqAuxValidator:
#     # NOTE: for acllables DONT USE ARGS/KWARGS! its just about
#     CALLABLES = True


# =====================================================================================================================
# class EqByAttrs:
#     pass
#     # for dir


# =====================================================================================================================
