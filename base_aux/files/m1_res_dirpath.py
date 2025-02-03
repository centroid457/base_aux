from typing import *
import pathlib

from base_aux.aux_types.m0_types import TYPE__PATH_DRAFT, TYPE__PATH_FINAL
from base_aux.base_inits.m1_source import InitSource
from base_aux.base_resolver.m1_resolver import Resolver


# =====================================================================================================================
@final
class Resolve_DirPath(InitSource, Resolver):
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
