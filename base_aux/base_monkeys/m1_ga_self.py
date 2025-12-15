from typing import Any, Self

from base_aux.base_monkeys.m0_base import Mark_Monkey
from base_aux.base_nest_dunders.m4_ga_self import NestGa_Self
from base_aux.base_nest_dunders.m2_str1_cls import *


# =====================================================================================================================
class Monkey_GaSelf(NestGa_Self, Mark_Monkey):
    """
    GOAL
    ----
    just show that final class is exactly the monkey - no more differences from NestGa_Self
    """


# =====================================================================================================================
class Monkey_GaSelf_CallResult(NestGa_Self, Mark_Monkey):
    """
    GOAL
    ----
    in test suits when we need some object like
        victim.any.attr.chain.could.be.here()

    EXAMPLE
    -------
    use any attr chain
        victim = Monkey_GaSelf_CallResult(5)
        assert victim.hello == victim
        assert victim.hello() == 5

        assert victim.hello.world == victim
        assert victim.hello.world() == 5
    """
    def __init__(self, call_result: Any = None) -> None:
        self._call_result: Any = call_result

    def __call__(self) -> Any:
        return self._call_result

    def __eq__(self, other: Self | Any) -> bool:
        if isinstance(other, self.__class__):
            return self._call_result == other._call_result
        else:
            return False

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._call_result=})"

    def __repr__(self) -> str:
        return str(self)


# =====================================================================================================================
