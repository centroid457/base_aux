from base_aux.valid.valid_10_chains import *


# =====================================================================================================================
TYPE__RESULT_BASE = Union[bool, Valid, ValidChains] | None
TYPE__RESULT_W_NORETURN = Union[TYPE__RESULT_BASE, NoReturn]
TYPE__RESULT_W_EXX = Union[TYPE__RESULT_BASE, type[Exception]]


# =====================================================================================================================
