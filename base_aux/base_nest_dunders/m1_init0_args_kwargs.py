from typing import *

from base_aux.aux_argskwargs.m2_argskwargs_aux import *
from base_aux.base_statics.m1_types import *


# =====================================================================================================================
class NestInit_Args_Implicit:
    """
    GOAL
    ----
    base for using classes with implicit args as variants

    SPECIALLY CREATED FOR
    ---------------------
    EqArgs for cmp all args between each other!
    """
    ARGS: TYPING.ARGS_FINAL

    def __init__(self, *args, **kwargs) -> None:
        self.ARGS = args
        super().__init__(**kwargs)


class NestInit_Kwargs_Implicit:
    """
    GOAL
    ----
    just extend same logic variant
    """
    KWARGS: TYPING.KWARGS_FINAL

    def __init__(self, *args, **kwargs) -> None:
        self.KWARGS = kwargs
        super().__init__(*args)


class NestInit_ArgsKwargs_Implicit:
    """
    GOAL
    ----
    just extend same logic variant
    """
    ARGS: TYPING.ARGS_FINAL
    KWARGS: TYPING.KWARGS_FINAL

    def __init__(self, *args, **kwargs) -> None:
        self.ARGS = args
        self.KWARGS = kwargs


# =====================================================================================================================
