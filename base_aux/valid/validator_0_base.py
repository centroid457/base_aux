from typing import *

from base_aux.aux_argskwargs.m1_argskwargs import TYPE__ARGS_FINAL, TYPE__KWARGS_FINAL
from base_aux.funcs import *
from base_aux.aux_callable import *
from base_aux.cmp.eq import Eq


# =====================================================================================================================
class EqValidator:
    """
    base object to make a validation by direct comparing with other object
    no raise
    """

    VALIDATE_LINK: TYPE__VALID_VALIDATOR
    EXPECTED: bool | Any
    ARGS: TYPE__ARGS_FINAL
    KWARGS: TYPE__KWARGS_FINAL

    def __init__(self, validate_link: TYPE__VALID_VALIDATOR, *args, **kwargs) -> None:
        self.VALIDATE_LINK = validate_link
        self.ARGS = args
        self.KWARGS = kwargs

    def __eq__(self, other) -> bool:
        other = CallableAux(other).resolve_exx()
        args = (other, *self.ARGS)
        expected = CallableAux(self.VALIDATE_LINK).resolve_exx(*args, **self.KWARGS)

        result = Eq(other).eq_doublesided__bool(expected)
        return result

    def __call__(self, other: Any) -> bool:
        return self == other


# =====================================================================================================================
