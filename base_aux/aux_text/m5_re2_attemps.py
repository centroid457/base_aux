from base_aux.aux_text.m5_re1_rexp import *
from base_aux.aux_iter.m1_iter_aux import *
from base_aux.base_values.m3_exceptions import *


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
    ATTEMPTS_USAGE
    if FIRST - return result for first match function in attempt order
    if ALL - return list of results for all matched attempts
    """
    ATTEMPTS: TYPING__REXPS_FINAL
    FLAGS_DEF: int = None
    ATTEMPTS_USAGE: EnumAdj_AttemptsUsage = EnumAdj_AttemptsUsage.ALL

    def __init__(self, *attempts: TYPING__REXP_DRAFT, flags_def: int = None, attempts_usage: EnumAdj_AttemptsUsage = None) -> None:
        if flags_def is not None:
            self.FLAGS_DEF = flags_def

        if attempts_usage is not None:
            self.ATTEMPTS_USAGE = EnumAdj_AttemptsUsage(attempts_usage)

        result = []
        for attempt in attempts:
            if isinstance(attempt, RExp):
                result.append(attempt)
            elif isinstance(attempt, str):
                result.append(RExp(attempt))
            else:
                raise Exc__Incompatible_Data(f"{attempt=}")

        self.ATTEMPTS = result

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _result__get_from_match(match: re.Match) -> TYPING__RE_RESULT__ONE:
        """
        NOTE
        ----
        this is one of the the main idea for whole this class!

        GOAL
        ----
        get result from match object
        1. if no groups - return matching string
        2. if one group - return exact the group value
        3. if several groups - return tuple of groups
        """
        if not isinstance(match, re.Match):
            raise Exc__WrongUsage(f"{match=}")

        groups = match.groups()
        if groups:
            if len(groups) == 1:
                return groups[0]
            else:
                return groups
        else:
            return match.group()

    # -----------------------------------------------------------------------------------------------------------------
    pass

    # return None only for FIRST! if ALL - retrun always LIST!

    def match(self, other: TYPING__OTHER_DRAFT) -> TYPING__RE_RESULT__ALL | None:
        other = str(other)
        result = []
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF, 0]).get_first_is_not_none()

            match = re.match(rexp.PAT, other, flags)
            if match:
                result_i = self._result__get_from_match(match)
                if self.ATTEMPTS_USAGE == EnumAdj_AttemptsUsage.FIRST:
                    return result_i
                else:
                    result.append(result_i)

        # finish
        if self.ATTEMPTS_USAGE == EnumAdj_AttemptsUsage.FIRST:
            return None
        else:
            return result

    def fullmatch(self, other: TYPING__OTHER_DRAFT) -> TYPING__RE_RESULT__ALL | None:
        other = str(other)
        result = []
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF, 0]).get_first_is_not_none()

            match = re.fullmatch(rexp.PAT, other, flags)
            if match:
                result_i = self._result__get_from_match(match)
                if self.ATTEMPTS_USAGE == EnumAdj_AttemptsUsage.FIRST:
                    return result_i
                else:
                    result.append(result_i)
        # finish
        if self.ATTEMPTS_USAGE == EnumAdj_AttemptsUsage.FIRST:
            return None
        else:
            return result

    def search(self, other: TYPING__OTHER_DRAFT) -> TYPING__RE_RESULT__ALL | None:
        other = str(other)
        result = []
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF, 0]).get_first_is_not_none()

            match = re.search(rexp.PAT, other, flags)
            if match:
                result_i = self._result__get_from_match(match)
                if self.ATTEMPTS_USAGE == EnumAdj_AttemptsUsage.FIRST:
                    return result_i
                else:
                    result.append(result_i)
        # finish
        if self.ATTEMPTS_USAGE == EnumAdj_AttemptsUsage.FIRST:
            return None
        else:
            return result

    # -----------------------------------------------------------------------------------------------------------------
    def findall(self, other: TYPING__OTHER_DRAFT) -> list[TYPING__RE_RESULT__ONE]:
        other = str(other)
        result = []
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF, 0]).get_first_is_not_none()

            result_i = re.findall(rexp.PAT, other, flags)
            if result_i:
                if self.ATTEMPTS_USAGE == EnumAdj_AttemptsUsage.FIRST:
                    return result_i
                else:
                    result.extend(result_i)

        return result

    # -----------------------------------------------------------------------------------------------------------------
    def sub(self, other: TYPING__OTHER_DRAFT, new: str = None) -> str:
        other = str(other)
        result = other
        for rexp in self.ATTEMPTS:
            flags = IterAux([rexp.FLAGS, self.FLAGS_DEF, 0]).get_first_is_not_none()
            new = IterAux([rexp.SUB, new, ""]).get_first_is_not_none()
            count = IterAux([rexp.SCOUNT, 0]).get_first_is_not_none()

            result = re.sub(rexp.PAT, new, other, count, flags)
            if result != other:
                other = result
                if self.ATTEMPTS_USAGE == EnumAdj_AttemptsUsage.FIRST:
                    break

        return result

    def delete(self, other: TYPING__OTHER_DRAFT) -> str:
        return self.sub(other)


# =====================================================================================================================
@final
class ReAttemptsFirst(Base_ReAttempts):
    ATTEMPTS_USAGE = EnumAdj_AttemptsUsage.FIRST


@final
class ReAttemptsAll(Base_ReAttempts):
    ATTEMPTS_USAGE = EnumAdj_AttemptsUsage.ALL


# =====================================================================================================================
