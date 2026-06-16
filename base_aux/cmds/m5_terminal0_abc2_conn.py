from abc import abstractmethod
from typing import Any, NoReturn

from base_aux.base_enums.m2_enum1_adj import EnumAdj_StdioeType
from base_aux.base_values.m3_exceptions import Exc__Io, Exc__UnDefined, Exc__WrongUsage, Exc__IoTimeout
from base_aux.cmds.m5_terminal0_abc1_user import BaseUser_CmdTerminal


class AbcConn_CmdTerminal(BaseUser_CmdTerminal):
    _conn: Any | None

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._conn = None
        self._last_byte_time: float = 0.0   # время последнего полученного байта
        self._stop_reading: bool = False

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
    def _create_tasks(self) -> None:
        """
        GOAL
        ----
        only create and start tasks! no validate/ no catching exc!!!???
        """
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _del_conn(self) -> None:
        """
        GOAL
        ----
        only create only one _conn! no validate/ no catching exc!!!
        """
        raise NotImplementedError()

    @abstractmethod
    def _del_tasks(self) -> None:
        """
        GOAL
        ----
        only create and start tasks! no validate/ no catching exc!!!???
        """
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _read_byte_with_timeout(
            self,
            timeout: float = 0.05,
            buffer_type: EnumAdj_StdioeType = EnumAdj_StdioeType.STDOUT,
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
