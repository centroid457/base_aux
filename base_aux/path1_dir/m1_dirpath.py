from base_aux.base_statics.m1_types import *
from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_nest_dunders.m3_calls import *


# =====================================================================================================================
@final
class Resolve_DirPath(NestInit_Source, NestCall_Resolve):
    """
    GOAL
    ----
    resolve dirpath by draft

    SPECIALLY CREATED FOR
    ---------------------
    Resolve_FilePath init dirpath
    """
    SOURCE: TYPING.PATH_DRAFT | None

    def resolve(self) -> TYPING.PATH_FINAL:
        if self.SOURCE is not None:
            return pathlib.Path(self.SOURCE)
        if self.SOURCE is None:
            return pathlib.Path().cwd()


# =====================================================================================================================
