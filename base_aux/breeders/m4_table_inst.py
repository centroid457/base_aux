from typing import *
from enum import Enum, auto

from base_aux.base_statics.m2_exceptions import *
from base_aux.aux_attr.m1_annot_attr1_aux import *

from base_aux.base_nest_dunders.m3_calls import *
from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.aux_argskwargs.m1_argskwargs import *


# =====================================================================================================================
TYPING__INST_OR_INST_LIST = Union[Any, tuple[Any, ...]]


# =====================================================================================================================
class TableInstLine:
    """
    GOAL
    ----
    smth like a group with several or one instances

    keep LIST[Any] or Single Any instance in Source.
    GI-access to elements.
    RETURN
        if INSTS is list - return source[index]
        otherwise - INSTS

    SPECIALLY CREATED FOR
    ---------------------
    simplifying work with Breeder like object!
    most important is wotk with already generated Elements!
    """
    # DONT multiply single instance into list!
    INSTS: TYPING__INST_OR_INST_LIST

    def __init__(self, *insts) -> None:
        self.INSTS = insts

    def __iter__(self):
        """
        GOAL
        ----
        iter all instances in line
        """
        yield from self.INSTS

    def __contains__(self, item):
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
        """
        return len(self.INSTS)

    def __call__(self, meth: str, *args, **kwargs) -> list[Any | Exception]:
        """
        GOAL
        ----
        call method on all instances
        """
        results = []
        for inst in self:
            try:
                inst_meth = getattr(inst, meth)
                ints_result = inst_meth(*args, **kwargs)
            except Exception as exx:
                ints_result = exx
            results.append(ints_result)

        return results

    @property
    def COUNT(self) -> int | None:
        """
        preferred using direct LEN???
        """
        return len(self.INSTS)


# =====================================================================================================================
class TableInst(NestInit_Source):
    """
    GOAL
    ----
    collect all tableLines (objects) in one object
    """
    SOURCE: dict[str, TableInstLine]

    def init_post(self) -> None | NoReturn:
        self._check_length()

    # ----------------------------------------------------------
    def __contains__(self, item: str) -> bool:
        """
        GOAL
        ----
        check just name exist in table
        """
        return item in self.SOURCE

    def lines_names(self) -> list[str]:
        return list(self.SOURCE)

    def _check_length(self) -> None | NoReturn:
        count_found_first: int | None = None

        for name, line in self.SOURCE.items():
            if line.COUNT is None:
                continue
            else:
                if count_found_first is None:
                    count_found_first = line.COUNT
                if count_found_first != line.COUNT:
                    msg = f"[ERR] incorrect length {name=}/{line.COUNT=}/{count_found_first=}"
                    print(msg)
                    raise Exx__WrongUsage(msg)

    def line__insts(self, name: str) -> TYPING__INST_OR_INST_LIST | NoReturn:
        return getattr(self, name).SOURCE

    def line_call__(self, meth: str, name: str | None = None, args: list | None = None, kwargs: dict | None = None) -> Union[NoReturn, TYPING__BREED_RESULT__GROUP, TYPING__BREED_RESULT__GROUPS]:
        """
        call one method on exact group (every object in group) or all groups (every object in all groups).
        created specially for call connect/disconnect for devices in TP.

        :param meth:
        :param group:

        :param args:
        :param kwargs:
        :return:
            RAISE only if passed group and group is not exists! or groups are not generated
        """
        args = args or ()
        kwargs = kwargs or {}

        # ALL GROUPS -------------------------------------------------
        if name is None:
            results = {}
            for group_name in self.lines_names():
                results.update({group_name: self.line_call__(meth, group_name, args, kwargs)})
            return results

        # if group is not exists ---------------------------------------------
        if group not in self.lines_names():
            raise Exx__NotExistsNotFoundNotCreated(group)

        # ONE GROUP ----------------------------------------------------
        group_objs = self.group_get__insts(group)

        if isinstance(group_objs, list):    # LIST
            results = []
            for obj in group_objs:
                try:
                    obj_meth = getattr(obj, meth)
                    obj_result = obj_meth(*args, **kwargs)
                except Exception as exx:
                    obj_result = exx
                results.append(obj_result)
        else:           # SINGLE
            obj = group_objs
            try:
                obj_meth = getattr(obj, meth)
                obj_result = obj_meth(*args, **kwargs)
            except Exception as exx:
                obj_result = exx
            results = obj_result

        return results


# =====================================================================================================================
class TableItems_Index:
    """
    GOAL
    ----
    replace/ref breederObject!
    """
    ITEMS: TableItems_Groups = TableItems_Groups()   # access for all lists!
    INDEX: int

    def __init__(self, index: int) -> None | NoReturn:
        if index + 1 > self.ITEMS.COUNT:
            msg = f"{index=}/{self.ITEMS.COUNT=}"
            raise Exx__Addressing(msg)

        self.INDEX = index

    def __getattr__(self, item: str) -> Any | NoReturn:
        group_items = getattr(self.ITEMS, item)
        if isinstance(group_items, list):
            return group_items[self.INDEX]
        else:
            return group_items      # as final SINGLE value!

    # def group_call__(self):   # DONT ADD HERE!!! use over GROUPS only!!!


# =====================================================================================================================
