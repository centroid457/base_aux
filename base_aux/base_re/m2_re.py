from typing import *
import re

from base_aux.aux_attr.m4_kits import *
from base_aux.base_re.m1_rexp import *


# =====================================================================================================================
class Re:
    """
    GOAL
    ----
    apply same methods as in RУ module, but
    work with attempts
    """
    ATTEMPTS: TYPING__REXPS_FINAL

    def __init__(self, *attempts: TYPING__REXP_DRAFT, flags: int = None) -> None:
        result = []
        for attempt in attempts:
            pass

        self.ATTEMPTS = result


# =====================================================================================================================
