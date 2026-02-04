from typing import *

from dataclasses import dataclass, field


# =====================================================================================================================
@dataclass
class IoItem:
    """
    GOAL
    ----
    replace old history variant like simple tuple
    """
    INPUT: str = ""    # dont use collection on input!!! dont use None here!
    OUTPUT: list[str] = field(default_factory=list)

    def append(self, data: str | Collection[str]) -> None | NoReturn:
        """
        GOAL
        ----
        append means only for output!
        for input try set it on inition only!
        """
        if isinstance(data, str):
            self.OUTPUT.append(data)
        else:
            for item in data:
                self.append(item)

    def __str__(self) -> str:
        result = f"{self.__class__.__name__}({self.INPUT},{self.OUTPUT})"
        return result


# =====================================================================================================================
