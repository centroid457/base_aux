from typing import *
from dataclasses import dataclass


# =====================================================================================================================
@dataclass
class TimeoutDef:
    """
    GOAL
    ----
    keep default set of values for timeout
    and get updated final state
    """
    WRITE: float | None
    READ_START: float | None
    READ_FINISH: float | None    # specially for cmds like ping with pauses between msg pack

    def change(
            self,
            write: float | None = None,
            read_start: float | None = None,
            read_finish: float | None = None,
    ) -> None:
        """
        GOAL
        ----
        update object from default state
        """
        if write is not None:
            self.WRITE = write
        if read_start is not None:
            self.READ_START = read_start
        if read_finish is not None:
            self.READ_FINISH = read_finish

    def get_active__write(
            self,
            other: float | None = None,
    ) -> float:
        if other is not None:
            return other
        else:
            return self.WRITE

    def get_active__read_start(
            self,
            other: float | None = None,
    ) -> float:
        if other is not None:
            return other
        else:
            return self.READ_START

    def get_active__read_finish(
            self,
            other: float | None = None,
    ) -> float:
        if other is not None:
            return other
        else:
            return self.READ_FINISH


# =====================================================================================================================
