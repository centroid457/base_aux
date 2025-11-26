import asyncio
from typing import *
import datetime
import time

from base_aux.aux_attr.m1_annot_attr1_aux import *


# =====================================================================================================================
# TODO: GET BACK simple TIMER! +use it in Stopwatch!!!???


# =====================================================================================================================
class Stopwatch:
    """
    GOAL
    ----
    create (at last) timer to check time passed
    """
    START_ON_INIT: bool = False

    def __init__(self, start: bool = None):
        self.time_initial: float = time.time()  # TODO: deprecate? use only one?
        self.time_started: float | None = None
        self.time_finished: float | None = None

        self._paused__state: bool = False
        self._paused__last_ts: float | None = None
        self._paused__summary: float = 0

        if start is not None:
            if start:
                self.time_started: float = self.time_initial
        elif self.START_ON_INIT:
            self.time_started: float = self.time_initial

    # -----------------------------------------------------------------------------------------------------------------
    def _clear(self) -> None:
        self.time_started = None
        self._paused__state = False
        self._paused__last_ts = None
        self._paused__summary = 0

    # -----------------------------------------------------------------------------------------------------------------
    def get_elapsed_time__from_start(self) -> float:
        """
        GOAL
        ----
        with/including paused time!
        """
        try:
            return time.time() - self.time_started
        except:
            return 0

    def get_execution_time__from_start(self) -> float:
        """
        GOAL
        ----
        without/not including paused time!
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
    def wait_execution__from_start(self, target: float) -> None:
        raise NotImplementedError()

    async def aio_wait_execution__from_start(self, target: float) -> None:
        raise NotImplementedError()


# =====================================================================================================================
class StopwatchStarted(Stopwatch):
    START_ON_INIT = True


# =====================================================================================================================
