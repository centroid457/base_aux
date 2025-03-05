from typing import *
import re

from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
class RExp(Nest_AttrKit):
    """
    GOAL
    ----
    simple pattern with all expected params
    """
    PAT: str
    FLAGS: int | None = None
    SUB: str = None     # used only for sub/del methods!


# =====================================================================================================================
TYPING__ATTEMTS = Iterable[str | RExp]


# =====================================================================================================================
