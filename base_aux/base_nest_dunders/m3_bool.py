from typing import *


# =====================================================================================================================
class NestBool_False:
    """
    GOAL
    ----
    just return static False on Bool!

    SPECIALLY CREATED FOR
    ---------------------
    Base_Exx
    """
    def __bool__(self):
        return False


# =====================================================================================================================
class NestBool_True:
    """
    just a mirror for False!
    """
    def __bool__(self):
        return True


# =====================================================================================================================
class NestBool_Resolve:
    """
    SPECIALLY CREATED FOR
    ---------------------
    EqArgs
    """
    def __bool__(self):
        return self.resolve()

    def resolve(self) -> bool | NoReturn:
        return NotImplemented


# =====================================================================================================================
if __name__ == "__main__":
    for victim in [NestBool_True(), NestBool_False()]:
        result_bool_call = bool(victim)
        print(f"{result_bool_call=}")

        result_bool_if = True if victim else False
        print(f"{result_bool_if=}")


# =====================================================================================================================
