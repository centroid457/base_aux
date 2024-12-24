from typing import *

from base_aux.base_argskwargs.argskwargs import TYPE__LAMBDA_ARGS, TYPE__LAMBDA_KWARGS
from base_aux.funcs import *
from base_aux.lambdas.lambdas import Lambda
from base_aux.cmp.eq import Eq


# =====================================================================================================================
class EqValidator:
    """
    base object to make a validation by direct comparing with other object
    no raise
    """

    VALIDATE_LINK: TYPE__VALID_VALIDATOR
    EXPECTED: bool | Any
    ARGS: TYPE__LAMBDA_ARGS
    KWARGS: TYPE__LAMBDA_KWARGS

    def __init__(self, validate_link: TYPE__VALID_VALIDATOR, *args, **kwargs) -> None:
        self.VALIDATE_LINK = validate_link
        self.ARGS = args
        self.KWARGS = kwargs

    def __eq__(self, other) -> bool:
        other = Lambda(other).get_result_or_exx()
        args = (other, *self.ARGS)
        expected = Lambda(self.VALIDATE_LINK).get_result_or_exx(*args, **self.KWARGS)

        result = Eq(other).eq_doublesided__bool(expected)
        return result

    def __call__(self, other: Any) -> bool:
        return self == other


# =====================================================================================================================
