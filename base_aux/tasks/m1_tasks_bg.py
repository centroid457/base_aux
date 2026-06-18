import asyncio
import threading
from abc import abstractmethod


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


# =====================================================================================================================
class Nest_TasksBg_AbcSync(Nest_TasksBg_Abc):
    _tasks_bg: list[threading.Thread]

    @abstractmethod
    def _tasks_bg__create_start(self) -> None:
        raise NotImplementedError()

    def _tasks_bg__stop_delete(self, timeout: float = 1) -> None:
        for task in self._tasks_bg:
            task.join(timeout=timeout)

        self._tasks_bg.clear()


# ---------------------------------------------------------------------------------------------------------------------
class Nest_TasksBg_AbcAio(Nest_TasksBg_Abc):
    _tasks_bg: list[asyncio.Task]

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

        self._tasks_bg.clear()


# =====================================================================================================================
