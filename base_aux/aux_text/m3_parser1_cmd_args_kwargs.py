from typing import *
import re


# =====================================================================================================================
class CmdArgsKwargsParser:
    """
    GOAL
    ----
    parse string line for Cmd with args Kwargs with syntax
        "prefix cmdName arg1 arg2 kwarg1=val1 kwarg2=val2"
    get exact values prefix/CMD/Args/Kwargs

    NOTE
    ----
    ALL RESULTS IN LOWERCASE! (EXCEPT SOURCE!)

    SPECIALLY CREATED FOR
    ---------------------
    buses.serialClient
    """
    # INITS ------------
    SOURCE: str

    # RESULTS ------------
    PREFIX: str = ""
    CMD: str = ""

    ARGS: list[str]
    KWARGS: dict[str, str]

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, source: str, prefix_expected: str = None):
        self.SOURCE = str(source)

        self.ARGS = []
        self.KWARGS = {}

        self.parse(prefix_expected=prefix_expected)

    # -----------------------------------------------------------------------------------------------------------------
    def parse(self, prefix_expected: str = None) -> None:
        # SOURCE fix ---------
        source = self.SOURCE.lower()
        source = re.sub(r"\s*=+\s*", "=", source)

        # PREFIX -------------
        prefix_expected = prefix_expected or ""
        prefix_expected = prefix_expected.lower()

        if prefix_expected and source.startswith(prefix_expected):
            self.PREFIX = prefix_expected

            source = source.replace(self.PREFIX, "", 1)

        # --------------------
        splits = source.split()
        if not splits:
            return

        # ARGS/KWARGS ----------------
        for part in splits:
            if "=" not in part:
                if not self.CMD:
                    self.CMD = part
                else:
                    self.ARGS.append(part)
            else:
                part__key_value = part.split("=")
                self.KWARGS.update(dict([part__key_value, ]))


# =====================================================================================================================
