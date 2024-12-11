# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT
# VERSION = (0, 0, 2)   # del blank lines
# VERSION = (0, 0, 3)   # separate all types/exx into static.py!


# =====================================================================================================================
# TEMPLATE
# from .static import (
# )
# from .main import (
# )
# ---------------------------------------------------------------------------------------------------------------------
from .static import (
    TYPE__PV_DICT,
    TYPE__PATH,
    TYPE__VALUE,

    Exx__FileNotExists,
    Exx__SameKeys,
)
from .attr_loader__0_base import (
    PrivateBase,
)
from .derivatives import (
    PrivateAuth,
    PrivateTgBotAddress,
)
from .attr_loader__1_env import (
    PrivateEnv,
)
from .attr_loader__2_csv import (
    PrivateCsv,
    PrivateAuthCsv,
    PrivateTgBotAddressCsv,
)
from .attr_loader__3_ini import (
    PrivateIni,
    PrivateAuthIni,
    PrivateTgBotAddressIni,
)
from .attr_loader__4_json import (
    PrivateJson,
    PrivateAuthJson,
    PrivateTgBotAddressJson,
)
from .attr_loader__5_auto import (
    PrivateAuto,
    PrivateAuthAuto,
    PrivateTgBotAddressAuto,
)

# =====================================================================================================================
