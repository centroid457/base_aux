from typing import *
import sys

from base_aux.base_nest_dunders.m1_init1_source import *


# =====================================================================================================================
class Warn(NestInit_Source):
    """
    GOAL
    ----
    when you dont want to use logger and raise error (by now).
    print msg in some inner functions when raising Exx after inner function return False.

    SPECIALLY CREATED FOR
    ---------------------
    ReleaseHistory.check_new_release__is_correct/generate

    TODO: try use direct logger?
    """
    SOURCE: str

    def init_post(self) -> None | NoReturn:
        self.SOURCE = f"[WARN]{self.SOURCE}"
        print(self.SOURCE, file=sys.stderr)


# =====================================================================================================================
if __name__ == "__main__":
    Warn(123)


# =====================================================================================================================
