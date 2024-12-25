from typing import *


# =====================================================================================================================
class InitSource:
    """
    GOAL
    ----
    just show that class uses init with source - one param
    means inside instance all methods will work on it!
    and all params for methods belong to methods! not about new source!

    SPECIALLY CREATED FOR
    ---------------------
    apply in AttrAux and same others
    """
    SOURCE: Any = None

    def __init__(self, source: Any = None) -> None:
        if source is not None:
            self.SOURCE = source


# =====================================================================================================================
