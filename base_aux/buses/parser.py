from . import *

from typing import *
import re


# =====================================================================================================================
class CmdArgsKwargsParser:
    """
    ALL RESULTS IN LOWERCASE! (EXCEPT ORIGINAL ORIGINAL!)

    GOAL
    ----
    parse string line for Cmd with args Kwargs with syntax
        "prefix cmdName arg1 arg2 kwarg1=val1 kwarg2=val2"
    get exact values prefix/CMD/Args/Kwargs
    """
    # REAL STATE --------------
    ORIGINAL: str
    PREFIX: str
    CMD: str
    ARGS: list[str]
    KWARGS: dict[str, str]

    # AUX ---------------------
    _PREFIX_EXPECTED: str

    def __init__(self, line: str, _prefix_expected: Optional[str] = None):
        # LINE ----------------
        line = str(line)
        line_lower = line.lower()

        # INIT ----------------
        self.ORIGINAL = line
        self.PREFIX = ""
        self.CMD = ""
        self.ARGS = []
        self.KWARGS = {}

        # PREFIX ----------------
        _prefix_expected = _prefix_expected or ""
        self._PREFIX_EXPECTED = _prefix_expected.lower()
        if _prefix_expected and line_lower.startswith(_prefix_expected):
            self.PREFIX = _prefix_expected
            line_lower = line_lower.replace(_prefix_expected, "", 1)

        # BLANK ----------------------
        if not line_lower:
            return

        line_lower = re.sub(r"\s*=+\s*", "=", line_lower)
        line_parts = line_lower.split()
        if not line_parts:
            return

        # ARGS/KWARGS ----------------
        for part in line_parts:
            if "=" not in part:
                self.ARGS.append(part)
            else:
                part__key_value = part.split("=")
                self.KWARGS.update(dict([part__key_value, ]))

        # CMD ------------------------
        if self.ARGS:
            self.CMD = self.ARGS[0]
            self.ARGS = self.ARGS[1:]

    def ARGS_count(self) -> int:
        return len(self.ARGS)

    def KWARGS_count(self) -> int:
        return len(self.KWARGS)

    def parse(self) -> None:
        pass



# =====================================================================================================================
