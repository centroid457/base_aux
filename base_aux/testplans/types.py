from typing import Union, NoReturn, Type
from funcs_aux import Valid, ValidChains


# =====================================================================================================================
TYPE__RESULT_BASE = Union[bool, Valid, ValidChains] | None
TYPE__RESULT_W_NORETURN = Union[TYPE__RESULT_BASE, NoReturn]
TYPE__RESULT_W_EXX = Union[TYPE__RESULT_BASE, Type[Exception]]


# =====================================================================================================================
