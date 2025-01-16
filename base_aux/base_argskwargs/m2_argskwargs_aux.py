from typing import *
from base_aux.base_source import *
from base_aux.base_argskwargs.m0_args_ensure import *
from base_aux.base_argskwargs.m1_argskwargs import *


# =====================================================================================================================
class ArgsKwargsAux(InitSource):
    SOURCE: TYPE__ARGS_DRAFT | TYPE__KWARGS_DRAFT

    def resolve_args(self) -> TYPE__ARGS_FINAL:
        if isinstance(self.SOURCE, ArgsKwargs):
            return self.SOURCE.ARGS

    def resolve_kwargs(self) -> TYPE__KWARGS_FINAL:
        if isinstance(self.SOURCE, ArgsKwargs):
            return self.SOURCE.KWARGS



# =====================================================================================================================
