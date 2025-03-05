from typing import *


# =====================================================================================================================
class AttrDump:
    """
    GOAL
    ----
    just use static class for dumping any set!

    WHY NOT - AttrsKit
    ------------------
    cause sometimes it makes circular recursion exx!
    """

# =====================================================================================================================
def check_name__buildin(name: str) -> bool:
    return name.startswith("__") and name.endswith("__") and len(name) > 4


# =====================================================================================================================
