from typing import *
import asyncio
import threading
from abc import abstractmethod
from base_aux.base_types.m1_type_aux import TypeAux
from base_aux.base_values.m3_exceptions import *
from base_aux.aux_paradigm.m1_thread import *
from base_aux.aux_paradigm.m2_aio import *


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
        self._event_stop: asyncio.Event = asyncio.Event()

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
        self._event_stop.clear()    # DONT FORGET!!!

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
            thread = ThreadAux(th).ensure_thread()
            self._tasks_bg.add(thread)

    @abstractmethod
    def _tasks_bg__create_start(self) -> None:
        self._event_stop.clear()    # DONT FORGET!!!

        raise NotImplementedError()

    def _tasks_bg__stop_delete(self, timeout: float = 1) -> None:
        self._event_stop.set()

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
            callback = self._tasks_bg__onexit_local
            if callback is not None:
                AioAux(callback).callback_sync_aio__execute()
        except:
            pass

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
            task = AioAux(aw).ensure_task()
            self._tasks_bg.add(task)

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _tasks_bg__create_start(self) -> None:  # KEEP SYNC!!! used in connect!
        self._event_stop.clear()    # DONT FORGET!!!

        raise NotImplementedError()

    async def _tasks_bg__stop_delete(self, timeout: float = 1) -> None:
        self._event_stop.set()

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

    def _tasks_bg__create_start(self) -> None:  # KEEP SYNC!!! used in connect!
        self._event_stop.clear()    # DONT FORGET!!!
        pass # NO CREATIONS!

    def _tasks_bg__extend(self, *aws: Awaitable | asyncio.Task | Coroutine | Callable[..., Awaitable]) -> None | NoReturn:
        for aw in aws:
            task = AioAux(aw).ensure_task()
            self._tasks_bg.add(task)

            task.add_done_callback(self._tasks_bg.discard)
            task.add_done_callback(self._tasks_bg__log_exc)

    @staticmethod
    def _tasks_bg__log_exc(fut):
        if fut.exception() and not isinstance(fut.exception(), asyncio.CancelledError):
            print(f"BgTask failed={fut.exception()!r}")

    def spawn(self, coro):
        self._tasks_bg__extend(coro)


# =====================================================================================================================
