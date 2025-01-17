from typing import *

from base_aux.base_source.m1_source import InitSource


# =====================================================================================================================
@final
class ValidLG(InitSource):
    """
    Try to keep all validating funcs in separated place
    """
    # FIXME: do smth! before it was all static! and source at first place!
    SOURCE: Any

    def ltgt(self, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        if low is not None:
            result &= self.SOURCE > low
        if high is not None:
            result &= self.SOURCE < high
        return result

    def ltge(self, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        if low is not None:
            result &= self.SOURCE > low
        if high is not None:
            result &= self.SOURCE <= high
        return result

    def legt(self, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        if low is not None:
            result &= self.SOURCE >= low
        if high is not None:
            result &= self.SOURCE < high
        return result

    def lege(self, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        if low is not None:
            result &= self.SOURCE >= low
        if high is not None:
            result &= self.SOURCE <= high
        return result


# =====================================================================================================================
