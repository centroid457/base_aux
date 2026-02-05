from typing import *
import time

from dataclasses import dataclass, field
from base_aux.base_enums.m2_enum1_adj import EnumAdj_Buffer
from base_aux.base_values.m3_exceptions import *


# =====================================================================================================================
@dataclass
class IoItem:
    """
    GOAL
    ----
    replace old history variant like simple tuple
    """
    INPUT: str = ""    # dont use collection on input!!! dont use None here!
    STDOUT: list[str] = field(default_factory=list)

    def append(self, data: str | Collection[str]) -> None | NoReturn:
        """
        GOAL
        ----
        append means only for output!
        for input try set it on inition only!
        """
        if isinstance(data, str):
            self.STDOUT.append(data)
        else:
            for item in data:
                self.append(item)

    def __str__(self) -> str:
        result = f"{self.__class__.__name__}({self.INPUT=},{self.STDOUT=})"
        return result


# =====================================================================================================================
@dataclass
class IoeItem(IoItem):
    """
    GOAL
    ----
    improve simple variant IoItem
    """
    INPUT: str = ""    # dont use collection on input!!! dont use None here!
    STDOUT: list[str] = field(default_factory=list)
    STDERR: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.duration: float = 0
        self._time_start: float = time.time()

    def __str__(self) -> str:
        result = f"{self.__class__.__name__}({self.INPUT=},{self.STDOUT=},{self.STDERR=})"
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def append(self, data: str | Collection[str], type_buffer: EnumAdj_Buffer = EnumAdj_Buffer.STDOUT) -> None | NoReturn:
        self.duration = time.time() - self._time_start

        if type_buffer == EnumAdj_Buffer.STDOUT:
            source = self.STDOUT
        elif type_buffer == EnumAdj_Buffer.STDERR:
            source = self.STDERR
        else:
            msg = f"use only STDOUT/STDERR, {type_buffer=}"
            raise Exc__Incompatible(msg)

        if isinstance(data, str):
            source.append(data)
        else:
            for item in data:
                self.append(data=item, type_buffer=type_buffer)

    def append_stdout(self, data: str | Collection[str]) -> None:
        return self.append(data=data, type_buffer=EnumAdj_Buffer.STDOUT)

    def append_stderr(self, data: str | Collection[str]) -> None:
        return self.append(data=data, type_buffer=EnumAdj_Buffer.STDERR)


# =====================================================================================================================
