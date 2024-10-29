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
from .static import (
    # TYPES
    # EXX
    Exx__AnnotNotDefined,
)
from .annot_1_aux import (
    # BASE
    AnnotAux,
    # AUX
)
from .annot_3_iter_values import AnnotValuesIter
from .annot_2_all_defined import (
    # BASE
    AnnotAllDefined,
    # AUX
)
from .annot_4_cls_keys_as_values import (
    # BASE
    AnnotClsKeysAsValues,
    # AUX
    AnnotClsKeysAsValues_Meta,
)
# ---------------------------------------------------------------------------------------------------------------------
from .cmp import (
    # BASE
    CmpInst,
    # AUX
    # TYPES
    # EXX
)
from .number import (
    # BASE
    NumberArithmTranslateToAttr,
    # AUX
    # TYPES
    TYPE__NUMBER,
    # EXX
    Exx__NumberArithm_NoName,
)
# ---------------------------------------------------------------------------------------------------------------------
from .getattr_0_echo import (
    # BASE
    GetattrEcho,
    GetattrEchoSpace,
    # AUX
    # TYPES
    # EXX
)
from .getattr_1_aux import (
    # BASE
    GetattrAux,
    # AUX
    # TYPES
    # EXX
)
from .getattr_2_anycase import (
    # BASE
    GetattrAnycase,
    # AUX
    # TYPES
    # EXX
)
from .getattr_3_prefix_1_inst import (
    # BASE
    GetattrPrefixInst,
    GetattrPrefixInst_RaiseIf,
    # AUX
    # TYPES
    # EXX
    Exx__GetattrPrefix,
    Exx__GetattrPrefix_RaiseIf,
)
from .getattr_3_prefix_2_cls import GetattrPrefixCls_MetaTemplate

# ---------------------------------------------------------------------------------------------------------------------
from .middle_group import (
    # BASE
    ClsMiddleGroup,
    # AUX
    # TYPES
    # EXX
)

# ---------------------------------------------------------------------------------------------------------------------
from .value_1_variants import (
    # BASE
    ValueVariants,
    # AUX
    # TYPES
    # EXX
    Exx__ValueNotInVariants,
    Exx__VariantsIncompatible,
)
from .value_2_unit import (
    # BASE
    ValueUnit,
    # AUX
    UnitBase,
    UNIT_MULT__VARIANTS,
    # TYPES
    Exx__ValueNotParsed,
    Exx__ValueUnitsIncompatible,
    # EXX
)
# ---------------------------------------------------------------------------------------------------------------------
from .valid_0_aux import ValidAux
from .valid_1_base import (
    # BASE
    Valid,
    # AUX
    # TYPES
    # TYPE__EXCEPTION,
    # TYPE__SOURCE_LINK,
    TYPE__VALIDATE_LINK,
    TYPE__BOOL_LINK,
    # EXX
)
from .valid_2_chains import (
    ValidChains,
    TYPE__CHAINS,
)
from .valid_1_base_derivatives import (
    # BASE
    ValidRetry1,
    ValidRetry2,
    ValidFailStop,
    ValidFailContinue,
    ValidNoCum,
    ValidReverse,
    ValidSleep,
    # AUX
    # TYPES
    # EXX
)
from .valid_3_regexp import (
    # BASE
    ValidRegExp,
    # AUX
    # TYPES
    # EXX
)

# ---------------------------------------------------------------------------------------------------------------------
from .breeder_1_str_1_series import (
    # BASE
    BreederStrSeries,
    # AUX
    # EXX
    Exx__IndexOverlayed,
    Exx__IndexNotSet,
    Exx__ItemNotExists,
    Exx__StartOuterNONE_UsedInStackByRecreation,
)
from .breeder_1_str_2_stack import (
    # BASE
    BreederStrStack,
    # AUX
    BreederStrStack_Example,
    BreederStrStack_Example__BestUsage
    # TYPES
    # EXX
)
from .breeder_2_objects import (
    # BASE
    BreederObjectList,
    # AUX
    BreederObjectList_GroupType,
    # TYPES
    TYPE__BREED_RESULT__ITEM,
    TYPE__BREED_RESULT__GROUP,
    TYPE__BREED_RESULT__GROUPS,
    # EXX
    Exx__BreederObjectList_GroupsNotGenerated,
    Exx__BreederObjectList_GroupNotExists,
    Exx__BreederObjectList_ObjCantAccessIndex,
)
# ---------------------------------------------------------------------------------------------------------------------
from .singleton import (
    # BASE
    SingletonManagerBase,
    SingletonMetaCallClass,
    SingletonByCallMeta,
    SingletonByNew,
    # AUX
    # TYPES
    # EXX
    Exx_SingletonNestingLevels,
)


# =====================================================================================================================
