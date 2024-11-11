# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT
# VERSION = (0, 0, 2)   # del blank lines
# VERSION = (0, 0, 3)   # separate all types/exx into static.py!


# =====================================================================================================================
# TEMPLATE
# from .STATIC import (
#     # TYPES
#     # EXX
# )
# from .main import (
#     # BASE
#     # AUX
# )
# ---------------------------------------------------------------------------------------------------------------------
# from .static import (
# )
# ---------------------------------------------------------------------------------------------------------------------
from .breeder_1_str_1_series import (
    BreederStrSeries,
)
from .breeder_1_str_2_stack import (
    BreederStrStack,
    BreederStrStack_Example,
    BreederStrStack_Example__BestUsage
)
from .breeder_2_objects import (
    BreederObjectList,
    BreederObjectList_GroupType,

    TYPE__BREED_RESULT__ITEM,
    TYPE__BREED_RESULT__GROUP,
    TYPE__BREED_RESULT__GROUPS,
)
# =====================================================================================================================
