from typing import *


# =====================================================================================================================
class Resolver:
    """
    GOAL
    ----
    ability to get dict from objects

    SPECIALLY CREATED FOR
    ---------------------
    dump attrs with values in gitMark
    """
    SOURCE: Any

    def __init__(self, source: Any):
        self.SOURCE = source

    def resolve(self) -> dict[str, Any]:
        pass


# =====================================================================================================================
