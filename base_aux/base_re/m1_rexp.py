from typing import *
import re

from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
class RExp(Nest_AttrKit):
    """
    GOAL
    ----
    simple pattern with all expected params

    RULES
    -----
    default methods use only None! to be ensure what would be replaced!
    """
    PAT: str
    FLAGS: int | None = None
    SUB: str = None     # used only for sub/del methods!


# =====================================================================================================================
TYPING__REXP_ATTEMTS = Iterable[str | RExp]


# =====================================================================================================================
if __name__ == "__main__":
    try:
        RExp()
        assert False
    except:
        pass

    assert RExp(111)[0] == 111

    assert RExp(111)[1] == None
    assert RExp(111, 222)[1] == 222

    assert RExp(111)[2] == None
    assert RExp(111, sub=333)[2] == 333
    assert RExp(111, sub=333).SUB == 333
    assert RExp(1, 2, 3, sub=333).sub == 333


# =====================================================================================================================
