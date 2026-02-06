from typing import *
from datetime import datetime

from dataclasses import dataclass, field
from base_aux.base_enums.m2_enum1_adj import EnumAdj_Buffer
from base_aux.base_values.m3_exceptions import *


# =====================================================================================================================
@dataclass
class CmdResult:
    """
    GOAL
    ----
    keep all data for command request

    CONSTRAINTS
    -----------
    1. all data lines are str! - json is not expecting!
    """
    INPUT: str = ""    # dont use collection on input!!! dont use None here!
    STDOUT: list[str] = field(default_factory=list)
    STDERR: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.timestamp: datetime = datetime.now()
        self.duration: float = 0
        self.retcode: int | None = None

        if self.STDOUT is None:
            self.STDOUT = []
        elif isinstance(self.STDOUT, str):
            self.STDOUT = [self.STDOUT, ]

        if self.STDERR is None:
            self.STDERR = []
        elif isinstance(self.STDERR, str):
            self.STDERR = [self.STDERR, ]

    def __str__(self) -> str:
        result = f"{self.__class__.__name__}({self.INPUT=},{self.STDOUT=},{self.STDERR=})"
        return result

    @property
    def STDOUTERR(self) -> list[str]:
        return [*self.STDOUT, *self.STDERR]

    # -----------------------------------------------------------------------------------------------------------------
    def append(
            self,
            data: str | Collection[str],
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

        if isinstance(data, str):
            source.append(data)
        else:
            for item in data:
                self.append(data=item, _type_buffer=_type_buffer)

    def append_stdout(self, data: str | Collection[str]) -> None:
        return self.append(data=data, _type_buffer=EnumAdj_Buffer.STDOUT)

    def append_stderr(self, data: str | Collection[str]) -> None:
        return self.append(data=data, _type_buffer=EnumAdj_Buffer.STDERR)


# =====================================================================================================================
