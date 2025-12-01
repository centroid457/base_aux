from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.base_nest_dunders.m7_cmp import *


# =====================================================================================================================
class Uptime(NestCmp_GLET_DigitAccuracy):
    """
    GOAL
    ----
    simplest way to check time passed from started

    SPECIALLY CREATED FOR
    ---------------------
    tests
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.time_started: float = time.time()
        self.time_stopped: float | None = None

    @property
    def CMP_VALUE(self) -> TYPING.DIGIT_FLOAT_INT:
        return self.get()

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


# =====================================================================================================================
