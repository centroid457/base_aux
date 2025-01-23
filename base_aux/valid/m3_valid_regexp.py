from typing import *
import re

from base_aux.cmp.m2_eq import EqAux


# =====================================================================================================================
class ValidRegExp:
    """
    GOAL
    ----
    use ready object to validate by comparing with others

    SPECIALLY CREATED FOR
    ---------------------
    buses.serial_client.SerialClient.write_read__last_validate_regexp
    replace write_read__last_validate_regexp by using only write_read__last_validate with this object as expected.

    BEST USAGE
    ----------
    OBJECT cmp
        assert 1 == ValidRegExp(r"\\d?")
        assert 1 == ValidRegExp([r"\\d?", r"\\s*\\d?"])
    METHOD check
        assert ValidRegExp(r"\\d?").run(1)

    """
    REGEXPS: Iterable[str] = None
    IGNORECASE: bool = True

    def __init__(self, regexps: str | Iterable[str] = None, ignorecase: bool = None):
        if ignorecase is not None:
            self.IGNORECASE = ignorecase

        if regexps:
            self.REGEXPS = regexps

        if isinstance(self.REGEXPS, str):
            self.REGEXPS = [self.REGEXPS, ]

    def __eq__(self, other: Any) -> bool:
        if not self.REGEXPS:
            return True

        for pattern in self.REGEXPS:
            if re.fullmatch(pattern=str(pattern), string=str(other), flags=re.RegexFlag.IGNORECASE if self.IGNORECASE else 0):
                return True
        return False

    def run(self, source: Any) -> bool:
        return EqAux(self).check_doubleside__bool(source)


# =====================================================================================================================
