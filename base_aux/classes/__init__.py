# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT
# VERSION = (0, 0, 2)   # del blank lines
# VERSION = (0, 0, 3)   # separate all types/exx into static.py!


# =====================================================================================================================
from .cmp import (
    CmpInst,
)
from .number import (
    NumberArithmTranslateToAttr,
    TYPE__NUMBER,
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
