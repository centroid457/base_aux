"""
IDEAS
-----
TableLine
    - work with all insts in one group
    - unnamed collection
TableKit
    - work with all insts in all groups
    - named collection (dict-like)
TableColumn
    - work with all insts in one column (useful for instances like TestCase)

USAGE
-----
1. creating Table
2. using like simple collections (iterable/gi)
"""

# =====================================================================================================================

from base_aux.base_values.m3_exceptions import *
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

    def __iter__(self) -> Iterable[Any]:
        """
        GOAL
        ----
        iter all instances in line

        NOTE-IMPORTANT
        --------------
        if instance IS (not EQ!) previous instance - skip!
        it NEED for applying several ATC for some groups (3 ATC for 12 PTB, so there are 1 ATC for 4 PTB)

        SO as result
            self.INSTS != [*self]
            len(self.INSTS) == len(self) >= [*self]
        """
        inst_prev = None
        for inst in self.INSTS:
            if inst is not inst_prev:
                inst_prev = inst
                yield inst

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

    # def __getattr__(self, item: str) -> Self | NoReturn:    # NOTE: DONT USE IT!!! CANT compose result with called value
    #     """
    #     GOAL
    #     ----
    #     used as calling methods on all INSTS
    #     """
    #     result = []
    #     for inst in self.INSTS:
    #         try:
    #             result_i = getattr(inst, item)
    #         except Exception as exc:
    #             result_i = exc
    #
    #         result.append(result_i)
    #
    #     return TableLine(*result)

    def __len__(self) -> int:
        """
        GOAL
        ----
        return number of line instances

        if one instance for all Columns - return 1
        """
        return len(self.INSTS)

    def __call__(self, meth: str, *args, **kwargs) -> list[Any | Exception]:        # TODO: APPLY TableLine as result???
        """
        GOAL
        ----
        call method on all instances
        """
        results = []
        inst_prev = None
        for inst in self.INSTS:
            if inst is not inst_prev:
                inst_prev = inst
                try:
                    inst_meth = getattr(inst, meth)
                    ints_result = inst_meth(*args, **kwargs)
                except Exception as exc:
                    ints_result = exc
            else:
                ints_result = results[-1]

            results.append(ints_result)

        return results

    @property
    def COUNT(self) -> int:
        """
        preferred using direct LEN???
        """
        return len(self.INSTS)

    def __eq__(self, other: Any | Self) -> bool:    # DECIDE: delete? it is not needed???
        """
        CREATED SPECIALLY FOR
        ---------------------
        just testing perpose! not a real tip!
        """
        if isinstance(other, TableLine):
            if self.COUNT == other.COUNT:
                for inst1, inst2 in zip(self.INSTS, other.INSTS):
                    if inst1 != inst2:
                        return False
                return True
            else:
                return False
        else:
            # VAR-1=BAD! not clear and DIFFICALT!
            # what if (INSTS-Single and Other-Multy) or ViceVersa
            # return other == self.INSTS

            # VAR-2=best way
            return False


# =====================================================================================================================
class TableKit:     # todo: add AttrsKit nesting???
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
    def _init_new_lines(self, **lines: TableLine) -> None | NoReturn:
        # TODO: add/extend in annotations???? - not really need!

        for name, value in lines.items():
            if isinstance(value, TableLine):
                setattr(self, name, value)
            else:
                msg = f"{value=} is not TableLine type"
                raise Exc__WrongUsage(msg)

    def _init_count_columns(self) -> None:
        for name, line in self.items():
            self.COUNT_COLUMNS = line.COUNT

    def _check_same_counts(self) -> None | NoReturn:
        for name, line in self.items():
            if line.COUNT not in [self.COUNT_COLUMNS, 1]:
                msg = f"{name=}/{line.COUNT=}/{self.COUNT_COLUMNS=}"
                raise Exc__WrongUsage(msg)

    # -----------------------------------------------------------------------------------------------------------------
    def __len__(self) -> int:
        """
        GOAL
        ----
        return count
        """
        return len(self.names())

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
            raise Exc__WrongUsage(msg)

    def size(self) -> tuple[int, int]:
        return len(self), self.COUNT_COLUMNS

    # -----------------------------------------------------------------------------------------------------------------
    def __contains__(self, item: str) -> bool:
        """
        GOAL
        ----
        check just name line exist in lines
        """
        return item in self.names()

    def __getitem__(self, item: str) -> TableLine | NoReturn:
        """
        GOAL
        ----
        access to LINE over str name!
        just as additional ability! - but its is really need in GUI tableModel
        """
        result = getattr(self, item)
        if isinstance(result, TableLine):
            return result
        else:
            msg = f"no TableLine item in LINES [{item=}]"
            raise Exc__Addressing(msg)

    # -----------------------------------------------------------------------------------------------------------------
    def items(self) -> Iterable[tuple[str, TableLine]]:
        """
        NOTE/CAREFUL!
        ----
        iterate in DIR ORDER!!! not as defined!
        """
        # TODO: apply Annotated aatrs only???   - not really need!
        for name in dir(self):
            # print(f"items={name=}")
            if name.startswith("_"):
                continue
            value = getattr(self, name)
            if isinstance(value, TableLine):
                yield name, value

    def names(self) -> list[str]:   # DONT USE SET!!!
        result = []
        for name, value in self.items():
            result.append(name)
        return result

    def values(self) -> list[TableLine]:
        """
        NOTE
        ----
        lineInstances (TableLine())! not internal Line instances(TableLine().INSTS)!
        """
        result = []
        for name, value in self.items():
            result.append(value)
        return result

    def iter_lines_insts(self) -> Iterable[Any]:
        """
        GOAL
        ----
        iter ALL instances from all LINES!
        """
        for line in self.values():
            yield from line

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
    LINES: TableKit = TableKit()   # access for all lines!
    INDEX: int

    def __init__(self, index: int, lines: TableKit = None) -> None | NoReturn:
        if lines is not None:
            self.LINES = lines

        if not isinstance(self.LINES, TableKit):
            msg = f"{self.LINES=} is non type(TableKit)"
            raise Exc__WrongUsage(msg)

        if index + 1 > self.LINES.COUNT_COLUMNS:
            msg = f"{index=}/{self.LINES.COUNT_COLUMNS=}"
            raise Exc__Addressing(msg)

        self.INDEX = index

    def __getattr__(self, item: str) -> Any | NoReturn:
        """
        GOAL
        ----
        get index from exact line by name

        """
        # if not hasattr(self, "LINES"):
        #     raise Exception("hello")

        line: TableLine = getattr(self.LINES, item)
        if isinstance(line, TableLine):     # as Line
            return line[self.INDEX]

        elif isinstance(line, list):        # as list                       # todo: decide is it really need?
            return line[self.INDEX]

        else:                               # as direct ATTR from LINES     # todo: decide is it really need? couse all LineAttrs would return
            return line


# =====================================================================================================================
