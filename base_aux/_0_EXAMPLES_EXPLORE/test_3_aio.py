from typing import *
import pytest
import asyncio
from pytest import mark

from base_aux.base_lambdas.m1_lambda import *


# =====================================================================================================================
@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="func_link, args, _EXPECTED",
    argvalues=[
        (asyncio.sleep, (0.1, 1), 1),
        (asyncio.sleep, ("hello",), TypeError),
    ]
)
async def test__aio(func_link, args, _EXPECTED):
    try:
        result = await func_link(*args)
    except BaseException as exc:
        result = type(exc)

    assert result == _EXPECTED

"""
Testing started at 18:19 ...
Launching pytest with arguments test0_tasks1_cm.py::test__aio --no-header --no-summary -q in C:\__STARICHENKO_Element\PROJECTS\abc=aio_testplan\aio_tp2

============================= test session starts =============================
collecting ... collected 2 items

test0_tasks1_cm.py::test__aio[sleep-args0-1] 
test0_tasks1_cm.py::test__aio[sleep-args1-TypeError] 

============================== 2 passed in 0.16s ==============================
PASSED                      [ 50%]PASSED              [100%]sys:1: RuntimeWarning: coroutine 'sleep' was never awaited

Process finished with exit code 0
"""


# =====================================================================================================================
