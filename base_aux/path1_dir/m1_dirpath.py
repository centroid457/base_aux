from typing import *
import pathlib

from base_aux.base_statics.m1_types import TYPE__PATH_DRAFT, TYPE__PATH_FINAL
from base_aux.base_inits.m1_source import Init_Source
from base_aux.base_resolver.m1_resolver import NestCall_Resolve


# =====================================================================================================================
@final
class Resolve_DirPath(Init_Source, NestCall_Resolve):
    """
    GOAL
    ----
    resolve dirpath by draft

    SPECIALLY CREATED FOR
    ---------------------
    Resolve_FilePath init dirpath
    """
    SOURCE: TYPE__PATH_DRAFT | None

    def resolve(self) -> TYPE__PATH_FINAL:
        if self.SOURCE is not None:
            return pathlib.Path(self.SOURCE)
        if self.SOURCE is None:
            return pathlib.Path().cwd()


# =====================================================================================================================
