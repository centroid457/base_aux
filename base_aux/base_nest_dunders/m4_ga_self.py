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
    1. use any chain if not exists ga
        class Victim(NestGa_Self): ...
        victim = Victim()
        assert victim == victim.hello.world

    2. use as nested
        class Victim(NestGa_Self):
            attr=1
            def meth(self, param=None):
                return param
        victim = Victim()
        assert victim.attr == victim.hello.world.attr
        assert victim.meth() == victim.hello.world.meth()
    """
    def __getattr__(self, item: str) -> Self:
        return self


# =====================================================================================================================
