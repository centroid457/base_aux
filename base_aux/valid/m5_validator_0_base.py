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
    preferably not use directly this object!
    USE DERIVATIVES!!! without validator passing

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
def _explore_1():
    print(_EqValidator(bool) == 2)
    print(_EqValidator(bool) == 1)
    print(_EqValidator(bool) != 0)
    print(_EqValidator(bool) == LAMBDA_TRUE)


# =====================================================================================================================
class _EqValid_Base(_EqValidator):
    def __init__(self, *args, **kwargs):
        # print(args, kwargs)
        # super(ArgsKwargs, self).__init__(*args, **kwargs)     # not working!

        # super().__init__(*args, **kwargs)
        self.ARGS = args
        self.KWARGS = kwargs

# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Variants(_EqValid_Base):
    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        if other in args:
            return True
        else:
            return False


def _explore_21():
    print(EqValid_Variants(0, 1, 2) == 1)
    print(EqValid_Variants(0, 1, 2) != 3)
    print(EqValid_Variants(*"123") == "1")
    print(EqValid_Variants(*"123") != "false")


@final
class EqValid_VariantsStrLow(_EqValid_Base):
    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        other = str(other).lower()
        args = (str(arg).lower() for arg in args)
        if other in args:
            return True
        else:
            return False


def _explore_22():
    print(EqValid_VariantsStrLow(*"ABC") == "A")
    print(EqValid_VariantsStrLow(*"ABC") == "a")
    print(EqValid_VariantsStrLow(*"ABC") != "d")


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Exx(_EqValid_Base):
    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        return TypeAux(other).check__exception()


def _explore_3():
    print(EqValid_Exx() != False)
    print(EqValid_Exx() != 1)
    print(EqValid_Exx() == Exception)
    print(EqValid_Exx() == Exception())
    print(EqValid_Exx() == LAMBDA_EXX)
    print(EqValid_Exx() == LAMBDA_RAISE)


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Raise(_EqValid_Base):
    def VALIDATOR(self, other, *args, **kwargs) -> bool:
        return self.OTHER_RAISED


def _explore_4():
    print(EqValid_Raise() != False)
    print(EqValid_Raise() != Exception)
    print(EqValid_Raise() != Exception())
    print(EqValid_Raise() == LAMBDA_RAISE)


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_LtGt(_EqValid_Base):
    def VALIDATOR(self, other, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other).ltgt(low, high)


@final
class EqValid_LtGe(_EqValid_Base):
    def VALIDATOR(self, other, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other).ltge(low, high)


@final
class EqValid_LeGt(_EqValid_Base):
    def VALIDATOR(self, other, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other).legt(low, high)

@final
class EqValid_LeGe(_EqValid_Base):
    def VALIDATOR(self, other, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux(other).lege(low, high)


def _explore_5():
    print(EqValid_LtGt(1, 3) != 1)
    print(EqValid_LtGt(1, 3) == 2)
    print(EqValid_LtGt(1, 3) != 3)


# =====================================================================================================================
if __name__ == "__main__":
    _explore_1()
    print()
    _explore_21()
    print()
    _explore_22()
    print()
    _explore_3()
    print()
    _explore_4()


# =====================================================================================================================
