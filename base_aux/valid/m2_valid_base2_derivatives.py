import time
from base_aux.valid.m2_valid_base import Valid


# =====================================================================================================================
# RETRY ---------------------------------------------------------------------------------------------------------------
class ValidRetry1(Valid):
    """
    CREATED SPECIALLY FOR
    ---------------------
    eltech_testplans make retry while testing Serial(Uart) validation responses by sending RESET with ensure result!
    """
    VALIDATE_RETRY = 1


class ValidRetry2(Valid):
    VALIDATE_RETRY = 2


# CONTINUE ------------------------------------------------------------------------------------------------------------
class ValidFailStop(Valid):
    """
    just a derivative
    """
    CHAIN__FAIL_STOP = True


class ValidFailContinue(Valid):
    """
    just a derivative
    """
    CHAIN__FAIL_STOP = False


# CHANGE RESULT -------------------------------------------------------------------------------------------------------
class ValidNoCum(Valid):
    """
    just a derivative

    you can use it as a stub in chains
    """
    CHAIN__CUM = False


class ValidReverse(Valid):
    """
    reverse direct valid result (if finished)
    """
    REVERSE_LINK = True


# =====================================================================================================================
class ValidSleep(ValidNoCum):
    """
    GOAL
    ----
    UTIL
    just make a pause in chain
    """
    NAME = "ValidSleep"
    VALIDATE_LINK = None

    def __init__(self, secs: float = 1, skip_link: bool = None):
        super().__init__(value_link=time.sleep, args__value=secs, skip_link=skip_link)


# ---------------------------------------------------------------------------------------------------------------------
class ValidBreak(ValidNoCum):
    """
    GOAL
    ----
    UTIL
    exit chain on some step

    when True - just exit chain with last Cum chain result
    when False - just noCum and continue process
    """
    NAME = "ValidBreak"


# =====================================================================================================================
