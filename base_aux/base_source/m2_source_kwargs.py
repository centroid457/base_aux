from typing import *

from base_aux.aux_argskwargs.m2_argskwargs_aux import *


# =====================================================================================================================
class InitSourceKwArgs_Implicite(InitSource):
    """
    NOTE
    ----
    InitSourceKwArgs_Explicite is more useful!

    GOAL
    ----
    just to make inition source with KwArgs
    """
    ARGS: TYPE__ARGS_FINAL
    KWARGS: TYPE__KWARGS_FINAL

    def __init__(self, source: Any = None, *args, **kwargs) -> None:
        self.ARGS = args
        self.KWARGS = kwargs
        super().__init__(source)


# =====================================================================================================================
class InitSourceKwArgs_Explicite(InitSource):
    """
    MORE USEFUL THEN InitSourceKwArgs_Implicite

    GOAL
    ----

    FOR PYTESTAUX!
    """
    ARGS: TYPE__ARGS_FINAL
    KWARGS: TYPE__KWARGS_FINAL

    def __init__(self, source: Any = None, args: TYPE__ARGS_DRAFT = (), kwargs: TYPE__KWARGS_DRAFT = None, *args2, **kwargs2) -> None:
        self.ARGS = ArgsKwargsAux(args).resolve_args()
        self.KWARGS = ArgsKwargsAux(kwargs).resolve_kwargs()
        super().__init__(source, *args2, **kwargs2)


# =====================================================================================================================
