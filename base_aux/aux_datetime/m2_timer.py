import asyncio
from typing import *
import datetime
import time

from base_aux.aux_attr.m1_annot_attr1_aux import *


# =====================================================================================================================
class StopWatch:
    """
    GOAL
    ----
    create (at last) timer to check time passed
    """
    START: bool = False

    def __init__(self, start: bool = None):
        self.time_initial: float = time.time()  # TODO: deprecate? use only one?
        self.time_started: float | None = None

        if start is not None:
            if start:
                self.time_started: float = self.time_initial
        elif self.START:
            self.time_started: float = self.time_initial

    # -----------------------------------------------------------------------------------------------------------------
    def get_elapsed_time__from_start(self) -> float:
        """
        GOAL
        ----
        with/including pausing time!
        """
        return time.time() - self.time_started

    def get_execution_time__from_start(self) -> float:
        """
        GOAL
        ----
        without/not including pausing time!
        """
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    def start(self) -> None:
        raise NotImplementedError()

    def stop(self) -> None:
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    def pause(self) -> None:
        raise NotImplementedError()

    def resume(self) -> None:
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    def clear(self) -> None:
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    def wait_execution__from_start(self, target: float) -> None:
        raise NotImplementedError()

    async def aio_wait_execution__from_start(self, target: float) -> None:
        raise NotImplementedError()


# =====================================================================================================================
class StopWatchStarted(StopWatch):
    START = True


# =====================================================================================================================
