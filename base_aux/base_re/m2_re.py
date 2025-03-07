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
class ReAttempts:
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

    def _result__get_from_match(self, match: re.Match) -> TYPING__RE_RESULT__ONE:
        """
        NOTE
        ----
        this is the main idea for whole this class!

        GOAL
        ----
        get result from match object
        1. if no groups - return matching string
        2. if one group - return exact group value
        3. if several groups - return tuple of groups
        """
        if not isinstance(match, re.Match):
            raise Exx__WrongUsage(f"{match=}")

        groups = match.groups()
        if groups:
            if len(groups) == 1:
                return groups[0]
            else:
                return groups
        else:
            return match.group()

    def search(self, other: Any) -> TYPING__RE_RESULT__ALL:
        other = str(other)

        result = []
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF]).get_first_is_not_none()

            match = re.search(rexp.PAT, other, flags)
            if match:
                return self._result__get_from_match(match)

    def sub(self):
        pass

    def delete(self):
        pass


# =====================================================================================================================
