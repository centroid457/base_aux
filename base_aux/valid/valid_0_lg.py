from typing import *


# =====================================================================================================================
class ValidLg:
    """
    Try to keep all validating funcs in separated place
    """

    @staticmethod
    def ltgt(source: Any, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        """
        NOTE
        ----
        1. important to keep source at first place!
        """
        result = True
        if low is not None:
            result &= source > low
        if high is not None:
            result &= source < high
        return result

    @staticmethod
    def ltge(source: Any, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        if low is not None:
            result &= source > low
        if high is not None:
            result &= source <= high
        return result

    @staticmethod
    def legt(source: Any, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        if low is not None:
            result &= source >= low
        if high is not None:
            result &= source < high
        return result

    @staticmethod
    def lege(source: Any, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        if low is not None:
            result &= source >= low
        if high is not None:
            result &= source <= high
        return result


# =====================================================================================================================
