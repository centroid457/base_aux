from typing import *
import time
import os
import uuid

from base_aux.cmds.m1_result import CmdResult
from base_aux.cmds.m2_history import CmdHistory


# =====================================================================================================================
class Abc_CmdTerminal:
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

        self.timeout_start: float = timeout_start
        self.timeout_finish: float = timeout_finish
        self.history: CmdHistory = CmdHistory()

        self.cwd: str | None = cwd

        self.id: str = id or str(uuid.uuid4())

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

    def disconnect(self) -> None:
        raise NotImplementedError()

    def reconnect(self) -> None:
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------------------------------------------
    def clear_history(self) -> None:
        """
        NOTE
        ----
        use only manually!
        """
        self.history.clear()

    # -----------------------------------------------------------------------------------------------------------------
    def send_command(
            self,
            cmd: str,
            timeout_start: float | None = None,
            timeout_finish: float | None = None,
    ) -> CmdResult:
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    def _wait__finish_executing_cmd(
            self,
            timeout_start: float | None = None,
            timeout_finish: float | None = None,
    ) -> bool:
        raise NotImplementedError()


# =====================================================================================================================
