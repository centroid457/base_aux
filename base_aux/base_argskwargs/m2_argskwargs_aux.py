from typing import *
from base_aux.base_source import *
from base_aux.base_objects import *
from base_aux.base_argskwargs.m1_argskwargs import *


# =====================================================================================================================
class ArgsKwargsAux(InitSource):
    SOURCE: TYPE__ARGS_DRAFT | TYPE__KWARGS_DRAFT

    def resolve_args(self) -> TYPE__ARGS_FINAL:     # REPLACING for args__ensure_tuple
        if isinstance(self.SOURCE, ArgsKwargs):
            return self.SOURCE.ARGS
        elif TypeCheck(self.SOURCE).check__elementary_collection():
            return tuple(self.SOURCE)
        else:
            return (self.SOURCE,)

    def resolve_kwargs(self) -> TYPE__KWARGS_FINAL | NoReturn:
        if isinstance(self.SOURCE, ArgsKwargs):
            return self.SOURCE.KWARGS
        elif not self.SOURCE:
            return {}
        else:
            return dict(self.SOURCE)


# =====================================================================================================================
