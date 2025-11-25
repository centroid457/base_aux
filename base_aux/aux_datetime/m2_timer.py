import datetime
import time

from base_aux.aux_attr.m1_annot_attr1_aux import *


# =====================================================================================================================
class Timer:
    """
    GOAL
    ----
    create (at last) timer to check time passed
    """
    def __init__(self):
        self.started: float = time.time()

    def check(self) -> float:
        """
        GOAL
        ----
        return time passed from start
        """
        return time.time() - self.started


# =====================================================================================================================
