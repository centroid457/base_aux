# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT
# VERSION = (0, 0, 2)   # del blank lines
# VERSION = (0, 0, 3)   # separate all types/exx into static.py!


# =====================================================================================================================
# TEMPLATE
# from .static import (
#     # TYPES
#     # EXX
# )
# from .main import (
#     # BASE
#     # AUX
# )
# ---------------------------------------------------------------------------------------------------------------------
from .static import (
    # TYPES
    TYPE__PV_DICT,
    TYPE__PATH,
    TYPE__VALUE,
    # EXX
    Exx__FileNotExists,
    Exx__SameKeys,
)
from .base import (
    # BASE
    PrivateBase,
    # AUX
)
from .derivatives import (
    # BASE
    PrivateAuth,
    PrivateTgBotAddress,
    # AUX
)
from .env import (
    # BASE
    PrivateEnv,
    # AUX
)
from .csv import (
    # BASE
    PrivateCsv,
    PrivateAuthCsv,
    PrivateTgBotAddressCsv,
    # AUX
)
from .ini import (
    # BASE
    PrivateIni,
    PrivateAuthIni,
    PrivateTgBotAddressIni,
    # AUX
)
from .json import (
    # BASE
    PrivateJson,
    PrivateAuthJson,
    PrivateTgBotAddressJson,
    # AUX
)
from .auto import (
    # BASE
    PrivateAuto,
    PrivateAuthAuto,
    PrivateTgBotAddressAuto,
    # AUX
)

# =====================================================================================================================
