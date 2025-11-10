import platform

from base_aux.aux_argskwargs.m3_args_bool_raise_if import *
from base_aux.aux_text.m8_str_ic import *
from base_aux.aux_dict.m2_dict_ic import *


# =====================================================================================================================
TYPING__EQ_VALID__FINAL = Base_EqValid
TYPING__EQ_VALID__DRAFT = Any | Base_EqValid


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

    PARAMS
    ------
    EQ_VALID__CLS_DEF
        if used - values in EQ_KWARGS used as arg for it!
        EqValid_EQ_StrIc i  most useful
    """
    OTHER_DRAFT: Any | Callable = True
    OTHER_FINAL__RESOLVE: bool = True
    OTHER_RAISED: bool = None
    OTHER_FINAL: Any | Exception = None

    EQ_VALID__CLS_DEF: type[Base_EqValid] | None = None
    EQ_KWARGS: DictIcKeys[str, TYPING__EQ_VALID__FINAL] = {}      # dont use StrIc! cant direct access as GI(value)
    EQ_EXPECTS: dict[str, bool | None | Any] = {}

    def __init__(self, other_draft: Any | Callable = NoValue, _eq_valid__cls_def: type[Base_EqValid] = None, **eq_kwargs: TYPING__EQ_VALID__DRAFT) -> None:
        if _eq_valid__cls_def is not None:
            self.EQ_VALID__CLS_DEF = _eq_valid__cls_def

        self.init__eq_kwargs(**eq_kwargs)

        self.init__other(other_draft)
        self.init__other_push__chain()

    def init__eq_kwargs(self, **eq_kwargs: TYPING__EQ_VALID__DRAFT) -> None:
        eq_kwargs = eq_kwargs or self.EQ_KWARGS
        self.EQ_KWARGS = DictIcKeys(eq_kwargs)

        if self.EQ_VALID__CLS_DEF is None:
            return

        for key, value in self.EQ_KWARGS.items():
             if not isinstance(value, Base_EqValid):
                self.EQ_KWARGS[key] = self.EQ_VALID__CLS_DEF(value)

    def init__other(self, other_draft: Any | Callable = NoValue) -> None:
        # other_draft ---------------------
        if other_draft is not NoValue:
            self.OTHER_DRAFT = other_draft

        if self.OTHER_FINAL__RESOLVE:
            try:
                self.OTHER_FINAL = Lambda(self.OTHER_DRAFT).resolve__raise()
                self.OTHER_RAISED = False
            except Exception as exc:
                self.OTHER_RAISED = True
                self.OTHER_FINAL = exc
        else:
            self.OTHER_FINAL = self.OTHER_DRAFT

    def init__other_push__chain(self):
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
                raise Exc__WrongUsage(msg)

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

    # -----------------------------------------------------------------------------------------------------------------
    def __getattr__(self, item: str) -> bool | NoReturn:
        """
        GOAL
        ----
        direct access to final validation (OTHER_DRAFT) by exact item (EqValid) in EQ_KWARGS

        NOTE
        ----
        useful only for existed OTHER_DRAFT
        """
        result = self.bool_if__all_true(**{item: True})
        return result


# =====================================================================================================================
class Base_KwargsEqExpect_StrIc(Base_KwargsEqExpect):
    EQ_VALID__CLS_DEF: type[Base_EqValid] | None = EqValid_EQ_StrIc


# =====================================================================================================================
class KwargsEqExpect_OS(Base_KwargsEqExpect_StrIc):
    OTHER_DRAFT: Any = platform.system()  # NOTE: dont forget lambda *args: !!!! if use callable!

    EQ_KWARGS = dict(
        LINUX="LINUX",
        WINDOWS="WINDOWS",
    )

    # -----------
    WINDOWS: bool
    LINUX: bool


# ---------------------------------------------------------------------------------------------------------------------
class KwargsEqExpect_MachineArch(Base_KwargsEqExpect_StrIc):
    OTHER_DRAFT: Any = platform.machine()

    EQ_KWARGS = dict(
        AMD64="AMD64",        # standard PC
        x86_64="x86_64",      # wsl standard
        AARCH64="AARCH64",    # raspberry=ARM!
    )

    # -----------
    AMD64: bool
    x86_64: bool
    AARCH64: bool


# =====================================================================================================================
if __name__ == "__main__":
    # examples when you need WINDOWS!
    assert KwargsEqExpect_OS().bool_if__any_true(windows=True)
    assert not KwargsEqExpect_OS().raise_if__any_true(linux=True)
    assert KwargsEqExpect_OS().WINDOWS is True
    assert KwargsEqExpect_OS().windows is True


# =====================================================================================================================
