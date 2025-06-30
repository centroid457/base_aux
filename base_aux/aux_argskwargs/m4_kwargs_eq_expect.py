import platform

from base_aux.aux_argskwargs.m3_args_bool_raise_if import *


# =====================================================================================================================
class Base_KwargsEqExpect:
    """
    GOAL
    ----
    1/ use object as named collection of EqValids
    2/ select exact EqValids for final cmp
    3/ select exact results for any expectatins

    SPECIALLY CREATED FOR
    ---------------------
    replace inconvenient Base_ReqCheckStr for objects like ReqCheckStr_Os
    good check exact expectations
    """
    OTHER_DRAFT: Any | Callable = True
    OTHER_FINAL__RESOLVE: bool = True
    OTHER_RAISED: bool = None
    OTHER_FINAL: Any | Exception = None

    EQ_KWARGS: dict[str, Any | Base_EqValid] = {}
    EQ_EXPECTS: dict[str, bool | None | Any] = {}

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

    def _eq_expects__get_final(self, **eq_axpects: bool | None | Any) -> dict[str, bool | None]:
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
            _raise_instead_true: bool = None,
            _iresult_cumulate: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ALL_TRUE,
            **eq_axpects: bool | None | Any,
    ) -> bool | NoReturn:
        results: list[bool] = []

        eq_axpects = self._eq_expects__get_final(**eq_axpects)
        for name, expect in eq_axpects.items():

            if name not in self.EQ_KWARGS:
                msg = f"{name=} not in {self.EQ_KWARGS=}"
                raise Exx__WrongUsage(msg)

            if expect is not None:
                result_i = Lambda(
                    lambda: self.EQ_KWARGS[name] == self.OTHER_FINAL,
                ).expect__check_bool(expect)
                results.append(result_i)

        # FINAL result -----------------------
        msg = f"{eq_axpects=}/{results=}"
        print(msg)

        result = Base_ArgsBoolIf(*results, _iresult_cumulate=_iresult_cumulate, _raise_instead_true=_raise_instead_true).resolve()
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def bool_if__all_true(self, **eq_axpects: bool | None | Any) -> bool | NoReturn:
        return self._check_if__(_raise_instead_true=False, _iresult_cumulate=EnumAdj_BoolCumulate.ALL_TRUE, **eq_axpects)

    def bool_if__any_true(self, **eq_axpects: bool | None | Any) -> bool | NoReturn:
        return self._check_if__(_raise_instead_true=False, _iresult_cumulate=EnumAdj_BoolCumulate.ANY_TRUE, **eq_axpects)

    def bool_if__all_false(self, **eq_axpects: bool | None | Any) -> bool | NoReturn:
        return self._check_if__(_raise_instead_true=False, _iresult_cumulate=EnumAdj_BoolCumulate.ALL_FALSE, **eq_axpects)

    def bool_if__any_false(self, **eq_axpects: bool | None | Any) -> bool | NoReturn:
        return self._check_if__(_raise_instead_true=False, _iresult_cumulate=EnumAdj_BoolCumulate.ANY_FALSE, **eq_axpects)

    # -----------------------------------------------------------------------------------------------------------------
    def raise_if__all_false(self, **eq_axpects: bool | None) -> None | NoReturn:
        """
        GOAL
        ----
        useful to check that single POSITIVE(expecting True) variant from any variants (mutually exclusive) expecting TRUE is not correct

        like
            (linux=True, windows=True)
        """
        return self._check_if__(_raise_instead_true=True, _iresult_cumulate=EnumAdj_BoolCumulate.ALL_FALSE, **eq_axpects)

    def raise_if__any_false(self, **eq_axpects: bool | None | Any) -> None | NoReturn:
        """
        GOAL
        ----
        seems like common usage for exact eq-results for special state
            (val1=True, val2=False, val3=True)
        """
        return self._check_if__(_raise_instead_true=True, _iresult_cumulate=EnumAdj_BoolCumulate.ANY_FALSE, **eq_axpects)

    def raise_if__all_true(self, **eq_axpects: bool | None | Any) -> None | NoReturn:
        return self._check_if__(_raise_instead_true=True, _iresult_cumulate=EnumAdj_BoolCumulate.ALL_TRUE, **eq_axpects)

    def raise_if__any_true(self, **eq_axpects: bool | None | Any) -> None | NoReturn:
        return self._check_if__(_raise_instead_true=True, _iresult_cumulate=EnumAdj_BoolCumulate.ANY_TRUE, **eq_axpects)


# =====================================================================================================================
class KwargsEqExpect_OS(Base_KwargsEqExpect):
    OTHER_DRAFT: Any = platform.system()  # NOTE: dont forget lambda *args: !!!! if use callable!

    EQ_KWARGS = dict(
        LINUX=EqValid_EQ_StrIc("LINUX"),
        WINDOWS=EqValid_EQ_StrIc("WINDOWS"),
    )


# ---------------------------------------------------------------------------------------------------------------------
class KwargsEqExpect_MachineArch(Base_KwargsEqExpect):
    OTHER_DRAFT: Any = platform.machine()

    EQ_KWARGS = dict(
        AMD64=EqValid_EQ_StrIc("AMD64"),        # standard PC
        x86_64=EqValid_EQ_StrIc("x86_64"),      # wsl standard
        AARCH64=EqValid_EQ_StrIc("AARCH64"),    # raspberry=ARM!
    )


# =====================================================================================================================
if __name__ == "__main__":
    assert KwargsEqExpect_OS().bool_if__any_true(windows=True)


# =====================================================================================================================
