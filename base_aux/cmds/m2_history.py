from typing import *

from base_aux.base_values.m3_exceptions import *
from base_aux.cmds.m1_result import *


# =====================================================================================================================
# TODO:
#   1. use deque with base_types Write Read WEol REol None(not used)?
#   if when writeLine - always readLines?


# =====================================================================================================================
TYPING__CMD_RESULT_DRAFT = CmdResult | tuple[TYPING__CMD_LINE, TYPING__CMD_LINES_DRAFT] | tuple[TYPING__CMD_LINE, TYPING__CMD_LINES_DRAFT, TYPING__CMD_LINES_DRAFT]
TYPING__CMD_HISTORY_DRAFT = list[TYPING__CMD_RESULT_DRAFT]


# =====================================================================================================================
class CmdHistory:
    """
    GOAL
    ----
    collect IO (request/response) sequence
    and manage it
        - cumulate is_succcess
        - get last result
        - get last line from any buff
        - collect same buffers

    use actual state for outside objects!
        if send input - show it immediately!
        no need to wait any timeout or exiting send method.
        so if you start using any bus and send cmd
            1. dont create CmdResult
            2. dont manipulate by CmdResult directly
            3. manage all by CmdHistory object! over its methods

    CONSTRAINTS
    -----------
    always use "" instead of None in value lines
    """
    _history: list[CmdResult]

    def __init__(self, source: Self | TYPING__CMD_HISTORY_DRAFT | None = None) -> None:
        self._history = []

        if not source:
            pass
        elif isinstance(source, self.__class__):
            self._history = list(source._history)
        elif isinstance(source, list):
            for item in source:
                self._add_result(item)
                # self.set_finished()

    # -----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other: Self | TYPING__CMD_HISTORY_DRAFT) -> bool:
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
    def __getitem__(self, item: int | TYPING__CMD_LINE) -> CmdResult | list[TYPING__CMD_LINE] | NoReturn:
        """
        GOAL
        ----
        get
        1/ CmdResult from history for passed int as index
        2/ output for passed string as input
        """
        if isinstance(item, int):
            return self._history[item]
        elif isinstance(item, (str, bytes)):
            for io_item in self:
                if io_item.INPUT == item:
                    return io_item.STDOUT
            msg = f"not found/{item=}"
        else:
            msg = f"incompatible type/{item=}"
        raise Exception(msg)

    # -----------------------------------------------------------------------------------------------------------------
    def __iter__(self) -> CmdResult:
        yield from self._history

    def __len__(self) -> int:
        return len(self._history)

    # -----------------------------------------------------------------------------------------------------------------
    def clear(self) -> None:
        self._history.clear()

    # -----------------------------------------------------------------------------------------------------------------
    def check_finished(self) -> bool:
        """
        GOAL
        ----
        last result is finished (all are finished).
        so history is free to go! feel free to start new stepResult
        """
        if self.last_result is None:
            return False
        else:
            return self.last_result.check__finished()

    def set_finished(self, status: EnumAdj_FinishedStatus | None = None) -> None:
        if self.last_result is not None:
            return self.last_result.set_finished(status)

    # -----------------------------------------------------------------------------------------------------------------
    def check_all_success(self) -> bool:
        """
        GOAL
        ----
        all results are success

        SPECIALLY CREATED FOR
        ---------------------
        send some batch of cmds and check are all success to future work in cli
        so we could do pre validation
        """
        for result in self._history:
            if result.check__fail():
                return False
        return True

    def check_any_fail(self) -> bool:
        """
        GOAL
        ----
        any result is fail
        """
        return not self.check_all_success()

    # =================================================================================================================
    def _add_result(
            self,
            data: TYPING__CMD_RESULT_DRAFT,
    ) -> None | NoReturn:
        """
        GOAL
        ----
        this is the MAIN NewLine creation method.
        use all addings over this method!!!
        """
        # if self.last_result is not None and not self.check_finished():
        #     msg = f"cant start new CmdResult in history without finishing last one!!! {self.last_result=}"
        #     raise Exc__NotReady(msg)

        # --------------------------
        if isinstance(data, CmdResult):
            pass
        elif isinstance(data, tuple):
            data = CmdResult(*data)
        else:
            msg = f"expect CmdResult/tuple/{data=}"
            raise Exc__Incompatible(msg)

        try:
            self._history.append(data)
        except Exception as exc:
            msg = f"{data=}/{exc!r}"
            raise Exc__Incompatible(msg)

    # -----------------------------------------------------------------------------------------------------------------
    def add_input(self, data: TYPING__CMD_LINE) -> None | NoReturn:
        self._add_result(CmdResult(data))

    def add_ioe(
            self,
            data_i: TYPING__CMD_LINE,
            data_o: TYPING__CMD_LINES_DRAFT | None = None,
            data_e: TYPING__CMD_LINES_DRAFT | None = None,
    ) -> None | NoReturn:
        self._add_result((data_i, data_o, data_e))

    def add_history(self, data: Self) -> None | NoReturn:
        for item in data:
            self._add_result(item)

    # -----------------------------------------------------------------------------------------------------------------
    def append_stdout(self, data: TYPING__CMD_LINES_DRAFT) -> None:
        # init base
        if not self._history:
            self.add_input("")

        self.last_result.append_stdout(data)

    def append_stderr(self, data: TYPING__CMD_LINES_DRAFT) -> None:
        # init base
        if not self._history:
            self.add_input("")

        self.last_result.append_stderr(data)

    # =================================================================================================================
    @property
    def last_result(self) -> CmdResult | None:
        try:
            return self._history[-1]
        except:
            return None

    # @property
    # def prev_result(self) -> CmdResult | None:
    #     """
    #     GOAL
    #     ----
    #     if we have some new cmd to send but read new stdouterr before - # DONT NEED!!!  JUST CALL append_stdout!
    #     """
    #     try:
    #         return self._history[-2]
    #     except:
    #         return None

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def last_input(self) -> TYPING__CMD_LINE:
        try:
            return self.last_result.INPUT
        except:
            return ""

    @property
    def last_stdout_buff(self) -> list[TYPING__CMD_LINE]:
        try:
            return self.last_result.STDOUT
        except:
            return []

    @property
    def last_stdout_line(self) -> TYPING__CMD_LINE:
        try:
            return self.last_result.STDOUT[-1]
        except:
            return ""

    @property
    def last_stderr_buff(self) -> list[TYPING__CMD_LINE]:
        try:
            return self.last_result.STDERR
        except:
            return []

    @property
    def last_stderr_line(self) -> TYPING__CMD_LINE:
        try:
            return self.last_result.STDERR[-1]
        except:
            return ""

    # =================================================================================================================
    def list_input(self) -> list[TYPING__CMD_LINE]:
        result = []
        for item in self._history:
            result.append(item.INPUT)
            print(item.INPUT)
        return result

    def list_stdout_lines(self) -> list[TYPING__CMD_LINE]:
        result = []
        for h_result in self._history:
            result.extend(h_result.STDOUT)
        return result

    def list_stderr_lines(self) -> list[TYPING__CMD_LINE]:
        result = []
        for h_result in self._history:
            result.extend(h_result.STDERR)
        return result

    def list_stdouterr_lines(self) -> list[TYPING__CMD_LINE]:
        result = []
        for h_result in self._history:
            result.extend(h_result.STDOUTERR)
        return result

    # =================================================================================================================
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
            result.print_state()
        print("="*100)

    def _as_dict(self) -> dict[TYPING__CMD_LINE, list[TYPING__CMD_LINE]]:
        """
        GOAL
        ----
        unit testing!
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
