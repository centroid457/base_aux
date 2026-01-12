from typing import *

from base_aux.tables.m1_table_obj import TableObj


# =====================================================================================================================
class TableObj_Column:
    """
    GOAL
    ----
    get item by name+index_column from Table
    just an attempt for simplification access to exact index item from list

    but you can access it directly by
        dev_table.ATC[index]
    instead
        dev_table_column.ATC
    """
    table: TableObj
    column: int

    def __init__(self, *, column: int, table: TableObj) -> None | NoReturn:
        self.column = column
        self.table = table

    def __getitem__(self, item: str) -> Any | NoReturn:
        return self.table[item][self.column]


# =====================================================================================================================
