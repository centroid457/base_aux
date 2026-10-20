import asyncio
import pytest
from utils import *


# ======================================================================================================================
STAND_DUT_COUNT: int = 4

@pytest.fixture(scope="session")
async def dc() -> Dc:
    dc = Dc()
    if not await dc._detect():
        pytest.fail(f"{dc=} not detected")
    print(f"{dc=} detected")
    if not await dc._connect():
        pytest.fail(f"{dc=} not connected")
    print(f"{dc=} connected")

    yield dc

    await dc._disconnect()


# DEVS -------------------------------------------------
@pytest.fixture(scope="session")
async def dut_list() -> tuple[Dut, ...]:
    result: list = []
    any_dut_connected = False

    for index in range(STAND_DUT_COUNT):
        dut = Dut(index)
        result.append(dut)

        if not await dut._detect():
            print(f"{dut=} not detected")
            continue
        print(f"{dut=} detected")
        if not await dut._connect():
            print(f"{dut=} not connected")
            continue
        print(f"{dut=} connected")
        any_dut_connected = True

    if not any_dut_connected:
        pytest.fail(f"{any_dut_connected=}")

    yield tuple(result)

    for dut in result:
        await dut._disconnect()


# ======================================================================================================================
