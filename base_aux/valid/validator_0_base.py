from typing import *

from base_aux.objects import TypeChecker
from base_aux.funcs import *
from base_aux.valid import ValidAux
from base_aux.classes import Lambda
from base_aux.classes.static import TYPE__LAMBDA_CONSTRUCTOR, TYPE__LAMBDA_ARGS, TYPE__LAMBDA_KWARGS


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

    def __init__(self, validate_link: TYPE__VALID_VALIDATOR, expected: bool | Any = True, *args, **kwargs) -> None:
        self.VALIDATE_LINK = validate_link
        self.EXPECTED = expected
        self.ARGS = args
        self.KWARGS = kwargs

    def __eq__(self, other) -> bool:
        if TypeChecker.check__callable_func_meth_inst(other):   #fixme: get final value? -  make call_if_callable()
            other = other()

        # if validate_link    #


# =====================================================================================================================
