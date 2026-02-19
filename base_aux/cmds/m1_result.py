from typing import *
from datetime import datetime

from dataclasses import dataclass, field
from base_aux.base_enums.m2_enum1_adj import EnumAdj_BufferType, EnumAdj_FinishedStatus
from base_aux.base_values.m3_exceptions import *


# =====================================================================================================================
TYPING__CMD_LINE = str | bytes
TYPING__CMD_LINES = Collection[TYPING__CMD_LINE]
TYPING__CMD_LINES_DRAFT = TYPING__CMD_LINE | TYPING__CMD_LINES


# =====================================================================================================================
@dataclass
class CmdCondition:
    """
    GOAL
    ----
    define exact cmd with timeout value
    """
    LINE: TYPING__CMD_LINE
    TIMEOUT: float | int | None = None


TYPING__CMD_CONDITION = Union[TYPING__CMD_LINE, tuple[TYPING__CMD_LINE, float | int | None]]
TYPING__CMDS_CONDITIONS = Union[TYPING__CMD_CONDITION, list[TYPING__CMD_CONDITION]]


# =====================================================================================================================
@dataclass
class CmdResult:
    """
    GOAL
    ----
    keep all data for command request

    CONSTRAINTS
    -----------
    1. all data lines are str/bytes! - json is not expecting!!!
    expecting shells
        - os terminal
        - buses
            - serial
            - i2c (linux)
    """
    INPUT: TYPING__CMD_LINE = ""    # dont use collection on input!!! dont use None here!

    STDOUT: list[TYPING__CMD_LINE] = field(default_factory=list)
    # only exact STDOUT buffer

    STDERR: list[TYPING__CMD_LINE] = field(default_factory=list)
    # STDERR buffer and execution exceptions

    DEBUG: list[TYPING__CMD_LINE] = field(default_factory=list)   # dont need! overcomplicating? NO!!! very need!
    # all additional comments here

    def __post_init__(self):
        self.timestamp: datetime = datetime.now()
        self.duration: float = 0
        self.finished_status: EnumAdj_FinishedStatus = EnumAdj_FinishedStatus.NOT_FINISHED
        self._retcode: int | None = None    # if None then not setted!

        # self.stdin_bytes: bytes = b""
        # self.stdout_bytes: bytes = b""
        # self.stderr_bytes: bytes = b""

        if self.STDOUT is None:
            self.STDOUT = []
        elif isinstance(self.STDOUT, (str, bytes)):
            self.STDOUT = [self.STDOUT, ]

        if self.STDERR is None:
            self.STDERR = []
        elif isinstance(self.STDERR, (str, bytes)):
            self.STDERR = [self.STDERR, ]

        if self.DEBUG is None:
            self.DEBUG = []
        elif isinstance(self.DEBUG, (str, bytes)):
            self.DEBUG = [self.DEBUG, ]

    def __str__(self) -> str:
        result = f"{self.__class__.__name__}({self.INPUT=},{self.STDOUT=},{self.STDERR=})"
        return result

    @property
    def STDOUTERR(self) -> list[TYPING__CMD_LINE]:
        return [*self.STDOUT, *self.STDERR]

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def retcode(self) -> int | None:
        return self._retcode

    def set_retcode(self, other: int | None = None) -> None:
        if self._retcode is None and other is not None:
            self._retcode = other

    # -----------------------------------------------------------------------------------------------------------------
    def set_finished(self, status: EnumAdj_FinishedStatus | None = None) -> None:
        """
        GOAL
        ----
        mark/show that execution is finished for any cause
        and no need to wait any more
        """

        if status is None:
            status = EnumAdj_FinishedStatus.CORRECT
        self.finished_status = status

        self.duration = (datetime.now() - self.timestamp).total_seconds()

    # -----------------------------------------------------------------------------------------------------------------
    def check__success(self) -> bool:
        return self.retcode in [0, None] and not self.STDERR and self.finished_status in [EnumAdj_FinishedStatus.NOT_FINISHED, EnumAdj_FinishedStatus.CORRECT]

    def check__fail(self) -> bool:
        return not self.check__success()

    def check__finished(self) -> bool:
        return self.finished_status != EnumAdj_FinishedStatus.NOT_FINISHED

    def check__timed_out(self) -> bool:
        return self.finished_status == EnumAdj_FinishedStatus.TIMED_OUT

    def check__finished_and_success(self) -> bool:
        return self.check__finished() and self.check__success()

    # -----------------------------------------------------------------------------------------------------------------
    def append(
            self,
            data: TYPING__CMD_LINES_DRAFT,
            buffer_type: EnumAdj_BufferType = EnumAdj_BufferType.STDOUT,
    ) -> None | NoReturn:
        """
        GOAL
        ----
        append means only for output!
        for input try set it on inition only!
        """
        self.duration = (datetime.now() - self.timestamp).total_seconds()

        if buffer_type == EnumAdj_BufferType.STDOUT:
            source = self.STDOUT
        elif buffer_type == EnumAdj_BufferType.STDERR:
            source = self.STDERR
        elif buffer_type == EnumAdj_BufferType.DEBUG:
            source = self.DEBUG
        else:
            msg = f"use only STDOUT/STDERR/DEBUG{buffer_type=}"
            raise Exc__Incompatible(msg)

        if isinstance(data, (str, bytes)):
            source.append(data)
        else:
            for item in data:
                self.append(data=item, buffer_type=buffer_type)

    # def append_stdout(self, data: TYPING__CMD_LINES_DRAFT) -> None:
    #     return self.append(data=data, buffer_type=EnumAdj_BufferType.STDOUT)
    #
    # def append_stderr(self, data: TYPING__CMD_LINES_DRAFT) -> None:
    #     return self.append(data=data, buffer_type=EnumAdj_BufferType.STDERR)
    #
    # def append_debug(self, data: TYPING__CMD_LINES_DRAFT) -> None:
    #     return self.append(data=data, buffer_type=EnumAdj_BufferType.DEBUG)

    # -----------------------------------------------------------------------------------------------------------------
    def print_state(self, short: bool | None = None) -> None:
        if not short:
            print(f"="*50)

        if self.check__fail():
            print(f"[{'#'*21}ERROR{'#'*21}]")

        print(f"{self.INPUT=}")
        if not short:
            print(f"{self.duration=}")
            print(f"{self.check__success()=}")
            print(f"{self.retcode=}")
            print(f"{self.finished_status=}")
            print(f"-" * 50)
            print("=")

        for name, buff in [("STDOUT", self.STDOUT), ("STDERR", self.STDERR)]:
            if not short:
                print(f"{name}")
            if buff:
                for line in buff:
                    print(f"\t|{line!r}")
            if not short:
                print(f"-"*50)

        if not short:
            print(f"="*50)


# =====================================================================================================================
