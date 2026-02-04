from typing import *

from base_aux.base_histories.m1_io_item import IoItem


# =====================================================================================================================
# TODO:
#   1. use deque with base_types Write Read WEol REol None(not used)?
#   2. add top(n=10)
#   if when writeLine - always readLines?

TYPING__IO_OUTPUT_DRAFT =  str | list[str]
TYPING__IO_ITEM_DRAFT = IoItem | tuple[str, str | list[str]]
TYPING__IO_HISTORY_DRAFT = list[IoItem] | list[tuple[str, list[str]]]


# =====================================================================================================================
class IoHistory:
    """
    GOAL
    ----
    collect IO (request/response) sequence

    CONSTRAINTS
    -----------
    always use "" instead of None in value lines
    """
    _history: list[IoItem]

    def __init__(self, source: Self | TYPING__IO_HISTORY_DRAFT | None = None) -> None:
        self._history = []
        if not source:
            pass
        elif isinstance(source, self.__class__):
            self._history = source._history
        elif isinstance(source, list):
            for item in source:
                self.add_item(item)

    # -----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other: Self | TYPING__IO_HISTORY_DRAFT) -> bool:
        # 1=prepare
        if isinstance(other, self.__class__):
            if len(self) != len(other):
                return False
        else:
            other = self.__class__(other)
            return self == other

        # 2=check
        for item_source, item_other in zip(self, other):
            if item_source != item_other:
                return False

        return True

    # -----------------------------------------------------------------------------------------------------------------
    def __iter__(self) -> IoItem:
        yield from self._history

    def __getitem__(self, item: int | str) -> IoItem | list[str] | NoReturn:
        """
        GOAL
        ----
        get
        1/ IoItem from history for passed int as index
        2/ output for passed string as input
        """
        if isinstance(item, int):
            return self._history[item]
        if isinstance(item, str):
            for io_item in self:
                if io_item.INPUT == item:
                    return io_item.OUTPUT

    def __len__(self) -> int:
        return len(self._history)

    def count(self) -> int:
        return len(self._history)

    # -----------------------------------------------------------------------------------------------------------------
    def clear(self) -> None:
        self._history.clear()

    # -----------------------------------------------------------------------------------------------------------------
    def add_item(self, data: IoItem | tuple[str, str | list[str]]) -> None:
        if isinstance(data, IoItem):
            self._history.append(data)
        if isinstance(data, tuple):
            input, output = data
            if isinstance(output, str):
                output = [output, ]
            self._history.append(IoItem(input, output))

    def add_input(self, data: str) -> None:
        self._history.append(IoItem(data))

    def add_output(self, data: TYPING__IO_OUTPUT_DRAFT) -> None:
        # init base
        if not self._history:
            self.add_input("")

        if isinstance(data, (tuple, list, )):
            self.last_outputs.extend(data)
        else:
            # SINGLE
            self.last_outputs.append(data)

    def add_io(self, data_i: str, data_o: TYPING__IO_OUTPUT_DRAFT) -> None:
        self.add_item((data_i, data_o))

    def add_history(self, data: Self) -> None:
        for item in data:
            self.add_item(item)

    # =================================================================================================================
    @property
    def last_io_item(self) -> IoItem | None:
        try:
            return self._history[-1]
        except:
            return None

    @property
    def last_input(self) -> str:
        try:
            return self.last_io_item.INPUT
        except:
            return ""

    @property
    def last_outputs(self) -> list[str]:
        try:
            return self.last_io_item.OUTPUT
        except:
            return []

    @property
    def last_output(self) -> str:
        try:
            return self.last_outputs[-1]
        except:
            return ""

    # -----------------------------------------------------------------------------------------------------------------
    def list_input(self) -> list[str]:
        result = []
        for item in self._history:
            result.append(item.INPUT)
            print(item.INPUT)
        return result

    def list_output(self) -> list[str]:
        result = []
        for item in self._history:
            for line in item.OUTPUT:
                result.append(line)
                print(line)
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def print_io(self) -> None:
        """
        GOAL
        ----
        just print history
        """
        title = f"{self.__class__.__name__}.print_io".upper()
        print()
        print("="*10 + f"{title:=<90}")
        for item in self._history:
            print(f"{item.INPUT:20}:", end="")
            indent = ""
            if item.OUTPUT:
                for line in item.OUTPUT:
                    line = f"{indent}{line}"
                    print(line)
                    indent = " "*20 + ":"
            else:
                print()
        print("="*100)

    def as_dict(self) -> dict[str, list[str]]:
        """
        CAREFUL
        -------
        not correct if exists same input lines
        """
        result = {}
        for item in self._history:
            result[item.INPUT] = item.OUTPUT

        return result


# =====================================================================================================================
