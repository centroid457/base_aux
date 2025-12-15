import pytest
import asyncio
from typing import *

from base_aux.base_nest_dunders.m4_ga_self import NestGa_Self


# =====================================================================================================================
def test_1_clear():
    victim = NestGa_Self()
    assert victim == victim.hello
    assert victim == victim.hello.world


def test_2_nested():

    class Victim(NestGa_Self):
        attr = 1
        def meth(self, param=None):
            return param

    victim = Victim()
    assert victim.attr == victim.hello.attr
    assert victim.attr == victim.hello.world.attr

    assert victim.meth(5) == victim.hello.meth(5)
    assert victim.meth(5) == victim.hello.world.meth(5)


# =====================================================================================================================
