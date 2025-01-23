from typing import *

from base_aux.aux_types.m0_primitives import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.base_source.m2_source_kwargs import *
from base_aux.aux_types.m0_types import TYPE__VALID_VALIDATOR
from base_aux.aux_callable.m1_callable_aux import *


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
    VALIDATOR: TYPE__VALID_VALIDATOR = True

    ARGS: TYPE__ARGS_FINAL
    KWARGS: TYPE__KWARGS_FINAL

    OTHER_RAISED: bool = None

    def __init__(self, validator: TYPE__VALID_VALIDATOR = None, args: TYPE__ARGS_DRAFT = (), kwargs: TYPE__KWARGS_DRAFT = None) -> None:
        if validator is not None:
            self.VALIDATOR = validator
        self.ARGS = ArgsKwargsAux(args).resolve_args()
        self.KWARGS = ArgsKwargsAux(kwargs).resolve_kwargs()

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

        result = CallableAux(self.VALIDATOR).resolve_bool(*(other_result, *self.ARGS), **self.KWARGS)
        return result


# ---------------------------------------------------------------------------------------------------------------------
def _explore_1():
    print(_EqValidator(bool) == 2)
    print(_EqValidator(bool) == 1)
    print(_EqValidator(bool) != 0)
    print(_EqValidator(bool) == LAMBDA_TRUE)


# =====================================================================================================================
class _EqValid_Base(_EqValidator):
    def __init__(self, args=(), kwargs=None):
        super().__init__(validator=None, args=args, kwargs=kwargs)

    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        return NotImplemented


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValidVariants(_EqValid_Base):
    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        if other in args:
            return True
        else:
            return False


def _explore_2():
    print(EqValidVariants([0, 1, 2]) == 1)
    print(EqValidVariants([0, 1, 2]) != 3)
    print(EqValidVariants([*"123"]) == "1")
    print(EqValidVariants([*"123"]) != "false")


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValidExx(_EqValid_Base):
    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        return TypeAux(other).check__exception()


def _explore_3():
    print(EqValidExx() != False)
    print(EqValidExx() != 1)
    print(EqValidExx() == Exception)
    print(EqValidExx() == Exception())
    print(EqValidExx() == LAMBDA_EXX)
    print(EqValidExx() == LAMBDA_RAISE)


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValidRaise(_EqValid_Base):
    def VALIDATOR(self, other, *args, **kwargs) -> bool:
        return self.OTHER_RAISED


def _explore_4():
    print(EqValidRaise() != False)
    print(EqValidRaise() != Exception)
    print(EqValidRaise() != Exception())
    print(EqValidRaise() == LAMBDA_RAISE)


# =====================================================================================================================
if __name__ == "__main__":
    _explore_1()
    print()
    _explore_2()
    print()
    _explore_3()
    print()
    _explore_4()


# =====================================================================================================================
