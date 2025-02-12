from base_aux.base_statics.m1_types import *
from base_aux.base_resolver.m1_resolver import *
from base_aux.aux_text.m1_text_aux import *
from base_aux.base_inits.m1_source import *


# =====================================================================================================================
class _NumParsedSingle(Init_Source, NestCall_Resolve):
    SOURCE: TYPES.NUMBER = None

    _numtype: NumType = NumType.BOTH

    def init_post(self) -> None | NoReturn:
        self.SOURCE = TextAux(self.SOURCE).parse__number_single(num_type=self._numtype)

    def resolve(self) -> TYPES.NUMBER | None:
        return self.SOURCE


# ---------------------------------------------------------------------------------------------------------------------
@final
class NumParsedSingle(_NumParsedSingle):
    pass


@final
class NumParsedSingleInt(_NumParsedSingle):
    _numtype: NumType = NumType.INT


@final
class NumParsedSingleFloat(_NumParsedSingle):
    _numtype: NumType = NumType.FLOAT


# =====================================================================================================================
