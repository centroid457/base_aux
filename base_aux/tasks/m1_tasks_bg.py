from typing import *
import asyncio
import threading
from abc import abstractmethod
from base_aux.base_types.m1_type_aux import TypeAux
from base_aux.base_values.m3_exceptions import *


# =====================================================================================================================
class Nest_TasksBg_Abc:
    _tasks_bg: list[threading.Thread | asyncio.Task]

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        self._tasks_bg = []

        super().__init__(*args, **kwargs)

    @abstractmethod
    def _tasks_bg__extend(self, *aws: Any) -> None | NoReturn:
        """
        GOAL
        ----
        only create and start tasks! no validate/ no catching exc!!!???
        """
        raise NotImplementedError()

    @abstractmethod
    def _tasks_bg__create_start(self) -> None:
        """
        GOAL
        ----
        only create and start tasks! no validate/ no catching exc!!!???
        """
        raise NotImplementedError()

    @abstractmethod
    def _tasks_bg__stop_delete(self, timeout: float = 1) -> None:
        """
        GOAL
        ----
        DONT USE only STOP! only with delete! create again if need!
        """
        raise NotImplementedError()

    @abstractmethod
    def _tasks_bg__onexit_local(self) -> None | NoReturn:
        raise NotImplementedError()


# =====================================================================================================================
class Nest_TasksBg_AbcSync(Nest_TasksBg_Abc):
    _tasks_bg: list[threading.Thread]

    @abstractmethod
    def _tasks_bg__extend(self, *ths: threading.Thread | Callable) -> None | NoReturn:
        for th in ths:
            thread = None
            if TypeAux(th).check__thread():
                thread = th
            elif callable(th):
                thread = threading.Thread(target=th, daemon=True)
            else:
                msg = f"not thread-able={th!r}"
                raise Exc__WrongUsage(msg)

            self._tasks_bg.append(thread)

    @abstractmethod
    def _tasks_bg__create_start(self) -> None:
        raise NotImplementedError()

    def _tasks_bg__stop_delete(self, timeout: float = 1) -> None:
        for task in self._tasks_bg:
            task.join(timeout=timeout)

        self._tasks_bg.clear()

    @abstractmethod
    def _tasks_bg__onexit_local(self) -> None | NoReturn:
        pass


# ---------------------------------------------------------------------------------------------------------------------
class Nest_TasksBg_AbcAio(Nest_TasksBg_Abc):
    _tasks_bg: list[asyncio.Task]

    _tasks_bg__onexit_local: Callable | Awaitable | None

    # -----------------------------------------------------------------------------------------------------------------
    async def __aenter__(self) -> Self | NoReturn:
        # DONT USE TRY!!!
        self._tasks_bg__create_start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # 1=MAIN exec
        try:
            await self._tasks_bg__stop_delete()
        except:
            pass

        # 2=LOCAL exec
        try:
            if self._tasks_bg__onexit_local is not None:
                if TypeAux(self._tasks_bg__onexit_local).check__coro():
                    await self._tasks_bg__onexit_local
                elif TypeAux(self._tasks_bg__onexit_local).check__coro_func():
                    await self._tasks_bg__onexit_local()
                elif callable(self._tasks_bg__onexit_local):
                    self._tasks_bg__onexit_local()
                else:
                    msg= f"{self._tasks_bg__onexit_local!r}"
                    raise Exc__WrongUsage(msg)
        except:
            pass

    @abstractmethod
    async def _tasks_bg__onexit_local(self) -> None | NoReturn:
        pass

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _tasks_bg__extend(self, *aws: Awaitable | asyncio.Task | Coroutine | Callable[..., Awaitable]) -> None | NoReturn:
        """
        GOAL
        ----
        only create and start tasks! no validate/ no catching exc!!!???
        """
        for aw in aws:
            task = None
            if TypeAux(aw).check__task():
                task = aw
            elif TypeAux(aw).check__coro():
                task = asyncio.create_task(aw)
            elif TypeAux(aw).check__coro_func():
                task = asyncio.create_task(aw())
            else:
                msg = f"not aw-able={task!r}"
                raise Exc__WrongUsage(msg)

            self._tasks_bg.append(task)

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _tasks_bg__create_start(self) -> None:  # KEEP SYNC!!! used in connect!
        raise NotImplementedError()

    async def _tasks_bg__stop_delete(self, timeout: float = 1) -> None:
        for task in self._tasks_bg:
            try:
                task.cancel()
            except:
                pass
        try:
            await asyncio.wait_for(
                asyncio.gather(*self._tasks_bg, return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            # Если задачи не завершились, просто забудем о них
            pass
        except:
            pass

        self._tasks_bg.clear()


# =====================================================================================================================
