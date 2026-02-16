from typing import *
import time
import os
import uuid

from base_aux.cmds.m1_result import CmdResult
from base_aux.cmds.m2_history import CmdHistory


# =====================================================================================================================
class Base_CmdTerminal:
    def __init__(
            self,
            *,
            id: str | None = None,

            timeout_start: float = 1,
            timeout_finish: float = 0.1,

            cwd: str | None = None,
            **kwargs,
    ):
        super().__init__(**kwargs)

        self._encoding: str = "cp866" if os.name == "nt" else "utf8"
        self._shell_cmd: str = "cmd" if os.name == "nt" else "bash"

        self._last_byte_time: float = 0.0   # время последнего полученного байта
        self._stop_reading: bool = False
        self._conn: Any | None = None
        self._bg_tasks: list[Any] = []

        self.id: str | None = id or str(uuid.uuid4())
        self.timeout_start: float = timeout_start
        self.timeout_finish: float = timeout_finish
        self.history: CmdHistory = CmdHistory()

        self.cwd: str | None = cwd

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_name(cls) -> str:
        """
        GOAl
        ----
        get name from class with ability not to redefine and receive correct class name
        """
        return cls.__name__

    # -----------------------------------------------------------------------------------------------------------------
    def connect(self) -> None:
        raise NotImplementedError()

    def _create_conn(self) -> None | NoReturn:
        """
        GOAL
        ----
        only create only one _conn! no validate/ no catching exc!!!
        """
        raise NotImplementedError()

    def _create_tasks(self) -> None:
        """
        GOAL
        ----
        only create and start tasks! no validate/ no catching exc!!!???
        """
        raise NotImplementedError()

    def disconnect(self) -> None:
        raise NotImplementedError()

    def reconnect(self) -> None:
        """
        GOAL
        ----
        apply closing and opening again
        without clear history (if need do it manually!)

        SPECIALLY CREATED FOR
        ---------------------
        for case when we send continious infinitive cmd and cant stop it
        so the only way is stop process/connection and open it again!
        this is the only way to do it cause sending Ctrl+С is not working correctly!
        """
        self.disconnect()
        self.connect()

    # -----------------------------------------------------------------------------------------------------------------
    def clear_history(self) -> None:
        """
        NOTE
        ----
        use only manually!
        """
        self.history.clear()

    # -----------------------------------------------------------------------------------------------------------------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    # -----------------------------------------------------------------------------------------------------------------
    def send_command(self, cmd: str, timeout_start: float | None = None, timeout_finish: float | None = None) -> CmdResult:
        raise NotImplementedError()

    def _wait__finish_executing_cmd(self, timeout_start: float | None = None, timeout_finish: float | None = None) -> bool:
        """
        GOAL
        ----
        ensure finishing any buffer activity
        1. wait long timeout_start for start activity
        2. wait short timeout2 for close waiting any new line!
        """
        timeout_start = timeout_start or self.timeout_start
        timeout_finish = timeout_finish or self.timeout_finish

        data_received: bool = False
        last_duration: float = self.history.last_result.duration

        timeout_active = timeout_start
        time_start = time.time()
        while time.time() - time_start < timeout_active:
            if last_duration != self.history.last_result.duration:
                data_received = True
                last_duration = self.history.last_result.duration
                time_start = time.time()
                timeout_active = timeout_finish
            else:
                time.sleep(timeout_finish / 3)   # at least we need to execute last check

        return data_received


# =====================================================================================================================
