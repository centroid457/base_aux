from typing import *

from base_aux.aux_types.m0_primitives import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.base_source.m2_source_kwargs import *
from base_aux.aux_types.m0_types import TYPE__VALID_VALIDATOR
from base_aux.aux_callable.m1_callable_aux import *
from base_aux.valid.m1_aux_valid_lg import *


# =====================================================================================================================
class _EqValidator:
    """
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

    ARGS: TYPE__ARGS_FINAL
    KWARGS: TYPE__KWARGS_FINAL

    OTHER_RAISED: bool = None

    def __init__(self, validator: TYPE__VALID_VALIDATOR = None, *args, **kwargs) -> None:
        if validator is not None:
            self.VALIDATOR = validator

        # super(ArgsKwargs, self).__init__(*args, **kwargs)
        self.ARGS = args
        self.KWARGS = kwargs

    def __eq__(self, other) -> bool:
        return self.validate(other)

    def __call__(self, other: Any, *other_args, **other_kwargs) -> bool:
        """
        NOTE
        ----
        other_args/* - only for manual usage!
        typically used only other and only by direct eq(o1 == o2)
        """
        return self.validate(other, *other_args, **other_kwargs)

    def validate(self, other: Any, *other_args, **other_kwargs) -> bool:
        """
        GOAL
        ----
        validate smth with special logic
        """
        # ------
        # TODO: decide use or not callable other??? = USE! it is really need to validate callable!!!
        try:
            other_result = CallableAux(other).resolve_raise(*other_args, **other_kwargs)
            self.OTHER_RAISED = False
        except Exception as exx:
            self.OTHER_RAISED = True
            other_result = exx

        result = CallableAux(self.VALIDATOR).resolve_bool(other_result, *self.ARGS, **self.KWARGS)
        return result

    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        return NotImplemented


# ---------------------------------------------------------------------------------------------------------------------
class EqValid_Base(_EqValidator):
    def __init__(self, *args, **kwargs):
        # print(args, kwargs)
        # super(ArgsKwargs, self).__init__(*args, **kwargs)     # not working!

        # super().__init__(*args, **kwargs)
        self.ARGS = args
        self.KWARGS = kwargs


# =====================================================================================================================
@final
class EqValid_Variants(EqValid_Base):
    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        if other in args:
            return True
        else:
            return False


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_VariantsStrLow(EqValid_Base):
    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        other = str(other).lower()
        args = (str(arg).lower() for arg in args)
        if other in args:
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
    def VALIDATOR(self, other, *args, **kwargs) -> bool:
        return self.OTHER_RAISED

# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Exx(EqValid_Base):
    """
    GOAL
    ----
    True - if Other object is exact Exception or Exception()
    if raised - return False!!
    """
    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        return not self.OTHER_RAISED and TypeAux(other).check__exception()


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_ExxRaised(EqValid_Base):
    """
    GOAL
    ----
    True - if Other object is exact Exception or Exception() or Raised
    """
    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        return self.OTHER_RAISED or TypeAux(other).check__exception()


# =====================================================================================================================
@final
class EqValid_LtGt(EqValid_Base):
    def VALIDATOR(self, other, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other).ltgt(low, high)


@final
class EqValid_LtGe(EqValid_Base):
    def VALIDATOR(self, other, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other).ltge(low, high)


@final
class EqValid_LeGt(EqValid_Base):
    def VALIDATOR(self, other, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other).legt(low, high)


@final
class EqValid_LeGe(EqValid_Base):
    def VALIDATOR(self, other, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other).lege(low, high)


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
