from typing import *
import os
from abc import ABC, abstractmethod

from base_aux.cmds.m1_result import *
from base_aux.cmds.m2_history import CmdHistory
from base_aux.base_enums.m2_enum1_adj import *
from base_aux.base_values.m3_exceptions import *
from base_aux.cmds.m3_timeout_def import TimeoutDef


# =====================================================================================================================
@dataclass
class CmdCondition:
    """
    GOAL
    ----
    define exact cmd with timeout value
    """
    LINE: TYPING__CMD_LINE
    TIMEOUT: TimeoutDef | None = None


TYPING__CMD_CONDITION = Union[TYPING__CMD_LINE, tuple[TYPING__CMD_LINE, float | None]]
TYPING__CMDS_CONDITIONS = Union[TYPING__CMD_CONDITION, list[TYPING__CMD_CONDITION]]


# =====================================================================================================================
class AbcUser_CmdTerminal(ABC):
    """
    GOAL
    ----
    separate/collect all settings from all abc levels
    and some more common ones
    """
    EOL_SEND: str = "\n"

    id: str
    id_index: int = 0
    _id_index__last: int = 0

    history: CmdHistory
    timeout_def: TimeoutDef = TimeoutDef(2, 1, 0.1)

    def __init__(
            self,
            *,
            id: str | None = None,
            eol_send: str | None = None,

            timeout_write: float | None = None,
            timeout_read_start: float | None = None,
            timeout_read_finish: float | None = None,

            cwd: str | None = None,
            **kwargs,
    ):
        super().__init__(**kwargs)

        # user setup -----------------------
        self.set_id(id)
        if eol_send is not None:
            self.EOL_SEND = eol_send

        self.cwd: str | None = cwd
        self.timeout_def.change(timeout_write, timeout_read_start, timeout_read_finish)

        # other bg --------------------
        self._encoding: str = "cp866" if os.name == "nt" else "utf8"
        self._shell_cmd: str = "cmd" if os.name == "nt" else "bash"

        self.history = CmdHistory()

    # -----------------------------------------------------------------------------------------------------------------
    def set_id(self, id: str | None = None) -> None:
        """
        GOAL
        ----
        set id name for instance specific or gen default with indexing
        """
        if id is not None:
            self.id = id
        else:
            self.id_index = self.__class__._id_index__last
            self.__class__._id_index__last += 1

            self.id = f"[{self.id_index}]{self.get_name()}"

    @classmethod
    def get_name(cls) -> str:
        """
        GOAl
        ----
        get name from class with ability not to redefine and receive correct class name
        """
        return cls.__name__

    def clear_history(self) -> None:
        """
        NOTE
        ----
        use only manually!
        """
        self.history.clear()


# =====================================================================================================================
class AbcConn_CmdTerminal(AbcUser_CmdTerminal):
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
            buffer_type: EnumAdj_BufferType = EnumAdj_BufferType.STDOUT,
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
