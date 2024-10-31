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
    # BASE
    ReqCheckStr_Base,
    ReqCheckStr_Os,
    ReqCheckStr_Arch,

    # AUX
    _GetattrClassmethod_Meta,

    # TYPES
    TYPE__VALUES,
    TYPE__RESULT_BOOL,
    TYPE__RESULT_RAISE,

    # EXX
    Exx_RequirementCantGetActualValue,
    Exx_Requirement,
)
from .pkgs import (
    # BASE
    Packages,
    CmdPattern,

    # AUX
    PATTERNS_IMPORT,
    PATTERN_IMPORT__MULTY_COMMA,
    PATTERN_IMPORT__MULTY_COMMA_BRACKETS,
    PATTERN_IMPORT__FROM,
    # TYPES
    # EXX
)
from .versions import (
    # BASE
    Version,
    ReqCheckVersion,
    ReqCheckVersion_Python,

    # AUX
    VersionBlock,

    # TYPES
    TYPE__VERSION_ELEMENT,
    TYPE__VERSION_ELEMENTS,
    TYPE__SOURCE_BLOCKS,

    TYPE__VERSION_BLOCKS,
    TYPE__SOURCE_VERSION,

    # EXX
    Exx_VersionIncompatible,
    Exx_VersionIncompatibleBlock,
    Exx_VersionIncompatibleCheck,
)


# =====================================================================================================================
