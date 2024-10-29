import time

from funcs_aux import Valid, TYPE__VALIDATE_LINK


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
    VALIDATE_REVERSE = True


# UTILS ---------------------------------------------------------------------------------------------------------------
class ValidSleep(ValidNoCum):
    """
    just a derivative - to make a pause in chains
    """
    NAME = "Sleep"
    VALIDATE_LINK: TYPE__VALIDATE_LINK = None

    def __init__(self, secs: float = 1):
        super().__init__(value_link=time.sleep, args__value=secs)


# =====================================================================================================================
