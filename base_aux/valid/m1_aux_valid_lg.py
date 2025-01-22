from typing import *

from base_aux.aux_values.m0_novalue import *
from base_aux.base_source.m2_source_kwargs import *


# =====================================================================================================================
@final
class ValidAux(InitSourceKwArgs_Explicite):
    """
    Try to keep all validating funcs in separated place
    """
    # FIXME: do smth! before it was all static! and source at first place!
    SOURCE: Any = NoValue

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
