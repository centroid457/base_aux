from typing import *

from base_aux.base_statics.m2_exceptions import *
from base_aux.aux_argskwargs.m1_argskwargs import *


# =====================================================================================================================
class TableLine:
    """
    GOAL
    ----
    smth like a group with several or one instances

    GI-access to elements.
        RETURN
            if INSTS multy - return source[index]
            otherwise - INSTS[0]

    SPECIALLY CREATED FOR
    ---------------------
    simplifying work with Breeder like object!
    (most important difference is working with already generated Elements!)
    """
    INSTS: tuple[Any, ...]

    def __init__(self, *insts: Any) -> None:
        """
        if one instance for all Columns - use one instance
        if used several instances - use exact count - each inst for each Columns
        """
        self.INSTS = insts

    def __iter__(self):
        """
        GOAL
        ----
        iter all instances in line
        """
        yield from self.INSTS

    def __contains__(self, item) -> bool:
        return item in self.INSTS

    def __getitem__(self, index: int) -> Any | NoReturn:
        """
        GOAL
        ----
        access to exact instance by index
        """
        if len(self.INSTS) == 1:
            return self.INSTS[0]
        else:
            return self.INSTS[index]

    def __len__(self):
        """
        GOAL
        ----
        return number of line instances

        if one instance for all Columns - return 1
        """
        return len(self.INSTS)

    def __call__(self, meth: str, *args, **kwargs) -> list[Any | Exception]:
        """
        GOAL
        ----
        call method on all instances
        """
        results = []
        for inst in self.INSTS:
            try:
                inst_meth = getattr(inst, meth)
                ints_result = inst_meth(*args, **kwargs)
                results.append(ints_result)
            except Exception as exx:
                results.append(exx)

        return results

    @property
    def COUNT(self) -> int | None:
        """
        preferred using direct LEN???
        """
        return len(self.INSTS)


# =====================================================================================================================
class TableLines:
    """
    GOAL
    ----
    just as object keeping sets for all lines

    USAGE
    =====
    two ways to define object
    -------------------------
        1=by direct set cls attrs
        2=by init kwargs

    create/use Instance
    -------------------
    """
    _count_columns: int = 1

    def __init__(self, **lines: TableLine) -> None | NoReturn:
        self._init_new_lines(**lines)
        self._init_count_columns()
        self._check_same_counts()

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def COUNT_COLUMNS(self) -> int:
        return self._count_columns

    @COUNT_COLUMNS.setter
    def COUNT_COLUMNS(self, new: int) -> None | NoReturn:
        if new == 1:
            return

        if self._count_columns == 1:
            self._count_columns = new
        elif self._count_columns != new:
            msg = f"{new=}/{self.COUNT_COLUMNS=}"
            raise Exx__WrongUsage(msg)

    # -----------------------------------------------------------------------------------------------------------------
    def _init_new_lines(self, **lines: TableLine) -> None:
        for name, value in lines.items():
            if isinstance(value, TableLine):
                setattr(self, name, value)
            else:
                msg = f"{value=} is not TableLine type"
                raise Exx__WrongUsage(msg)

    def _init_count_columns(self) -> None | NoReturn:
        for name, line in self.items():
            self.COUNT_COLUMNS = line.COUNT

    def _check_same_counts(self) -> None | NoReturn:
        for name, line in self.items():
            if line.COUNT not in [self.COUNT_COLUMNS, 1]:
                msg = f"{name=}/{line.COUNT=}/{self.COUNT_COLUMNS=}"
                raise Exx__WrongUsage(msg)

    # -----------------------------------------------------------------------------------------------------------------
    def __contains__(self, item: str) -> bool:
        """
        GOAL
        ----
        check just name line exist in lines
        """
        return item in self.names()

    # -----------------------------------------------------------------------------------------------------------------
    def items(self) -> Iterable[tuple[str, TableLine]]:
        for name in dir(self):
            print(f"items={name=}")
            if name.startswith("_"):
                continue
            value = getattr(self, name)
            if isinstance(value, TableLine):
                yield name, value

    def names(self) -> list[str]:
        result = []
        for name, value in self.items():
            result.append(name)
        return result

    def values(self) -> list[TableLine]:
        result = []
        for name, value in self.items():
            result.append(value)
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def __call__(self, meth: str, *args, **kwargs) -> dict[str, list[Any | Exception]]:
        """
        GOAL
        ----
        call method on all lines
        """
        results = {}
        for name, line in self.items():
            results.update({name: line(meth, *args, **kwargs)})

        return results


# =====================================================================================================================
class TableColumn:
    """
    GOAL
    ----
    replace/ref breederObject!
    access to exact instance in line by simple name (implying index)
    """
    LINES: TableLines   # = TableLines()   # access for all lines!
    INDEX: int

    def __init__(self, index: int) -> None | NoReturn:
        if index + 1 > self.LINES.COUNT_COLUMNS:
            msg = f"{index=}/{self.LINES.COUNT_COLUMNS=}"
            raise Exx__Addressing(msg)

        self.INDEX = index

    def __getattr__(self, item: str) -> Any | NoReturn:
        line: TableLine = getattr(self.LINES, item)
        return line[self.INDEX]


# =====================================================================================================================
