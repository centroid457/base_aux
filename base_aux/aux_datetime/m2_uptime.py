from base_aux.aux_attr.m1_annot_attr1_aux import *


# =====================================================================================================================
class Uptime:
    """
    GOAL
    ----
    simplest way to check time passed from started

    SPECIALLY CREATED FOR
    ---------------------
    tests
    """
    def __init__(self, accuracy: float = 0):
        self.accuracy: float = accuracy

        self.time_started: float = time.time()
        self.time_stopped: float | None = None

    def restart(self) -> None:
        self.time_started = time.time()
        self.time_stopped = None

    def stop(self) -> float:
        self.time_stopped = time.time()
        return self.get()

    # -----------------------------------------------------------------------------------------------------------------
    def get(self) -> float:
        """
        GOAL
        ----
        return time passed from start (initial time)
        """
        if self.time_stopped:
            return self.time_stopped - self.time_started
        else:
            return time.time() - self.time_started

    # -----------------------------------------------------------------------------------------------------------------
    def check_lt(self, other: float, accuracy: float = 0) -> bool:
        raise NotImplementedError()

    def check_le(self, other: float, accuracy: float = 0) -> bool:
        raise NotImplementedError()

    def check_gt(self, other: float, accuracy: float = 0) -> bool:
        raise NotImplementedError()

    def check_ge(self, other: float, accuracy: float = 0) -> bool:
        raise NotImplementedError()

    # TODO: add __cmp__/__eq__


# =====================================================================================================================
