# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT


# =====================================================================================================================
# TEMPLATE
# from .main import (
#     EXACT_OBJECTS,
# )
# ---------------------------------------------------------------------------------------------------------------------
from .history import HistoryIO
from .serial_client import (
    SerialClient,

    TYPE__ADDRESS,
    TYPE__RW_ANSWER_SINGLE,
    TYPE__RW_ANSWER,
    Type__WrReturn,
    Type__AddressAutoAcceptVariant,

    Exx_SerialAddress_NotApplyed,
    Exx_SerialAddress_NotExists,
    Exx_SerialAddresses_NoVacant,
    Exx_SerialAddresses_NoAutodetected,
    Exx_SerialAddress_AlreadyOpened,
    Exx_SerialAddress_AlreadyOpened_InOtherObject,
    Exx_SerialAddress_OtherError,
    Exx_SerialRead_NotFullLine,
    Exx_SerialRead_FailPattern,
    Exx_SerialRead_FailDecoding,
    Exx_SerialPL2303IncorrectDriver,
)
from .serial_server import (
    SerialServer_Base,
    SerialServer_Echo,
    SerialServer_Example,

    AnswerVariants,

    TYPE__CMD_RESULT,
)
from .serial_derivatives import (
    SerialClient_FirstFree,
    SerialClient_FirstFree_Shorted,
    SerialClient_FirstFree_Paired,
    SerialClient_FirstFree_AnswerValid,
    SerialClient_Emulated,
)

# ==========INFO: NOTE: use direct import from file! not here!!! sometimes in some PC Windows it get Stack!
# from base_aux.requirements import ReqCheckStr_Os
# if ReqCheckStr_Os.bool_if__LINUX():
#     from .i2c_client import (
#         BusI2c,
#         Patterns,
#
#         Exx_I2cConnection,
#     )


# =====================================================================================================================
