from base_aux.aux_values.m2_typing import TYPING
from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.aux_types.m1_type_aux import TypeAux

from base_aux.aux_argskwargs.m1_argskwargs import ArgsKwargs
from base_aux.aux_values.m2_types import *


# =====================================================================================================================
@final
class ArgsKwargsAux(NestInit_Source):
    SOURCE: TYPING.ARGS_DRAFT | TYPING.KWARGS_DRAFT

    def resolve_args(self) -> TYPING.ARGS_FINAL:     # REPLACING for args__ensure_tuple
        if isinstance(self.SOURCE, ArgsKwargs):
            return self.SOURCE.ARGS
        elif TypeAux(self.SOURCE).check__elementary_collection():
            return tuple(self.SOURCE)
        else:
            return (self.SOURCE,)

    def resolve_kwargs(self) -> TYPING.KWARGS_FINAL | NoReturn:
        if isinstance(self.SOURCE, ArgsKwargs):
            return self.SOURCE.KWARGS
        elif not self.SOURCE:
            return {}
        else:
            return dict(self.SOURCE)


# =====================================================================================================================
