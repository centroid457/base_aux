from typing import *

import re

from base_aux.aux_types.m0_primitives import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.base_source.m2_source_kwargs import *
from base_aux.aux_types.m0_types import TYPE__VALID_VALIDATOR
from base_aux.aux_callable.m1_callable_aux import *
from base_aux.valid.m1_aux_valid_lg import *


# =====================================================================================================================
class _EqValidator:
    """
    MAIN IDEA
    ---------
    ALL WHAT PASSED INTO INIT WOULD PASS INTO VALIDATOR() AFTER FIRST ARG (OTHER)

    NOTE
    ----
    1/ preferably not use directly this object!
    USE DERIVATIVES!!! without validator passing

    2/ MAIN IDEA - NEVER RAISED!!! if any - return FALSE!!! if need - check manually!
    why so? - because i need smth to make a tests with final result of any source!
    dont mind reason!

    GOAL
    ----
    base object to make a validation by direct comparing with other object
    no raise

    USAGE
    -----
    PLACE ONLY IN FIRST PLACE!
    """
    VALIDATOR: TYPE__VALID_VALIDATOR

    V_ARGS: TYPE__ARGS_FINAL
    V_KWARGS: TYPE__KWARGS_FINAL

    REVERSE: bool = None

    OTHER_RAISED: bool = None
    OTHER_RESULT: Any | Exception = None

    def __init__(self, validator: TYPE__VALID_VALIDATOR = None, *v_args, reverse: bool = None, **v_kwargs) -> None:
        if validator is not None:
            self.VALIDATOR = validator

        if reverse is not None:
            self.REVERSE = reverse

        # super(ArgsKwargs, self).__init__(*v_args, **v_kwargs)
        self.V_ARGS = v_args
        self.V_KWARGS = v_kwargs

    def __str__(self):
        args = self.V_ARGS
        kwargs = self.V_KWARGS
        reverse = self.REVERSE
        return f"{self.__class__.__name__}({args=},{kwargs=},{reverse=})"

    def __eq__(self, other_draft) -> bool:
        return self.validate(other_draft)

    def __call__(self, other_draft: Any, *other_args, **other_kwargs) -> bool:
        """
        NOTE
        ----
        other_args/* - only for manual usage!
        typically used only other and only by direct eq(o1 == o2)
        """
        return self.validate(other_draft, *other_args, **other_kwargs)

    def __contains__(self, item) -> bool:
        return self.validate(item)

    def __iter__(self) -> Iterable[Any]:
        """
        NOTE
        ----
        not always correct!
        best usage for EqVariants or for any object with several args (Reqexp/...)
        """
        yield from self.V_ARGS

    def validate(self, other_draft: Any, *other_args, **other_kwargs) -> bool:
        """
        GOAL
        ----
        validate smth with special logic
        """
        # ------
        # TODO: decide use or not callable other??? = USE! it is really need to validate callable!!!
        try:
            self.OTHER_RESULT = CallableAux(other_draft).resolve_raise(*other_args, **other_kwargs)
            self.OTHER_RAISED = False
        except Exception as exx:
            self.OTHER_RAISED = True
            self.OTHER_RESULT = exx

        result = CallableAux(self.VALIDATOR).resolve_bool(self.OTHER_RESULT, *self.V_ARGS, **self.V_KWARGS)
        if self.REVERSE:
            result = not result
        return result

    def VALIDATOR(self, other_result, *v_args, **v_kwargs) -> bool | NoReturn:
        return NotImplemented


# ---------------------------------------------------------------------------------------------------------------------
class EqValid_Base(_EqValidator):
    def __init__(self, *v_args, reverse: bool = None, **v_kwargs):
        # print(v_args, v_kwargs)
        # super(ArgsKwargs, self).__init__(*v_args, **v_kwargs)     # not working!

        # super().__init__(*v_args, **v_kwargs)
        self.V_ARGS = v_args
        self.V_KWARGS = v_kwargs

        if reverse is not None:
            self.REVERSE = reverse


# =====================================================================================================================
@final
class EqValid_Variants(EqValid_Base):
    V_ARGS: TYPE__ARGS_FINAL
    V_KWARGS = KWARGS_FINAL__NOT_USED

    def VALIDATOR(self, other_result: Any, *variants: Any):
        if other_result in variants:
            return True
        else:
            return False


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_VariantsStrLow(EqValid_Base):
    V_ARGS: tuple[str, ...]
    V_KWARGS = KWARGS_FINAL__NOT_USED

    def VALIDATOR(self, other_result: Any, *variants: Any):
        other_result = str(other_result).lower()
        variants = (str(var).lower() for var in variants)

        if other_result in variants:
            return True
        else:
            return False


