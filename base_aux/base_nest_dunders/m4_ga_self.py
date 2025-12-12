from typing import *


# =====================================================================================================================
class NestGa_Self:
    """
    GOAL
    ----
    in tests when we need some object like
        stand_schema.device_table.count_columns()
    but we dont want to create all levels!

    SPECIALLY CREATED FOR
    ---------------------
    BaseTgcPhases_Case tests:
    we need to pass stand_schema,
    but used only stand_schema.device_table.count_columns()

    NOTE
    ----
    it is only a part of realisation!
    1. create expected methods in child!
    2. create expected attrs in init!

    EXAMPLE
    -------
    use any chain
        class Victim(NestGa_Self): ...
        victim = Victim()
        assert victim == victim.hello.world
    """
    def __getattr__(self, item: str) -> Self:
        return self


# =====================================================================================================================
class Monkey_GaSelf_CallResult(NestGa_Self):
    """
    GOAL
    ----
    in test suits when we need some object like
        victim.any.attr.chain.could.be.here()

    EXAMPLE
    -------
    use any attr chain
        victim = Monkey_GaSelf_CallResult(5)
        assert victim.any.attr.chain.could.be.here() == 5
    """
    def __init__(self, call_result: Any = None) -> None:
        self._call_result: Any = call_result

    def __call__(self) -> Any:
        return self._call_result


# =====================================================================================================================
