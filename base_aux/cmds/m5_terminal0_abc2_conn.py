import asyncio
from abc import abstractmethod
from typing import *

from base_aux.base_values.m3_exceptions import Exc__Io, Exc__UnDefined, Exc__WrongUsage, Exc__IoTimeout
from base_aux.cmds.m0_tasks_bg import Nest_TasksBg_Abc
from base_aux.cmds.m5_terminal0_abc1_user import BaseUser_CmdTerminal


# =====================================================================================================================
class AbcConn_CmdTerminal(BaseUser_CmdTerminal, Nest_TasksBg_Abc):
    _conn: Any | None
    _event_connected = asyncio.Event

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._conn = None
        self._last_byte_time: float = 0.0   # время последнего полученного байта

        self._event_connected = asyncio.Event()
        self._event_connected.clear()

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _create_conn(self) -> None | NoReturn:
        """
        GOAL
        ----
        only create only one _conn! no validate/ no catching exc!!!
        """
        raise NotImplementedError()

    @abstractmethod
    def _del_conn(self) -> None:
        """
        GOAL
        ----
        only create only one _conn! no validate/ no catching exc!!!
        """
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _read_byte_with_timeout(
            self,
            buffer: Any,
            timeout: float = 0.05,
    ) -> bytes | NoReturn | Exc__Io | Exc__UnDefined | Exc__WrongUsage:
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _write_line(
            self,
            cmd: str,
            timeout: float | None = None,
            eol: str | None = None,
    ) -> None | NoReturn | Exc__IoTimeout:
        raise NotImplementedError()


# =====================================================================================================================
