from typing import *

from base_aux.base_source.m1_source import InitSource
from base_aux.base_objects.m1_obj_types import TypeCheck

from base_aux.aux_argskwargs.m1_argskwargs import ArgsKwargs, TYPE__ARGS_DRAFT, TYPE__KWARGS_DRAFT, TYPE__ARGS_FINAL, TYPE__KWARGS_FINAL


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
