from base_aux.aux_text.m5_re1_rexp import *
from base_aux.aux_iter.m1_iter_aux import *
from base_aux.base_statics.m2_exceptions import *


# =====================================================================================================================
TYPING__OTHER_DRAFT = str | Any
TYPING__RE_RESULT__ONE = str | tuple[str, ...]
TYPING__RE_RESULT__ALL = TYPING__RE_RESULT__ONE | list[TYPING__RE_RESULT__ONE]


# =====================================================================================================================
class Base_ReAttempts:
    """
    GOAL
    ----
    apply same methods as in RE module, but
    work with attempts

    NOTE
    ----
    ATTEMPTS_USAGE - expecting work with priority
    if FIRST - return result for first match function in attempt order
    if ALL - return list of results for all matched attempts
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

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _result__get_from_match(match: re.Match) -> TYPING__RE_RESULT__ONE:
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

    # -----------------------------------------------------------------------------------------------------------------
    def match(self, other: TYPING__OTHER_DRAFT) -> TYPING__RE_RESULT__ALL:
        other = str(other)
        result = []
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF, 0]).get_first_is_not_none()

            match = re.match(rexp.PAT, other, flags)
            if match:
                result_i = self._result__get_from_match(match)
                if self.ATTEMPTS_USAGE == AttemptsUsage.FIRST:
                    return result_i
                else:
                    result.append(result_i)
        return result

    def fullmatch(self, other: TYPING__OTHER_DRAFT) -> TYPING__RE_RESULT__ALL:
        other = str(other)
        result = []
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF, 0]).get_first_is_not_none()

            match = re.fullmatch(rexp.PAT, other, flags)
            if match:
                result_i = self._result__get_from_match(match)
                if self.ATTEMPTS_USAGE == AttemptsUsage.FIRST:
                    return result_i
                else:
                    result.append(result_i)
        return result

    def search(self, other: TYPING__OTHER_DRAFT) -> TYPING__RE_RESULT__ALL | None:
        other = str(other)
        result = []
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF, 0]).get_first_is_not_none()

            match = re.search(rexp.PAT, other, flags)
            if match:
                result_i = self._result__get_from_match(match)
                if self.ATTEMPTS_USAGE == AttemptsUsage.FIRST:
                    return result_i
                else:
                    result.append(result_i)
        return result

    def sub(self, other: TYPING__OTHER_DRAFT, new: str = None) -> str:
        result = None
        other = str(other)
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF, 0]).get_first_is_not_none()
            new = IterAux([rexp.SUB, new, ""]).get_first_is_not_none()

            result = re.sub(rexp.PAT, new, other, flags)
            if result != other:
                other = result
                if self.ATTEMPTS_USAGE == AttemptsUsage.FIRST:
                    break

        return result

    def delete(self, other: TYPING__OTHER_DRAFT) -> str:
        return self.sub(other)

    def findall(self, other: TYPING__OTHER_DRAFT) -> TYPING__RE_RESULT__ALL:
        other = str(other)
        result = []
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF, 0]).get_first_is_not_none()

            result_i = re.findall(rexp.PAT, other, flags)
            if result_i:
                if self.ATTEMPTS_USAGE == AttemptsUsage.FIRST:
                    return result_i
                else:
                    result.append(*result_i)

        return result


# =====================================================================================================================
@final
class ReAttemptsFirst(Base_ReAttempts):
    ATTEMPTS_USAGE = AttemptsUsage.FIRST


@final
class ReAttemptsAll(Base_ReAttempts):
    ATTEMPTS_USAGE = AttemptsUsage.ALL


# =====================================================================================================================
