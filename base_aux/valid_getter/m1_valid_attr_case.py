import platform

from base_aux.base_lambdas.m1_lambda import *

from base_aux.aux_eq.m3_eq_valid1_base import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.base_nest_dunders.m4_gsai_ic__annots import *

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_types.m0_static_types import *
from base_aux.base_types.m0_static_typing import *


# =====================================================================================================================
# FIXME: FINISH! its just a zero start - not working and not understand how it must work!!!

class Base_ValidSets:
    OTHER_DRAFT: Any | Callable = True
    OTHER_FINAL__RESOLVE: bool = True
    OTHER_RAISED: bool = None
    OTHER_FINAL: Any | Exception = None

    EQ_VALIDS: dict[str, Any | Base_EqValid] = {}
    EQ_EXPECTS: dict[str, bool | None] = {}

    def __init__(self, other_draft: Any = NoValue, **eq_valids: Any | Base_EqValid) -> None:
        # INIT=eq_valids -------------------------
        if eq_valids:
            self.EQ_VALIDS = eq_valids

        # remake to LOWER(IC)
        self.EQ_VALIDS = {key.lower(): value for key, value in self.EQ_VALIDS.items()}

        # other_draft ---------------------
        if other_draft is not NoValue:
            self.OTHER_DRAFT = other_draft

        if self.OTHER_FINAL__RESOLVE:
            try:
                self.OTHER_FINAL = Lambda(self.OTHER_DRAFT).resolve__raise()
                self.OTHER_RAISED = False
            except Exception as exx:
                self.OTHER_RAISED = True
                self.OTHER_FINAL = exx
        else:
            self.OTHER_FINAL = self.OTHER_DRAFT

        # FINISH=_other_final__resolve
        for eq_valid in self.EQ_VALIDS.values():
            eq_valid.OTHER_FINAL__RESOLVE = False
            eq_valid.OTHER_RAISED = self.OTHER_RAISED

    # -----------------------------------------------------------------------------------------------------------------
    def raise_if__fail_all(self, **eq_axpects: bool | None) -> None | NoReturn:
        """
        GOAL
        ----
        useful to check that single POSITIVE(expecting True) variant from any variants (mutually exclusive) expecting TRUE is not correct

        like
            (linux=True, windows=True)
        """
        pass

    def raise_if__fail_any(self, **eq_axpects: bool | None) -> None | NoReturn:
        """
        GOAL
        ----
        seems like common usage for exact eq-results for special state
            (val1=True, val2=False, val3=True)
        """
        pass

    def raise_if__any(self, **eq_axpects: bool | None) -> None | NoReturn:
        pass

    def raise_if__all(self, **eq_axpects: bool | None) -> None | NoReturn:
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def bool_if__all(self, **eq_axpects: bool | None) -> None | NoReturn:
        accept_any_true = False
        eq_axpects = {key.lower(): value for key, value in (eq_axpects or self.EQ_EXPECTS).items()}
        for name, accept in eq_axpects.items():
            if accept is not None:
                validate = self.OTHER_FINAL == self.EQ_VALIDS[name]
                result = accept and validate
                if not result:
                    msg = f"{name=}/{accept=}/{validate=}"
                    raise Exx__ValueNotValidated(msg)

    def bool_if__any(self, **eq_axpects: bool | None) -> bool | NoReturn:
        try:
            self.raise_if__accept_any_false__or__not_accept_any_true(**eq_axpects)
            return True
        except Exx__ValueNotValidated:
            return False
        except Exception as exx:
            raise exx

    def bool_if__fail_any(self, **eq_axpects: bool | None) -> None | NoReturn:
        pass

    def bool_if__fail_all(self, **eq_axpects: bool | None) -> None | NoReturn:
        pass

# # =====================================================================================================================
# class ValidAccepts_OS(Base_ValidAccepts):
#     OTHER_DRAFT: Any = platform.system
#
#     LINUX: Union[Base_EqValid, bool] = EqValid_EQ_StrIc("LINUX")
#     WINDOWS: Union[Base_EqValid, bool] = EqValid_EQ_StrIc("WINDOWS")
#
#
# # =====================================================================================================================
# # if __name__ == "__main__":
# #     assert ValidAccepts_OS("liNUX", linux=True).bool_if__accepts_meet()
#
#
# # =====================================================================================================================
# @pytest.mark.parametrize(
#     argnames="cls, _EXPECTED",
#     argvalues=[
#         # (Base_ValidAccepts, set()),
#         (ValidAccepts_OS, {"LINUX", "WINDOWS"}),
#     ]
# )
# def test__items_eq(cls, _EXPECTED):
#     Lambda(set(cls().items_eq())).expect__check_assert(_EXPECTED)
#
#
# # =====================================================================================================================
