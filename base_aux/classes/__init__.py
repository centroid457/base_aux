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
    Exx__AnnotNotDefined,
    Exx__NumberArithm_NoName,
    Exx__GetattrPrefix,
    Exx__GetattrPrefix_RaiseIf,
    Exx__ValueNotInVariants,
    Exx__VariantsIncompatible,
    Exx__ValueNotParsed,
    Exx__ValueUnitsIncompatible,
    Exx__IndexOverlayed,
    Exx__IndexNotSet,
    Exx__ItemNotExists,
    Exx__StartOuterNONE_UsedInStackByRecreation, Exx__BreederObjectList_GroupsNotGenerated,
    Exx__BreederObjectList_GroupNotExists, Exx__BreederObjectList_ObjCantAccessIndex,
)
from .annot_1_aux import (
    AnnotAux,
)
from .annot_3_iter_values import (
    AnnotValuesIter
)
from .annot_2_all_defined import (
    AnnotAllDefined,
)
from .annot_4_cls_keys_as_values import (
    AnnotClsKeysAsValues,
    AnnotClsKeysAsValues_Meta,
)
# ---------------------------------------------------------------------------------------------------------------------
from .cmp import (
    CmpInst,
)
from .number import (
    NumberArithmTranslateToAttr,
    TYPE__NUMBER,
)
# ---------------------------------------------------------------------------------------------------------------------
from .getattr_0_echo import (
    GetattrEcho,
    GetattrEchoSpace,
)
from .attr_1_aux import (
    AttrAux,
)
from .attr_2_anycase import (
    AttrAnycase,
)
from .getattr_3_prefix_1_inst import (
    GetattrPrefixInst,
    GetattrPrefixInst_RaiseIf,

)
from .getattr_3_prefix_2_cls import (
    GetattrPrefixCls_MetaTemplate
)

from .attr_4_construct_on_init import (
    ConstructOnInit_Item,
    ConstructOnInit,
)
# ---------------------------------------------------------------------------------------------------------------------
from .attr_3_dict_dots_1_simple import (
    DictDots,
)
from .attr_3_dict_dots_2_full import (
    DictDotsFull,
)
# ---------------------------------------------------------------------------------------------------------------------
from .middle_group import (
    ClsMiddleGroup,
)

# ---------------------------------------------------------------------------------------------------------------------
from .value_1_variants import (
    ValueVariants,
)
from .value_2_unit import (
    ValueUnit,

    UnitBase,
    UNIT_MULT__VARIANTS,
)
# ---------------------------------------------------------------------------------------------------------------------
from .valid_0_aux import ValidAux
from .valid_1_base import (
    Valid,

    TYPE__VALIDATE_LINK,
    TYPE__BOOL_LINK,
)
from .valid_2_chains import (
    ValidChains,
    TYPE__CHAINS,
)
from .valid_1_base_derivatives import (
    ValidRetry1,
    ValidRetry2,
    ValidFailStop,
    ValidFailContinue,
    ValidNoCum,
    ValidReverse,
    ValidSleep,
)
from .valid_3_regexp import (
    ValidRegExp,
)

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
# ---------------------------------------------------------------------------------------------------------------------
from .singleton import (
    SingletonManagerBase,
    SingletonMetaCallClass,
    SingletonByCallMeta,
    SingletonByNew,

    Exx_SingletonNestingLevels,
)


# =====================================================================================================================
