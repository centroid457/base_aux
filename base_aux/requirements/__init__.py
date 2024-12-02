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
from .strings import (
    ReqCheckStr_Base,
    ReqCheckStr_Os,
    ReqCheckStr_Arch,

    _GetattrClassmethod_Meta,

    TYPE__VALUES,
    TYPE__RESULT_BOOL,
    TYPE__RESULT_RAISE,

    Exx_RequirementCantGetActualValue,
    Exx_Requirement,
)
from .pkgs import (
    Packages,
    CmdPattern,

    PATTERNS_IMPORT,
    PATTERN_IMPORT__MULTY_COMMA,
    PATTERN_IMPORT__MULTY_COMMA_BRACKETS,
    PATTERN_IMPORT__FROM,
)
from .versions import (
    Version,
    CheckVersion,
    CheckVersion_Python,

    VersionBlock,

    TYPE__VERSION_ELEMENT,
    TYPE__VERSION_ELEMENTS,
    TYPE__SOURCE_BLOCKS,

    TYPE__VERSION_BLOCKS,
    TYPE__SOURCE_VERSION,

    Exx_VersionIncompatible,
    Exx_VersionIncompatibleBlock,
    Exx_VersionIncompatibleCheck,
)


# =====================================================================================================================
