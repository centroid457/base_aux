from typing import *

from base_aux.aux_types.m0_primitives import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.base_source.m2_source_kwargs import *
from base_aux.aux_types.m0_types import TYPE__VALID_VALIDATOR
from base_aux.aux_callable.m1_callable_aux import *
from base_aux.cmp.m2_eq import EqAux


# =====================================================================================================================
class EqValidator:
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

    def __init__(self, validator: TYPE__VALID_VALIDATOR = None, args: TYPE__ARGS_DRAFT = (), kwargs: TYPE__KWARGS_DRAFT = None, *args2, **kwargs2) -> None:
        if validator is not None:
            self.VALIDATOR = validator
        self.ARGS = ArgsKwargsAux(args).resolve_args()
        self.KWARGS = ArgsKwargsAux(kwargs).resolve_kwargs()
        super().__init__(*args2, **kwargs2)

    def __eq__(self, other) -> bool:
        return self.validate(other)

    def __call__(self, other: Any, *other_args, **other_kwargs) -> bool:
        return self.validate(other, *other_args, **other_kwargs)

    def validate(self, other: Any, *other_args, **other_kwargs) -> bool:
        """
        GOAL
        ----
        validate smth with special logic
        """
        # other_result = CallableAux(other, *_args, **_kwargs).resolve_exx()
        # expected = CallableAux(self.SOURCE).resolve_exx(*args, **self.KWARGS)
        # result = EqAux(other_result).eq_doublesided__bool(expected)

        # ------
        other_result = CallableAux(other).resolve_exx(*other_args, **other_kwargs)
        result = CallableAux(self.VALIDATOR).resolve_bool(*(other_result, *self.ARGS), **self.KWARGS)
        return result


# ---------------------------------------------------------------------------------------------------------------------
def _explore_1():
    print(EqValidator(bool) == 2)
    print(EqValidator(bool) == 1)
    print(EqValidator(bool) != 0)
    print(EqValidator(bool) != LAMBDA_TRUE)


# =====================================================================================================================
class EqVariants(EqValidator):
    def __init__(self, args=(), kwargs=None):
        super().__init__(validator=None, args=args, kwargs=kwargs)

    def VALIDATOR(self, other, *args, **kwargs) -> bool | NoReturn:
        if other in args:
            return True
        else:
            return False


# ---------------------------------------------------------------------------------------------------------------------
def _explore_2():
    print(EqVariants([0,1,2 ]) == 1)
    print(EqVariants([0,1,2 ]) != 3)
    print(EqVariants([*"123"]) == "1")
    print(EqVariants([*"123"]) != "false")


# =====================================================================================================================
if __name__ == "__main__":
    _explore_1()
    print()
    _explore_2()


# =====================================================================================================================
