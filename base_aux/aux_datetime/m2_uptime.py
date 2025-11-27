from base_aux.aux_attr.m1_annot_attr1_aux import *


# =====================================================================================================================
class Uptime:
    """
    GOAL
    ----
    simplest way to check time passed from started

    SPECIALLY CREATED FOR
    ---------------------

    """
    def __init__(self):
        self.started: float = time.time()

    def get(self) -> float:
        """
        GOAL
        ----
        return time passed from start (initial time)
        """
        return time.time() - self.started


# =====================================================================================================================
