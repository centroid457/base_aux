import os
from abc import ABC

from base_aux.cmds.m1_result import *
from base_aux.cmds.m2_history import CmdHistory_Aio
from base_aux.base_enums.m2_enum1_adj import *
from base_aux.cmds.m3_timeout_def import TimeoutDef
from base_aux.qeues.m1_event_broadcaster import EventBroadcaster, Nest_EventBroadcasterImplemented


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
class BaseUser_CmdTerminal(Nest_EventBroadcasterImplemented):
    """
    GOAL
    ----
    separate/collect all settings from all abc levels
    and some more common ones
    """
    EOL_SEND: str = "\n"

    idn: str
    id_index: int = 0
    _id_index__last: int = 0

    history: CmdHistory_Aio
    timeout_def: TimeoutDef = TimeoutDef(2, 1, 0.1)

    def __init__(
            self,
            idn: str | None = None,
            eol_send: str | None = None,

            timeout_write: float | None = None,
            timeout_read_start: float | None = None,
            timeout_read_finish: float | None = None,

            **kwargs,
    ):
        super().__init__(**kwargs)

        # user setup -----------------------
        self.set_id(idn)
        if eol_send is not None:
            self.EOL_SEND = eol_send

        self.timeout_def.change(timeout_write, timeout_read_start, timeout_read_finish)

        # other bg --------------------
        self._encoding: str = "cp866" if os.name == "nt" else "utf8"
        self._shell_cmd: str = "cmd" if os.name == "nt" else "bash"

        self._eb__aux["item_id"] = self.idn
        self.history = CmdHistory_Aio(eb=self._eb__obj, eb_aux=self._eb__aux)

    # -----------------------------------------------------------------------------------------------------------------
    def set_id(self, idn: str | None = None) -> None:
        """
        GOAL
        ----
        set idn name for instance specific or gen default with indexing
        """
        if idn is not None:
            self.idn = idn
        else:
            self.id_index = self.__class__._id_index__last
            self.__class__._id_index__last += 1

            self.idn = f"[{self.id_index}]{self.get_name()}"

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