# =====================================================================================================================
@final
class EqValid_Raise(EqValid_Base):
    """
    GOAL
    ----
    True - if Other object called with raised
    if other is exact final Exception without raising - it would return False!
    """
    V_ARGS = ARGS_FINAL__NOT_USED
    V_KWARGS = KWARGS_FINAL__NOT_USED

    def VALIDATOR(self, other_result, *v_args, **v_kwargs) -> bool:
        return self.OTHER_RAISED


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_NotRaise(EqValid_Base):
    """
    GOAL
    ----
    True - if Other object called with raised
    if other is exact final Exception without raising - it would return False!
    """
    V_ARGS = ARGS_FINAL__NOT_USED
    V_KWARGS = KWARGS_FINAL__NOT_USED

    def VALIDATOR(self, other_result, *v_args, **v_kwargs) -> bool:
        return not self.OTHER_RAISED


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Exx(EqValid_Base):
    """
    GOAL
    ----
    True - if Other object is exact Exception or Exception()
    if raised - return False!!
    """
    V_ARGS = ARGS_FINAL__NOT_USED
    V_KWARGS = KWARGS_FINAL__NOT_USED

    def VALIDATOR(self, other_result, *v_args, **v_kwargs) -> bool | NoReturn:
        return not self.OTHER_RAISED and TypeAux(other_result).check__exception()


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_ExxRaised(EqValid_Base):
    """
    GOAL
    ----
    True - if Other object is exact Exception or Exception() or Raised
    """
    V_ARGS = ARGS_FINAL__NOT_USED
    V_KWARGS = KWARGS_FINAL__NOT_USED

    def VALIDATOR(self, other_result, *v_args, **v_kwargs) -> bool | NoReturn:
        return self.OTHER_RAISED or TypeAux(other_result).check__exception()


# =====================================================================================================================
@final
class EqValid_LtGt(EqValid_Base):
    def VALIDATOR(self, other_result, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other_result).ltgt(low, high)


@final
class EqValid_LtGe(EqValid_Base):
    def VALIDATOR(self, other_result, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other_result).ltge(low, high)


@final
class EqValid_LeGt(EqValid_Base):
    def VALIDATOR(self, other_result, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other_result).legt(low, high)


@final
class EqValid_LeGe(EqValid_Base):
    def VALIDATOR(self, other_result, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other_result).lege(low, high)


# =====================================================================================================================
class EqValid_Regexp(EqValid_Base):
    V_ARGS: tuple[str, ...]
    V_KWARGS: TYPE__KWARGS_FINAL

    BOOL_COLLECT: BoolCollect = BoolCollect.ALL_TRUE

    def VALIDATOR(
            self,
            other_result,
            *regexps: str,
            ignorecase: bool = True,
            bool_collect: BoolCollect = None,
            match_link: Callable = re.fullmatch,
    ) -> bool | NoReturn:
        bool_collect = bool_collect or self.BOOL_COLLECT

        for pattern in regexps:
            result_i = match_link(pattern=str(pattern), string=str(other_result), flags=re.RegexFlag.IGNORECASE if ignorecase else 0)

            # CUMULATE --------
            if bool_collect == BoolCollect.ALL_TRUE:
                if not result_i:
                    return False
            elif bool_collect == BoolCollect.ANY_TRUE:
                if result_i:
                    return True
            elif bool_collect == BoolCollect.ALL_FALSE:
                if result_i:
                    return False
            elif bool_collect == BoolCollect.ANY_FALSE:
                if not result_i:
                    return True

        # FINAL ------------
        if bool_collect in [BoolCollect.ALL_TRUE, BoolCollect.ALL_FALSE]:
            return True
        else:
            return False


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_RegexpAllTrue(EqValid_Regexp):
    BOOL_COLLECT: BoolCollect = BoolCollect.ALL_TRUE


@final
class EqValid_RegexpAnyTrue(EqValid_Regexp):
    BOOL_COLLECT: BoolCollect = BoolCollect.ANY_TRUE


@final
class EqValid_RegexpAllFalse(EqValid_Regexp):
    BOOL_COLLECT: BoolCollect = BoolCollect.ALL_FALSE


@final
class EqValid_RegexpAnyFalse(EqValid_Regexp):
    BOOL_COLLECT: BoolCollect = BoolCollect.ANY_FALSE


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
