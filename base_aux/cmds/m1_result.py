from typing import *
from datetime import datetime

from dataclasses import dataclass, field
from base_aux.base_enums.m2_enum1_adj import EnumAdj_Buffer
from base_aux.base_values.m3_exceptions import *


# =====================================================================================================================
TYPING__CMD_LINE = str | bytes
TYPING__CMD_LINES = Collection[TYPING__CMD_LINE]
TYPING__CMD_LINES_DRAFT = TYPING__CMD_LINE | TYPING__CMD_LINES

TYPING__CMD_CONDITION = Union[TYPING__CMD_LINE, tuple[TYPING__CMD_LINE, float | int | None]]
TYPING__CMDS_CONDITIONS = Union[TYPING__CMD_CONDITION, list[TYPING__CMD_CONDITION]]


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
    STDERR: list[TYPING__CMD_LINE] = field(default_factory=list)
    # DEBUG: list[TYPING__CMD_LINE] = field(default_factory=list)

    def __post_init__(self):
        self.timestamp: datetime = datetime.now()
        self.duration: float = 0
        self.retcode: int | None = None     # not always used
        self.timedout: bool = False     # not always used
        self.finished: bool = False     # not always used

        if self.STDOUT is None:
            self.STDOUT = []
        elif isinstance(self.STDOUT, (str, bytes)):
            self.STDOUT = [self.STDOUT, ]

        if self.STDERR is None:
            self.STDERR = []
        elif isinstance(self.STDERR, (str, bytes)):
            self.STDERR = [self.STDERR, ]

    def __str__(self) -> str:
        result = f"{self.__class__.__name__}({self.INPUT=},{self.STDOUT=},{self.STDERR=})"
        return result

    @property
    def STDOUTERR(self) -> list[TYPING__CMD_LINE]:
        return [*self.STDOUT, *self.STDERR]

    # -----------------------------------------------------------------------------------------------------------------
    def set_finished(self, timedout: bool | None = None) -> None:
        """
        GOAL
        ----
        mark/show that execution is finished for any cause
        and no need to wait any more
        """
        self.finished = True

        if timedout is not None:
            self.timedout = timedout

    # -----------------------------------------------------------------------------------------------------------------
    def check_success(self) -> bool:
        return self.retcode in [0, None] and not self.STDERR and not self.timedout

    def check_fail(self) -> bool:
        return not self.check_success()

    def check_finished_and_success(self) -> bool:
        return self.finished and self.check_success()

    # -----------------------------------------------------------------------------------------------------------------
    def append(
            self,
            data: TYPING__CMD_LINES_DRAFT,
            _type_buffer: EnumAdj_Buffer = EnumAdj_Buffer.STDOUT,
    ) -> None | NoReturn:
        """
        GOAL
        ----
        append means only for output!
        for input try set it on inition only!
        """
        self.duration = datetime.now() - self.timestamp

        if _type_buffer == EnumAdj_Buffer.STDOUT:
            source = self.STDOUT
        elif _type_buffer == EnumAdj_Buffer.STDERR:
            source = self.STDERR
        else:
            msg = f"use only STDOUT/STDERR, {_type_buffer=}"
            raise Exc__Incompatible(msg)

        if isinstance(data, (str, bytes)):
            source.append(data)
        else:
            for item in data:
                self.append(data=item, _type_buffer=_type_buffer)

    def append_stdout(self, data: TYPING__CMD_LINES_DRAFT) -> None:
        return self.append(data=data, _type_buffer=EnumAdj_Buffer.STDOUT)

    def append_stderr(self, data: TYPING__CMD_LINES_DRAFT) -> None:
        return self.append(data=data, _type_buffer=EnumAdj_Buffer.STDERR)

    # -----------------------------------------------------------------------------------------------------------------
    def print_state(self, short: bool | None = None) -> None:
        if not short:
            print(f"="*50)

        if self.check_fail():
            print(f"[{'#'*21}ERROR{'#'*21}]")

        print(f"{self.INPUT=}")
        if not short:
            print(f"{self.duration=}")
            print(f"{self.check_success()=}")
            print(f"{self.retcode=}")
            print(f"{self.timedout=}")
            print(f"{self.finished=}")
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
