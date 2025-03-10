from base_aux.base_statics.m1_types import *
from base_aux.base_inits.m1_nest_init_source import NestInit_Source
from base_aux.aux_callable.m2_nest_calls import NestCall_Resolve


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
