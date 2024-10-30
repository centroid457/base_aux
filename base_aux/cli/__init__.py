# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT


# =====================================================================================================================
# TEMPLATE
# from .main import (
#     # BASE
#     EXACT_OBJECTS,
#
#     # AUX
#
#     # TYPES
#
#     # EXX
# )
# ---------------------------------------------------------------------------------------------------------------------
from .main import (
    # BASE
    CliUser,
    # AUX
    # TYPES
    TYPE__CMD,
    TYPE__CMDS,
    # EXX
    Exx_CliNotAvailable,
    Exx_CliTimeout,
    Exx_CliRetcode,
    Exx_CliStderr,
)


# =====================================================================================================================
