import asyncio
from typing import Callable, Awaitable, Any, final, Coroutine, NoReturn

from base_aux.base_nest_dunders.m1_init1_source import NestInit_Source
from base_aux.base_types.m1_type_aux import TypeAux
from base_aux.base_values.m3_exceptions import Exc__WrongUsage, Exc__UnExpectedExc


# =====================================================================================================================
TYPES__CALLBACK_AIO = Callable[..., Awaitable[Any | None]] | Callable[..., Any | None]
TYPES__CALLBACK_AIO__DATA = Callable[[dict | Any], Awaitable[None]] | Callable[[dict | Any], None]


# =====================================================================================================================
@final
class AioAux(NestInit_Source):
    SOURCE: (
            TYPES__CALLBACK_AIO |
            Awaitable | asyncio.Task | Coroutine | Callable[..., Awaitable] |
            None
    )

    async def callback_sync_aio__execute(
            self,
            *args: tuple[Any, ...] | None,
            **kwargs: dict[str, Any] | None,
    ) -> Any | None | NoReturn:
        """
        GOAL
        call callback as async or sync func!
        """
        result = None
        args = args or tuple()
        kwargs = kwargs or dict()

        try:
            if self.SOURCE is None:
                return
            elif TypeAux(self.SOURCE).check__coro_func():
                result = await self.SOURCE(*args, **kwargs)
            elif TypeAux(self.SOURCE).check__coro():
                result = await self.SOURCE
            elif callable(self.SOURCE):
                result = self.SOURCE(*args, **kwargs)
            else:
                msg = f"{self.SOURCE!r}({args=},{kwargs=})"
                raise Exc__WrongUsage(msg)
        except asyncio.CancelledError:  # проброс дальше!
            raise
        except Exception as exc:
            raise Exc__UnExpectedExc(f"{exc!r}")

        return result

    def ensure_task(self) -> asyncio.Task | NoReturn:
        """
        GOAL
        use only existed object no args/kwargs!
        """
        if TypeAux(self.SOURCE).check__task():
            task = self.SOURCE

        elif TypeAux(self.SOURCE).check__coro_func():
            task = asyncio.create_task(self.SOURCE())

        elif TypeAux(self.SOURCE).check__coro():
            task = asyncio.create_task(self.SOURCE)

            # elif callable(self.SOURCE):
            #     pass
            #     # TODO: use to_task? or use before manually called

        else:
            msg = f"not aw-able={self.SOURCE!r}"
            raise Exc__WrongUsage(msg)

        return task


# =====================================================================================================================
