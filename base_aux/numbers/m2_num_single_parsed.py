from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_text.m1_text_aux import *
from base_aux.base_nest_dunders.m1_init1_source import *

from base_aux.base_types.m0_static_types import TYPES


# =====================================================================================================================
class _NumParsedSingle(NestInit_Source, NestCall_Resolve):
    SOURCE: TYPES.NUMBER = None

    _numtype: EnumAdj_NumType = EnumAdj_NumType.BOTH

    def _init_post(self) -> None | NoReturn:
        self.SOURCE = TextAux(self.SOURCE).parse__number_single(num_type=self._numtype)

    def resolve(self) -> TYPES.NUMBER | None:
        return self.SOURCE


# ---------------------------------------------------------------------------------------------------------------------
@final
class NumParsedSingle(_NumParsedSingle):
    pass


@final
class NumParsedSingleInt(_NumParsedSingle):
    _numtype: EnumAdj_NumType = EnumAdj_NumType.INT


@final
class NumParsedSingleFloat(_NumParsedSingle):
    _numtype: EnumAdj_NumType = EnumAdj_NumType.FLOAT


# =====================================================================================================================
