from typing import *

from base_aux.aux_values.m0_novalue import *
from base_aux.base_inits.m2_source_kwargs import *
from base_aux.aux_text.m1_text_aux import *


# =====================================================================================================================
# @final
class ValidAux(InitSource):
    """
    Try to keep all validating funcs in separated place
    """
    # FIXME: do smth! before it was all static! and source at first place!
    SOURCE: Any = None

    def ltgt(self, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        # low ----------
        if low is not None:
            result &= self.SOURCE > low
        if not result:
            return False
        # high ----------
        if high is not None:
            result &= self.SOURCE < high
        # final ----------
        return result

    def ltge(self, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        # low ----------
        if low is not None:
            result &= self.SOURCE > low
        if not result:
            return False
        # high ----------
        if high is not None:
            result &= self.SOURCE <= high
        # final ----------
        return result

    def legt(self, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        # low ----------
        if low is not None:
            result &= self.SOURCE >= low
        if not result:
            return False
        # high ----------
        if high is not None:
            result &= self.SOURCE < high
        # final ----------
        return result

    def lege(self, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        result = True
        # low ----------
        if low is not None:
            result &= self.SOURCE >= low
        if not result:
            return False
        # high ----------
        if high is not None:
            result &= self.SOURCE <= high
        # final ----------
        return result


# =====================================================================================================================
@final
class ValidAux_Obj(ValidAux):
    """
    cmp will be executed by direct object without modification
    """
    SOURCE: Any = None


# =====================================================================================================================
@final
class ValidAux_SingleNumParsed(ValidAux):
    """
    cmp will be executed by parse single num from STR(source)
    """
    SOURCE: int | float | None = None
    _fpoint: FPoint = FPoint.DOT

    def __init__(self, source: Any = NoValue, *args, fpoint: FPoint = FPoint.DOT, **kwargs) -> None | NoReturn:
        if fpoint:
            self._fpoint = FPoint(fpoint)
        super().__init__(source=source, *args, **kwargs)

    def init_post(self) -> None:
        self.SOURCE = TextAux(self.SOURCE).parse__single_number(fpoint=self._fpoint)


# =====================================================================================================================
