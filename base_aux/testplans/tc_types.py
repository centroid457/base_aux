from base_aux.valid.m3_valid_chains import *


# =====================================================================================================================
# NOTE: dont move into TC! need separation!

TYPING__RESULT_BASE = Union[bool, Valid, ValidChains] | None
TYPING__RESULT_W_NORETURN = Union[TYPING__RESULT_BASE, NoReturn]
TYPING__RESULT_W_EXC = Union[TYPING__RESULT_BASE, type[Exception]]


# =====================================================================================================================
