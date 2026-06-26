from typing import *
import asyncio
import threading
from abc import abstractmethod
from base_aux.base_types.m1_type_aux import TypeAux
from base_aux.base_values.m3_exceptions import *


# =====================================================================================================================
class Nest_TasksBg_Abc:
    _tasks_bg: set[threading.Thread | asyncio.Task]

    def __init__(
            self,
            *args,
            _tasks_bg__onexit_local: Callable | Awaitable | None = None,
            **kwargs,
    ):
        self._tasks_bg = set()
        self._event_exit: asyncio.Event = asyncio.Event()

        if _tasks_bg__onexit_local is not None:
            self._tasks_bg__onexit_local = _tasks_bg__onexit_local

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
        """
        GOAL
        additional logic for global __aexit__

        SPECIALLY CREATED FOR
        WsClient
        """
        raise NotImplementedError()


# =====================================================================================================================
class Nest_TasksBg_AbcSync(Nest_TasksBg_Abc):
    _tasks_bg: set[threading.Thread]

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

            self._tasks_bg.add(thread)

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
    _tasks_bg: set[asyncio.Task]
    _tasks_bg__onexit_local: Callable | Awaitable | None

    # --------------------------------------------
    def __await__(self):
        yield from self._tasks_bg__wait().__await__()

    async def _tasks_bg__wait(self, timeout: float | None = None) -> None:
        await asyncio.wait_for(
            asyncio.gather(*self._tasks_bg, return_exceptions=True),
            timeout=timeout
        )

    # -----------------------------------------------------------------------------------------------------------------
    async def __aenter__(self) -> Self | NoReturn:
        self._event_exit.clear()
        try:    # DONT USE TRY!!!???
            self._tasks_bg__create_start()
        except:
            raise
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

        self._event_exit.set()

    @abstractmethod
    async def _tasks_bg__onexit_local(self) -> None | NoReturn:
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def _tasks_bg__extend(self, *aws: Awaitable | asyncio.Task | Coroutine | Callable[..., Awaitable]) -> None | NoReturn:
        """
        GOAL
        ----
        only create and start tasks! no validate/ no catching exc!!!???
        """
        for aw in aws:
            task = self._tasks_bg__ensure_task(aw)
            self._tasks_bg.add(task)

    def _tasks_bg__ensure_task(self, source: Awaitable | asyncio.Task | Coroutine | Callable[..., Awaitable]) -> Awaitable | NoReturn:
        if TypeAux(source).check__task():
            task = source
        elif TypeAux(source).check__coro():
            task = asyncio.create_task(source)
        elif TypeAux(source).check__coro_func():
            task = asyncio.create_task(source())
        else:
            msg = f"not aw-able={source!r}"
            raise Exc__WrongUsage(msg)
        return task

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
            await self._tasks_bg__wait(timeout)
        except asyncio.TimeoutError:
            # Если задачи не завершились, просто забудем о них
            pass
        except:
            pass

        self._tasks_bg.clear()


# =====================================================================================================================
class TasksBg_PoolGlobal(Nest_TasksBg_AbcAio):
    """
    Глобальный (синглтон) реестр фоновых задач, не привязанный к конкретному владельцу.
    Предоставляет spawn(coro) для запуска и wait_all() для ожидания/отмены.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _tasks_bg__ensure_task(self, source: Awaitable | asyncio.Task | Coroutine | Callable[..., Awaitable]) -> Awaitable | NoReturn:
        task = super()._tasks_bg__ensure_task(source)
        task.add_done_callback(self._tasks_bg.discard)
        task.add_done_callback(self._tasks_bg__log_exc)

    @staticmethod
    def _tasks_bg__log_exc(fut):
        if fut.exception() and not isinstance(fut.exception(), asyncio.CancelledError):
            print(f"BgTask failed={fut.exception()!r}")

    def spawn(self, coro):
        self._tasks_bg__extend(coro)


# =====================================================================================================================
