import pytest
import asyncio
from typing import *

from base_aux.base_nest_dunders.m4_ga_self import Monkey_GaSelf_CallResult


# =====================================================================================================================
def test_monkey():
    print()
    print("-"*50)
    print(f"{Monkey_GaSelf_CallResult(5).count_columns()=}")
    print("-"*50)

    assert Monkey_GaSelf_CallResult(5) != 5
    assert Monkey_GaSelf_CallResult(5).count_columns() == 5
    assert Monkey_GaSelf_CallResult(5).count_columns() != 55
    assert Monkey_GaSelf_CallResult(1).hello.world.count_columns() == 1
    assert Monkey_GaSelf_CallResult(5).hello.world.count_columns() == 5
    assert Monkey_GaSelf_CallResult(5).hello.world.count_columns() != 55


# =====================================================================================================================
