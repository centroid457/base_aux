import time
from typing import *
import asyncio


# =====================================================================================================================
class Sleep:
    """
    GOAL
    ----
    just a primitive func for tests or other purpose!
    """
    DEF_SEC: float = 1
    sec: float

    def __init__(self, sec: float = None):
        if sec is not None:
            self.sec = sec
        else:
            self.sec = self.DEF_SEC

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.sec})"

    def __repr__(self) -> str:
        return str(self)

    # -----------------------------------------------------------------------------------------------------------------
    def echo(self, echo: Any = None, *args, **kwargs) -> Any:
        time.sleep(self.sec)
        return echo

    def NONE(self, *args, **kwargs) -> None:
        # NOTE: why used uppercase!? - cause "raise" name here will not be appropriate!
        return self.echo(echo=None, *args, **kwargs)

    def TRUE(self, *args, **kwargs) -> bool:
        return self.echo(echo=True, *args, **kwargs)

    def FALSE(self, *args, **kwargs) -> bool:
        return self.echo(echo=False, *args, **kwargs)

    def EXC(self, *args, **kwargs) -> Exception:
        return self.echo(echo=Exception("Sleep.EXC"), *args, **kwargs)

    def RAISE(self, *args, **kwargs) -> NoReturn:
        self.echo()
        raise Exception("Sleep.RAISE")

    # -----------------------------------------------------------------------------------------------------------------
    async def aio_echo(self, echo: Any = None, *args, **kwargs) -> Any:
        await asyncio.sleep(self.sec)
        return echo

    async def aio_NONE(self, *args, **kwargs) -> None:
        return await self.aio_echo(echo=None, *args, **kwargs)

    async def aio_TRUE(self, *args, **kwargs) -> bool:
        return await self.aio_echo(echo=True, *args, **kwargs)

    async def aio_FALSE(self, *args, **kwargs) -> bool:
        return await self.aio_echo(echo=False, *args, **kwargs)

    async def aio_EXC(self, *args, **kwargs) -> Exception:
        return await self.aio_echo(echo=Exception("Sleep.EXC"), *args, **kwargs)

    async def aio_RAISE(self, *args, **kwargs) -> NoReturn:
        await self.aio_echo()
        raise Exception("Sleep.RAISE")


# =====================================================================================================================
class Base_SleepAw(Sleep):
    async def start(self) -> Any | NoReturn:
        raise NotImplementedError()

    def __await__(self) -> None | NoReturn:
        result = yield from self.start().__await__()
        return result


# ---------------------------------------------------------------------------------------------------------------------
class SleepAwNone(Base_SleepAw):
    async def start(self) -> None:
        return await self.aio_NONE()


class SleepAwTrue(Base_SleepAw):
    async def start(self) -> bool:
        return await self.aio_TRUE()


class SleepAwFalse(Base_SleepAw):
    async def start(self) -> bool:
        return await self.aio_FALSE()


class SleepAwExc(Base_SleepAw):
    async def start(self) -> Exception:
        return await self.aio_EXC()


class SleepAwRaise(Base_SleepAw):
    async def start(self) -> NoReturn:
        return await self.aio_RAISE()


# =====================================================================================================================
