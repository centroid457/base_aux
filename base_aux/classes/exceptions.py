from typing import *


# =====================================================================================================================
class ExxBool(Exception):
    """
    just a solution to bet correct bool if get Exx as value

    SPECIALLY CREATED FOR
    ---------------------
    classes.VALID if
    """
    def __bool__(self):
        return False


# =====================================================================================================================
if __name__ == '__main__':
    # REASON --------------
    assert bool(Exception(0)) is True
    assert bool(Exception(False)) is True

    # SOLUTION --------------
    assert bool(ExxBool(0)) is False
    assert bool(ExxBool(False)) is False


# =====================================================================================================================
