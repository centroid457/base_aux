import platform

from base_aux.base_lambdas.m1_lambda import *

from base_aux.aux_eq.m3_eq_valid1_base import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.base_nest_dunders.m4_gsai_ic__annots import *

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m4_primitives import *
from base_aux.base_types.m0_static_types import *
from base_aux.base_types.m0_static_typing import *


# =====================================================================================================================
# FIXME: FINISH! its just a zero start - not working and not understand how it must work!!!

class Base_ValidEqKwargs:
    OTHER_DRAFT: Any | Callable = True
    OTHER_FINAL__RESOLVE: bool = True
    OTHER_RAISED: bool = None
    OTHER_FINAL: Any | Exception = None

    EQ_KWARGS: dict[str, Any | Base_EqValid] = {}
    EQ_EXPECTS: dict[str, bool | None] = {}

    def __init__(self, other_draft: Any = NoValue, **eq_kwargs: Any | Base_EqValid) -> None:
        # INIT=eq_kwargs -------------------------
        if eq_kwargs:
            self.EQ_KWARGS = eq_kwargs

        # remake to LOWERCASE
        self.EQ_KWARGS = {key.lower(): value for key, value in self.EQ_KWARGS.items()}

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
        for eq_valid in self.EQ_KWARGS.values():
            if isinstance(eq_valid, Base_EqValid):
                eq_valid.OTHER_FINAL__RESOLVE = False
                eq_valid.OTHER_RAISED = self.OTHER_RAISED

    def _eq_expects__get_final(self, **eq_axpects: bool | None) -> dict[str, bool | None]:
        """
        GOAL
        ----
        two goals:
        1/ if passed any set - get it as pre-final, if not - get default!
        2/ apply lowercase for keys of preFinal
        """
        result = {key.lower(): value for key, value in (eq_axpects or self.EQ_EXPECTS).items()}

        if not result:
            result = {key.lower(): True for key, value in self.EQ_KWARGS.items()}
        return result

    # =================================================================================================================
    def _check_if__(
            self,
            _raise_if_fail: bool = None,
            _bool_cumulate: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ALL_TRUE,
            **eq_axpects: bool | None,
    ) -> bool | NoReturn:
        results: list[bool] = []

        eq_axpects = self._eq_expects__get_final(**eq_axpects)
        for name, expect in eq_axpects.items():

            if name not in self.EQ_KWARGS:
                msg = f"{name=} not in {self.EQ_KWARGS=}"
                raise Exx__WrongUsage(msg)

            if expect is not None:
                validate_i = self.EQ_KWARGS[name] == self.OTHER_FINAL   # RAISE
                result_i = validate_i is expect
                results.append(result_i)

                if (
                        _bool_cumulate == EnumAdj_BoolCumulate.ALL_TRUE and not result_i
                        or
                        _bool_cumulate == EnumAdj_BoolCumulate.ALL_FALSE and result_i
                ):
                    msg = f"{name=}/{expect=}/{validate_i=}"
                    if _raise_if_fail:
                        raise Exx__ValueNotValidated(msg)               # RAISE
                    else:
                        print(msg)
                        return False

                if (
                        _bool_cumulate == EnumAdj_BoolCumulate.ANY_TRUE and result_i
                        or
                        _bool_cumulate == EnumAdj_BoolCumulate.ANY_FALSE and not result_i
                ):
                    msg = f"{name=}/{expect=}/{validate_i=}"
                    print(msg)
                    return True

        # FINAL result -----------------------
        msg = f"{eq_axpects=}/{results=}"
        print(msg)

        from base_aux.base_lambdas.m1_lambda2_derivatives import Boo
        if _bool_cumulate == EnumAdj_BoolCumulate.ALL_TRUE:
            result = Bool(results)
        if _bool_cumulate == EnumAdj_BoolCumulate.ALL_FALSE:
            result = all(results)
        return True

    # -----------------------------------------------------------------------------------------------------------------
    def bool_if__all(self, _raise_if_fail: bool = None, **eq_axpects: bool | None) -> bool | NoReturn:
        return self._check_if__(_raise_if_fail=False, _bool_cumulate=EnumAdj_BoolCumulate.ALL_TRUE, **eq_axpects)

    def bool_if__any(self, **eq_axpects: bool | None) -> bool | NoReturn:
        return self._check_if__(_raise_if_fail=False, _bool_cumulate=EnumAdj_BoolCumulate.ANY_TRUE, **eq_axpects)

    def bool_if__fail_all(self, **eq_axpects: bool | None) -> bool | NoReturn:
        return self._check_if__(_raise_if_fail=False, _bool_cumulate=EnumAdj_BoolCumulate.ALL_FALSE, **eq_axpects)

    def bool_if__fail_any(self, **eq_axpects: bool | None) -> bool | NoReturn:
        return self._check_if__(_raise_if_fail=False, _bool_cumulate=EnumAdj_BoolCumulate.ANY_FALSE, **eq_axpects)

    # -----------------------------------------------------------------------------------------------------------------
    def raise_if__fail_all(self, **eq_axpects: bool | None) -> None | NoReturn:
        """
        GOAL
        ----
        useful to check that single POSITIVE(expecting True) variant from any variants (mutually exclusive) expecting TRUE is not correct

        like
            (linux=True, windows=True)
        """
        return self._check_if__(_raise_if_fail=True, _bool_cumulate=EnumAdj_BoolCumulate.ALL_FALSE, **eq_axpects)

    def raise_if__fail_any(self, **eq_axpects: bool | None) -> None | NoReturn:
        """
        GOAL
        ----
        seems like common usage for exact eq-results for special state
            (val1=True, val2=False, val3=True)
        """
        return self._check_if__(_raise_if_fail=True, _bool_cumulate=EnumAdj_BoolCumulate.ANY_FALSE, **eq_axpects)

    def raise_if__all(self, **eq_axpects: bool | None) -> None | NoReturn:
        return self._check_if__(_raise_if_fail=True, _bool_cumulate=EnumAdj_BoolCumulate.ALL_TRUE, **eq_axpects)

    def raise_if__any(self, **eq_axpects: bool | None) -> None | NoReturn:
        return self._check_if__(_raise_if_fail=True, _bool_cumulate=EnumAdj_BoolCumulate.ANY_TRUE, **eq_axpects)


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


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="other_draft, eq_kwargs, eq_expects, _EXPECTED",
    argvalues=[
        # TOOD: add LAMBDA_RAISE

        (1, dict(eq1=EqValid_EQ(1)), {}, [True, True, False, False]),
    ]
)
def test__base(other_draft, eq_kwargs, eq_expects, _EXPECTED):
    # Lambda(Base_ValidEqKwargs(other_draft, **eq_kwargs).bool_if__all, **eq_expects).expect__check_assert(_EXPECTED[0])
    # Lambda(Base_ValidEqKwargs(other_draft, **eq_kwargs).bool_if__any, **eq_expects).expect__check_assert(_EXPECTED[1])
    # Lambda(Base_ValidEqKwargs(other_draft, **eq_kwargs).bool_if__fail_all, **eq_expects).expect__check_assert(_EXPECTED[2])
    Lambda(Base_ValidEqKwargs(other_draft, **eq_kwargs).bool_if__fail_any, **eq_expects).expect__check_assert(_EXPECTED[3])


# =====================================================================================================================
