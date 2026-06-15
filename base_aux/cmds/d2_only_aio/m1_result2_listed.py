import asyncio
from typing import *
from datetime import datetime

from dataclasses import dataclass, field
from base_aux.base_enums.m2_enum1_adj import EnumAdj_StdioeType, EnumAdj_FinishedStatus
from base_aux.base_values.m3_exceptions import *


# =====================================================================================================================
TYPING__CMD_LINE = str | bytes


# =====================================================================================================================
@dataclass
class BufferLine:
    """
    GOAL
    ----
    exact line for/from any buffer.
    just an ATOMIC LINE.
    """
    BUFFER_TYPE: EnumAdj_StdioeType
    BUFFER_LINE: TYPING__CMD_LINE

    def __post_init__(self):
        self.TIMESTAMP: datetime = datetime.now()


# =====================================================================================================================
class CmdResult2_DataLines:
    """
    GOAL
    ----
    keep all dataLINES for command request

    CONSTRAINTS
    -----------
    1. all data lines are str/bytes! - json is not expecting!!!
    expecting shells
        - os terminal
        - buses
            - serial
            - i2c (linux)
    """
    DATALINES: list[BufferLine]
    duration: float = 0

    def __init__(self, inputline: TYPING__CMD_LINE = "") -> None:
        self.finished_status: EnumAdj_FinishedStatus = EnumAdj_FinishedStatus.NOT_FINISHED
        self._retcode: int | None = None    # if None then not setted!

        self.DATALINES = []
        self._append(line=inputline, buffer_type=EnumAdj_StdioeType.STDIN)

    # -----------------------------------------------------------------------------------------------------------------
    def _append(
            self,
            line: TYPING__CMD_LINE,
            buffer_type: EnumAdj_StdioeType,
        ) -> None | NoReturn:
            """
            GOAL
            ----
            append means only for output!
            for input try set it on inition only!
            """
            if buffer_type == EnumAdj_StdioeType.STDIN and self.DATALINES:
                msg = f"STDIN already added! {self.DATALINES}"
                raise Exc__WrongUsage(msg)

            if buffer_type in [EnumAdj_StdioeType.STDOUT, EnumAdj_StdioeType.STDERR]:
                self.duration = (datetime.now() - self.TIMESTAMP).total_seconds()

            dataline = BufferLine(buffer_type, line)

            self.DATALINES.append(dataline)

    def append_stdout(self, line: TYPING__CMD_LINE) -> None:
        return self._append(line=line, buffer_type=EnumAdj_StdioeType.STDOUT)

    def append_stderr(self, line: TYPING__CMD_LINE) -> None:
        return self._append(line=line, buffer_type=EnumAdj_StdioeType.STDERR)

    def append_debug(self, line: TYPING__CMD_LINE) -> None:
        return self._append(line=line, buffer_type=EnumAdj_StdioeType.DEBUG)

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def TIMESTAMP(self) -> datetime:
        return self.INPUTLINE.TIMESTAMP

    @property
    def INPUTLINE(self) -> BufferLine:
        result = self.DATALINES[0]
        return result

    @property
    def STDOUT(self) -> list[BufferLine]:
        result = list(filter(lambda line: line.BUFFER_TYPE == EnumAdj_StdioeType.STDOUT, self.DATALINES))
        return result

    @property
    def STDERR(self) -> list[BufferLine]:
        result = list(filter(lambda line: line.BUFFER_TYPE == EnumAdj_StdioeType.STDERR, self.DATALINES))
        return result

    @property
    def DEBUG(self) -> list[BufferLine]:
        result = list(filter(lambda line: line.BUFFER_TYPE == EnumAdj_StdioeType.DEBUG, self.DATALINES))
        return result

    def __str__(self) -> str:
        result = f"{self.__class__.__name__}({self.INPUTLINE=},{self.STDOUT=},{self.STDERR=})"
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def retcode(self) -> int | None:
        return self._retcode

    def set_retcode(self, other: int | None = None) -> None:
        if other is None:
            return
        if self._retcode in [None, 0]:
            self._retcode = other

    # -----------------------------------------------------------------------------------------------------------------
    pass # TODO: FINISH
    pass # TODO: FINISH
    pass # TODO: FINISH
    pass # TODO: FINISH
    pass # TODO: FINISH

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

        self.duration = (datetime.now() - self.TIMESTAMP).total_seconds()

    # -----------------------------------------------------------------------------------------------------------------
    def check__success(self) -> bool:
        return self.retcode in [0, None] and not self.STDERR and self.finished_status == EnumAdj_FinishedStatus.CORRECT

    def check__fail(self) -> bool:
        return not self.check__success()

    def check__finished(self) -> bool:
        return self.finished_status != EnumAdj_FinishedStatus.NOT_FINISHED

    def check__timed_out(self) -> bool:
        return self.finished_status == EnumAdj_FinishedStatus.TIMED_OUT

    def check__finished_and_success(self) -> bool:
        return self.check__finished() and self.check__success()

    # -----------------------------------------------------------------------------------------------------------------
    def print_state(self, short: bool | None = None) -> None:
        if not short:
            print(f"="*50)

        if self.check__fail():
            print(f"[{'#'*21}ERROR{'#'*21}]")

        print(f"{self.INPUTLINE=}")
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
