from typing import *

from base_aux.base_source.m2_source_kwargs import *
from base_aux.aux_types.m1_type_aux import TypeAux
from base_aux.aux_argskwargs.m1_argskwargs import TYPE__KWARGS_FINAL

from base_aux.aux_attr.m1_attr1_aux import AttrAux


# =====================================================================================================================
@final
class EqAux(InitSource):
    # -----------------------------------------------------------------------------------------------------------------
    def check_oneside__exx(self, other: Any, return_bool: bool = None) -> bool | Exception:
        # fixme: finish one side!!!!
        return NotImplemented

    def check_oneside__bool(self, other: Any) -> bool:
        return self.check_oneside__exx(other, return_bool=True)

    def check_oneside__reverse(self, other: Any) -> bool:
        return self.check_oneside__bool(other) is not True

    # -----------------------------------------------------------------------------------------------------------------
    def check_doubleside__exx(self, other: Any, return_bool: bool = None) -> bool | Exception:
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
        manipulate aux_types which have special methods for __cmp__
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
        if TypeAux(self.SOURCE).check__exception():
            if TypeAux(other).check__nested__by_cls_or_inst(self.SOURCE):
                return True
        elif TypeAux(other).check__exception():
            if TypeAux(self.SOURCE).check__nested__by_cls_or_inst(other):
                return True

        try:
            result12 = self.SOURCE == other
            if result12:
                return True
        except Exception as exx:
            result12 = exx
            # if TypeAux(other).check__exception() and TypeAux(result12).check__nested__by_cls_or_inst(other):
            #     return True

        try:
            result21 = other == self.SOURCE
            if result21:
                return True
        except Exception as exx:
            result21 = exx
            # if TypeAux(self.SOURCE).check__exception() and TypeAux(result21).check__nested__by_cls_or_inst(self.SOURCE):
            #     return True

        try:
            result3 = other is self.SOURCE
            if result3:
                return True
        except Exception as exx:
            result3 = exx
            pass

        if False in [result12, result21] or return_bool:
            return False
        else:
            return result12

    def check_doubleside__bool(self, other: Any) -> bool:
        """
        same as compare_doublesided_or_exx but
        in case of ClsException - return False

        CREATED SPECIALLY FOR
        ---------------------
        Valid.value_validate
        """
        return self.check_doubleside__exx(other, return_bool=True)

    def check_doubleside__reverse(self, other: Any) -> bool:
        """
        just reverse result for compare_doublesided__bool
        so never get ClsException, only bool
        """
        return self.check_doubleside__bool(other) is not True

    # -----------------------------------------------------------------------------------------------------------------
    def check_by_dict__direct(self, other: TYPE__KWARGS_FINAL) -> bool:
        """
        GOAL
        ----
        cmp direct values

        CREATED SPECIALLY FOR
        ---------------------
        """
        for key, expected in other.items():
            key_real = AttrAux(self.SOURCE).anycase__find(key)
            if key_real is None:
                if expected is None:
                    continue
                else:
                    return False
            try:
                actual = getattr(self.SOURCE, key)
            except Exception as exx:
                actual = exx

            if actual != expected:
                msg = f"for {key_real=} {actual=}/{expected=}"
                print(msg)
                return False


# =====================================================================================================================
# class EqByAttrs:
#     pass
#     # for dir


# =====================================================================================================================
