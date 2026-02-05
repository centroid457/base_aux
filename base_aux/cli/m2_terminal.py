from typing import *

import subprocess
import time

from base_aux.loggers.m1_print import *
from base_aux.base_values.m3_exceptions import *



# =====================================================================================================================

class Terminal:
    """
    GOAL
    ----
    just an improved version of simple first
    """
    TIMEOUT: Optional[float] = 2
    RAISE: Optional[bool] = None

    CMDS_REQUIRED: Iterable[str] | dict[str, Optional[str]] | None = None

    history:
    def cli_check_available(self) -> bool:
        if self.CMDS_REQUIRED:
            for cmd, error_msg in self.CMDS_REQUIRED.items():
                if not self.send(cmd, _raise=False):
                    Print(f"cmd NOT available [{cmd}]")
                    self.print_state()
                    return False
        return True
