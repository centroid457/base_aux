from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
class RExp(Base_AttrKit):
    """
    GOAL
    ----
    simple pattern with all expected params for batch usage

    RULES
    -----
    default methods use only None! to be ensure what would be replaced!
    """
    PAT: str
    FLAGS: int | None = None
    SUB: str = None     # used only for sub/del methods!
    SCOUNT: int = 0     # used only for sub/del methods!


# =====================================================================================================================
TYPING__REXP_DRAFT = str | RExp
TYPING__REXPS_FINAL = Iterable[RExp]


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
