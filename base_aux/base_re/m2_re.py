from typing import *
import re

from base_aux.aux_attr.m4_kits import *
from base_aux.base_re.m1_rexp import *
from base_aux.aux_iter.m1_iter_aux import *
from base_aux.base_statics.m2_exceptions import *


# =====================================================================================================================
TYPING__RE_RESULT__ONE = str | tuple[str, ...] | None
TYPING__RE_RESULT__ALL = TYPING__RE_RESULT__ONE | list[TYPING__RE_RESULT__ONE] | None


# =====================================================================================================================
class Re:
    """
    GOAL
    ----
    apply same methods as in RE module, but
    work with attempts

    NOTE
    ----
    ATTEMPTS_USAGE - useful not in all methods - tis obvious.
    """
    ATTEMPTS: TYPING__REXPS_FINAL
    FLAGS_DEF: int = None
    ATTEMPTS_USAGE: AttemptsUsage = AttemptsUsage.ALL

    def __init__(self, *attempts: TYPING__REXP_DRAFT, flags_def: int = None, attempts_usage: AttemptsUsage = None) -> None:
        if flags_def is not None:
            self.FLAGS_DEF = flags_def

        if attempts_usage is not None:
            self.ATTEMPTS_USAGE = AttemptsUsage(attempts_usage)

        result = []
        for attempt in attempts:
            if isinstance(attempt, RExp):
                result.append(attempt)
            elif isinstance(attempt, str):
                result.append(RExp(attempt))
            else:
                raise Exx__Incompatible(f"{attempt=}")

        self.ATTEMPTS = result

    def search(self, flags: int = None) -> TYPING__RE_RESULT__ALL:
        result = []
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS,  flags, self.FLAGS_DEF]).get_first_is_not_none()

            if re.search():
                pass



# =====================================================================================================================
