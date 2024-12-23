from typing import *
import re


# =====================================================================================================================
class CmdArgsKwargsParser:
    """
    ALL RESULTS IN LOWERCASE! (EXCEPT SOURCE!)

    GOAL
    ----
    parse string line for Cmd with args Kwargs with syntax
        "prefix cmdName arg1 arg2 kwarg1=val1 kwarg2=val2"
    get exact values prefix/CMD/Args/Kwargs

    SPECIALLY CREATED FOR
    ---------------------
    buses.serialClient
    """
    # INITS ------------
    SOURCE: str = None
    PREFIX_EXPECTED: str = ""

    # RESULTS ------------
    PREFIX: str = ""
    CMD: str = ""

    ARGS: list[str]
    KWARGS: dict[str, str]

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, source: str, prefix_expected: Optional[str] = None):
        self.SOURCE = str(source)

        prefix_expected = prefix_expected or ""
        self.PREFIX_EXPECTED = prefix_expected.lower()

        self.ARGS = []
        self.KWARGS = {}

        self.parse()

    # -----------------------------------------------------------------------------------------------------------------
    def parse(self) -> None:
        # SOURCE fix ---------
        source = self.SOURCE.lower()
        source = re.sub(r"\s*=+\s*", "=", source)

        # PREFIX -------------
        if self.PREFIX_EXPECTED and source.startswith(self.PREFIX_EXPECTED):
            self.PREFIX = self.PREFIX_EXPECTED

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

    # -----------------------------------------------------------------------------------------------------------------
    def ARGS_count(self) -> int:
        return len(self.ARGS)

    def KWARGS_count(self) -> int:
        return len(self.KWARGS)


# =====================================================================================================================
