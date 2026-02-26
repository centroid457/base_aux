import sys
from typing import *

from base_aux.base_nest_dunders.m3_bool import NestBool_False


# =====================================================================================================================
class Print:
    """
    GOAL
    ----
    print multy lines msg in stdout

    SPECIALLY CREATED FOR
    ---------------------
    Base for Warn

    TODO: try use direct logger?
        or rename into some new class! as universal Msging!
    """
    OUTPUT: TextIO = sys.stdout
    PREFIX: str = "[INFO]"

    INDENT: str = "__"
    EOL: str = "\n"
    MSG_LINES: tuple[str, ...]

    def __init__(self, *lines, prefix: str | None = None, noprint: bool | None = None, **kwargs) -> None:
        self.MSG_LINES = lines
        if prefix is not None:
            self.PREFIX = prefix

        if not noprint:
            print(self, file=self.OUTPUT)

            if self.OUTPUT == sys.stderr:
                # additional print - cause of stderr prints not in same
                print(self, file=sys.stdout)

        super().__init__(**kwargs)

    def __str__(self):
        return self.MSG_STR

    @property
    def MSG_STR(self) -> str:
        result = f"{self.PREFIX}"
        for index, line in enumerate(self.MSG_LINES):
            if index == 0:
                result += f"{line}"
            else:
                result += f"{self.EOL}{self.INDENT}{line}"

        return result


# =====================================================================================================================
class Warn(
    Print,

    NestBool_False,
):
    """
    GOAL
    ----
    when you dont want to use logger and raise error (by now).
    print msg in some inner functions when raising Exc after inner function return False.

    SPECIALLY CREATED FOR
    ---------------------
    ReleaseHistory.check_new_release__is_correct/generate
    """
    OUTPUT: TextIO = sys.stderr
    PREFIX: str = "[WARN]"


# =====================================================================================================================
