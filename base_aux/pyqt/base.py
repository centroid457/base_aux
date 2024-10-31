from typing import *


# TEST STUFF ==========================================================================================================
class Row_:
    NAME: str = "row"
    SKIP: Optional[bool] = None
    result: Optional[bool] = None

    def __init__(self, name: Optional[Any] = None):
        if name:
            self.NAME = str(name)


class Dev_:
    NAME: str = "dev"
    SKIP: Optional[bool] = None
    result: Optional[bool] = None

    def __init__(self, name: Optional[Any] = None):
        if name:
            self.NAME = str(name)

    def SKIP_reverse(self) -> None:
        self.SKIP = not bool(self.SKIP)

class Data_:
    ROWS: list[Row_] = None
    DEVS: list[Dev_] = None

    def __init__(self, rows: list[Row_], devs: list[Dev_]):
        self.ROWS = rows
        self.DEVS = devs


# =====================================================================================================================
