from typing import *

from base_aux.base_inits.m1_source import *
from base_aux.aux_types.m1_type_aux import TypeAux

from base_aux.aux_argskwargs.m1_argskwargs import ArgsKwargs, TYPE__ARGS_DRAFT, TYPE__KWARGS_DRAFT
from base_aux.aux_types.m0_types import TYPE__ARGS_FINAL, TYPE__KWARGS_FINAL


# =====================================================================================================================
@final
class ArgsKwargsAux(InitSource):
    SOURCE: TYPE__ARGS_DRAFT | TYPE__KWARGS_DRAFT

    def resolve_args(self) -> TYPE__ARGS_FINAL:     # REPLACING for args__ensure_tuple
        if isinstance(self.SOURCE, ArgsKwargs):
            return self.SOURCE.ARGS
        elif TypeAux(self.SOURCE).check__elementary_collection():
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
