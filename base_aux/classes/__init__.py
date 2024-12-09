# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT
# VERSION = (0, 0, 2)   # del blank lines
# VERSION = (0, 0, 3)   # separate all types/exx into static.py!


# =====================================================================================================================
# ---------------------------------------------------------------------------------------------------------------------
from .annot_1_aux import (
    AnnotAux,
)
from .annot_3_iter_values import (
    AnnotValuesIter
)
from .annot_2_required import (
    AnnotRequired,
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
from .attr_0_init_kwargs import (
    AttrInitKwargs,
)
from .attr_1_aux import (
    AttrAux,
)
from .attr_2_anycase import (
    AttrAnycase,
)
from .attr_3_lambda_call import (
    AttrLambdaCall,
)
# ---------------------------------------------------------------------------------------------------------------------
from .lambdas import (
    Lambda,

    LambdaBool,
    LambdaBoolReversed,

    LambdaTrySuccess,
    LambdaTryFail,

    LambdaSleep,
    LambdaSleepAfter,
)
# ---------------------------------------------------------------------------------------------------------------------
from .middle_group import (
    ClsMiddleGroup,
)
# ---------------------------------------------------------------------------------------------------------------------
from .text import (
    Text,
)
# ---------------------------------------------------------------------------------------------------------------------
from .translator import (
    Translator,
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
