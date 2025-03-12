from base_aux.base_statics.m1_types import *
from base_aux.aux_text.m1_text_aux import *
from base_aux.base_nest_dunders.m1_init1_source import *


# =====================================================================================================================
# @final
class ValidAux(NestInit_Source):
    """
    Try to keep all validating funcs in separated place
    """
    # FIXME: do smth! before it was all static! and source at first place!
    SOURCE: Any = None

    def eq(self, other: Any) -> bool | NoReturn:
        return NotImplemented

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
class ValidAux_NumParsedSingle(ValidAux):
    """
    cmp will be executed by parse single num from STR(source)
    """
    SOURCE: TYPES.NUMBER | None = None

    def init_post(self) -> None:
        self.SOURCE = TextAux(self.SOURCE).parse__number_single()

    def eq(self, other: Any | None | bool | Union[NumType | int | float]) -> bool:
        if other is True:
            return self.SOURCE is not None

        elif other in [False, None, NoValue]:
            return self.SOURCE is None

        elif other in NumType:
            return TextAux(self.SOURCE).parse__number_single(num_type=other) is not None

        else:
            return self.SOURCE == TextAux(other).parse__number_single()


# =====================================================================================================================
