import pytest
import asyncio
from typing import *

from base_aux.base_monkeys.m1_ga_self import Monkey_GaSelf_CallResult


# =====================================================================================================================
def test_monkey__value_and_eq():
    victim = Monkey_GaSelf_CallResult(5)

    print()
    print("-"*50)
    print(f"{victim.count_columns()=}")
    print("-"*50)

    assert victim != 5
    assert victim == Monkey_GaSelf_CallResult(5)
    assert victim() == 5
    assert victim() != Monkey_GaSelf_CallResult(5)

    assert victim.hello == victim
    assert victim.hello != 5
    assert victim.hello() == 5
    assert victim.hello() != 100
    assert victim.hello() != victim
    assert victim.hello() != Monkey_GaSelf_CallResult(5)

    assert victim.hello.world == victim
    assert victim.hello.world() == 5
    assert victim.hello.world() != 100

    assert victim.hello.world.count_columns() == 5
    assert victim.hello.world.count_columns() != 100


# =====================================================================================================================
