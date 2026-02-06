from typing import *

from base_aux.base_values.m3_exceptions import *
from base_aux.cmds.m1_result import CmdResult


# =====================================================================================================================
# TODO:
#   1. use deque with base_types Write Read WEol REol None(not used)?
#   2. add top(n=10)
#   if when writeLine - always readLines?

TYPING__IO_OUTPUT_DRAFT = str | list[str]
TYPING__IO_ITEM_DRAFT = CmdResult | tuple[str, str | list[str]]
TYPING__IO_HISTORY_DRAFT = list[CmdResult] | list[tuple[str, list[str]]]


# =====================================================================================================================
class CmdHistory:
    """
    GOAL
    ----
    collect IO (request/response) sequence

    CONSTRAINTS
    -----------
    always use "" instead of None in value lines
    """
    _history: list[CmdResult]

    def __init__(self, source: Self | TYPING__IO_HISTORY_DRAFT | None = None) -> None:
        self._history = []
        if not source:
            pass
        elif isinstance(source, self.__class__):
            self._history = list(source._history)
        elif isinstance(source, list):
            for item in source:
                self.add_result(item)

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
    def __iter__(self) -> CmdResult:
        yield from self._history

    def __getitem__(self, item: int | str) -> CmdResult | list[str] | NoReturn:
        """
        GOAL
        ----
        get
        1/ CmdResult from history for passed int as index
        2/ output for passed string as input
        """
        if isinstance(item, int):
            return self._history[item]
        elif isinstance(item, str):
            for io_item in self:
                if io_item.INPUT == item:
                    return io_item.STDOUT
            msg = f"not found/{item=}"
        else:
            msg = f"incompatiible type/{item=}"
        raise Exception(msg)

    def __len__(self) -> int:
        return len(self._history)

    # -----------------------------------------------------------------------------------------------------------------
    def clear(self) -> None:
        self._history.clear()

    # =================================================================================================================
    def add_result(
            self,
            data: CmdResult | tuple[str, TYPING__IO_OUTPUT_DRAFT] | tuple[str, TYPING__IO_OUTPUT_DRAFT, TYPING__IO_OUTPUT_DRAFT]
    ) -> None:
        if isinstance(data, CmdResult):
            pass
        elif isinstance(data, tuple):
            data = CmdResult(*data)

        try:
            self._history.append(data)
        except Exception as exc:
            msg = f"{data=}/{exc!r}"
            raise Exc__Incompatible(msg)

    # -----------------------------------------------------------------------------------------------------------------
    def append_input(self, data: str) -> None:
        self._history.append(CmdResult(data))

    def append_stdout(self, data: TYPING__IO_OUTPUT_DRAFT) -> None:
        # init base
        if not self._history:
            self.append_input("")

        self.last_result.append_stdout(data)

    def append_stderr(self, data: TYPING__IO_OUTPUT_DRAFT) -> None:
        # init base
        if not self._history:
            self.append_input("")

        self.last_result.append_stderr(data)

    def add_ioe(
            self,
            data_i: str,
            data_o: TYPING__IO_OUTPUT_DRAFT | None = None,
            data_e: TYPING__IO_OUTPUT_DRAFT | None = None,
    ) -> None:
        self.add_result((data_i, data_o, data_e))

    def add_history(self, data: Self) -> None:
        for item in data:
            self.add_result(item)

    # =================================================================================================================
    @property
    def last_result(self) -> CmdResult | None:
        try:
            return self._history[-1]
        except:
            return None

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def last_input(self) -> str:
        try:
            return self.last_result.INPUT
        except:
            return ""

    @property
    def last_stdout_buff(self) -> list[str]:
        try:
            return self.last_result.STDOUT
        except:
            return []

    @property
    def last_stdout_line(self) -> str:
        try:
            return self.last_result.STDOUT[-1]
        except:
            return ""

    @property
    def last_stderr_buff(self) -> list[str]:
        try:
            return self.last_result.STDERR
        except:
            return []

    @property
    def last_stderr_line(self) -> str:
        try:
            return self.last_result.STDERR[-1]
        except:
            return ""

    # =================================================================================================================
    def list_input(self) -> list[str]:
        result = []
        for item in self._history:
            result.append(item.INPUT)
            print(item.INPUT)
        return result

    def list_stdout_lines(self) -> list[str]:
        result = []
        for h_result in self._history:
            result.extend(h_result.STDOUT)
        return result

    def list_stderr_lines(self) -> list[str]:
        result = []
        for h_result in self._history:
            result.extend(h_result.STDERR)
        return result

    def list_stdouterr_lines(self) -> list[str]:
        result = []
        for h_result in self._history:
            result.extend(h_result.STDOUTERR)
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
        for result in self._history:
            print(f"{result.INPUT:20}:", end="")
            indent = ""
            for buffer in [result.STDOUT, result.STDERR]:
                for line in buffer:
                    line = f"{indent}{line}"
                    print(line)
                    indent = " "*20 + ":"
        print("="*100)

    def as_dict(self) -> dict[str, list[str]]:
        """
        GOAL
        ----
        get table results   # TODO: DEPRECATE!!! maybe not useful! use direct clear exact values!

        CAREFUL
        -------
        not correct if exists same input lines
        """
        result = {}
        for item in self._history:
            result[item.INPUT] = item.STDOUTERR

        return result


# =====================================================================================================================
