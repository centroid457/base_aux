# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT
# VERSION = (0, 0, 2)   # del blank lines


# =====================================================================================================================
# TEMPLATE
# from .main import (
#     EXACT_OBJECTS,
# )
# ---------------------------------------------------------------------------------------------------------------------
from .gui import (
    Gui,
    TYPE__SIZE_TUPLE,
)
from .signals import (
    SignalsTemplate,
)
from .th import (
    HeaderViewCB,
)
from .tm import (
    Headers,
    TableModelTemplate,
)
from .hl import (
    format_make,
    HlStyle,
    HlStyles,
    Highlighter,

    HlStylesPython,
    HlStylesMultiline,
    HlStylesExample,
    start_example,
)
from .static import (
    COLOR_TUPLE_RGB,
    MARGINS,
    ALIGNMENT,
)
from .mods import (
    Icons,
    WgtColorChange,
    WgtColored,
    QPushButton_Checkable,
)


# =====================================================================================================================

