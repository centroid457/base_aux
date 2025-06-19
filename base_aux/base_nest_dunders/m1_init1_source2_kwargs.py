from base_aux.aux_argskwargs.m2_argskwargs_aux import *
from base_aux.aux_values.m2_types import *
from base_aux.aux_values.m2_typing import TYPING


# =====================================================================================================================
class NestInit_SourceKwArgs_Implicit(NestInit_Source):
    """
    NOTE
    ----
    NestInit_SourceKwArgs_Explicite is more useful!

    GOAL
    ----
    just to make inition source with KwArgs
    """
    ARGS: TYPING.ARGS_FINAL
    KWARGS: TYPING.KWARGS_FINAL

    def __init__(self, source: Any = None, *args, **kwargs) -> None:
        self.ARGS = args
        self.KWARGS = kwargs
        super().__init__(source)


# =====================================================================================================================
class NestInit_SourceKwArgs_Explicite(NestInit_Source):
    """
    MORE USEFUL THEN NestInit_SourceKwArgs_Implicit

    GOAL
    ----

    FOR PYTESTAUX!
    """
    ARGS: TYPING.ARGS_FINAL
    KWARGS: TYPING.KWARGS_FINAL

    def __init__(self, source: Any = None, args: TYPING.ARGS_DRAFT = (), kwargs: TYPING.KWARGS_DRAFT = None, *args2, **kwargs2) -> None:
        self.ARGS = ArgsKwargsAux(args).resolve_args()
        self.KWARGS = ArgsKwargsAux(kwargs).resolve_kwargs()
        super().__init__(source, *args2, **kwargs2)


# =====================================================================================================================
