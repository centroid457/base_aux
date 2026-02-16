from typing import *

from base_aux.aux_text.m1_text_aux import *
from base_aux.base_nest_dunders.m1_init1_source import *
# from base_aux.base_resolver.m1_resolver import *


# =====================================================================================================================
@final
class WildCardMask(NestInit_Source):
    """
    GOAL
    ----
    _shell_cmd-style wildcards
    just transform WcMask to regexp

    SPECIALLY CREATED FOR
    ---------------------
    work with files(glob)/words by simple old human wildcard mask
    """
    SOURCE: str = "*"

    RULES: dict[str, str] = {
        # PAT: NEW,
        # [+?. * ^ $ ( ) [] {} |] -

        # CHAR -----------
        # brackets ----
        r"\[": "\[",
        r"\]": "\]",

        r"\(": "\(",
        r"\)": "\)",

        r"\{": "\{",
        r"\}": "\}",

        # char ----
        r"\.": "\.",  # keep first!
        r"\+": "\+",
        r"\^": "\^",
        r"\$": "\$",
        r"\|": "\|",

        # MASK -----------
        r"\*": ".*",
        r"\?": ".{0,1}",
    }

    def to_regexp(self) -> str:
        return TextAux(self.SOURCE).sub__regexps(*self.RULES.items())


# =====================================================================================================================
