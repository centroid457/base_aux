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
    time_started: float

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.time_started = time.time()

    # -----------------------------------------------------------------------------------------------------------------
    def get(self) -> float:
        """
        GOAL
        ----
        return time passed from start (initial time)
        """
        return time.time() - self.time_started

    # -----------------------------------------------------------------------------------------------------------------
    def check_lt(self, other: float, accuracy: float = 0) -> bool: raise NotImplementedError()
    def check_le(self, other: float, accuracy: float = 0) -> bool: raise NotImplementedError()
    def check_gt(self, other: float, accuracy: float = 0) -> bool: raise NotImplementedError()
    def check_ge(self, other: float, accuracy: float = 0) -> bool: raise NotImplementedError()

    # TODO: add __cmp__/__eq__


# =====================================================================================================================
