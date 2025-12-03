import time
from typing import *
import asyncio


# =====================================================================================================================
@final
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
