import pytest
import asyncio

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_types.m0_static_typing import *
from base_aux.aux_datetime.m1_sleep import *


# =====================================================================================================================
@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        # TRIVIAL ---------------------------------
        (None, Exception),
        (1, Exception),
        (Base_SleepAw(0.1), Exception),
        (SleepAwNone(0.1), None),
        (SleepAwTrue(0.1), True),
        (SleepAwFalse(0.1), False),
        (SleepAwExc(0.1), Exception),
        (SleepAwRaise(0.1), Exception),
    ]
)
async def test__1(
        source: TYPING.AIO_CORO | Any,
        _EXPECTED: bool | type[Exception] | Any,
):
    try:
        result = await source
    except BaseException as exc:
        result = exc

    Lambda(result).expect__check_assert(_EXPECTED)


# =====================================================================================================================
