from typing import *
from base_aux.base_source.m2_source_kwargs import *
from base_aux.aux_argskwargs.m1_argskwargs import TYPE__ARGS_FINAL, TYPE__KWARGS_FINAL
from base_aux.aux_types.m0_types import TYPE__VALID_VALIDATOR
from base_aux.aux_callable.m1_callable_aux import *
from base_aux.cmp.m2_eq import EqAux


# =====================================================================================================================
class EqValidator(InitSourceKwArgs_Explicite):
    """
    GOAL
    ----
    base object to make a validation by direct comparing with other object
    no raise

    USAGE
    -----
    PLACE ONLY IN FIRST PLACE!
    """

    SOURCE: TYPE__VALID_VALIDATOR
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

        result = EqAux(other).eq_doublesided__bool(expected)
        return result

    def __call__(self, other: Any) -> bool:
        return self == other

    def validate(self) -> bool:
        pass


# =====================================================================================================================
