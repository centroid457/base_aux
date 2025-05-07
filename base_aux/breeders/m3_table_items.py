from typing import *
from enum import Enum, auto

from base_aux.base_statics.m2_exceptions import *
from base_aux.aux_attr.m1_annot_attr1_aux import *

from base_aux.base_nest_dunders.m3_calls import *
from base_aux.base_nest_dunders.m1_init1_source import *


# =====================================================================================================================
TYPING__BREED_RESULT__ITEM = Union[Any, Exception]
TYPING__BREED_RESULT__GROUP = Union[
    TYPING__BREED_RESULT__ITEM,        # SINGLE variant
    list[TYPING__BREED_RESULT__ITEM]   # LIST variant
]
TYPING__BREED_RESULT__GROUPS = dict[str, TYPING__BREED_RESULT__GROUP]


# =====================================================================================================================
class Base_GenItems(NestInit_Source):
    """
    GOAL
    ----
    determine/show classes for Single/Multy objects
    with will generate list of objects by one fabric (Class/CallableFunc)

    SPECIALLY CREATED FOR
    ---------------------
    as part for TableItems (one list)
    """
    SOURCE: type[Any] | Callable[..., Any] | Any
    MULTYPLICITY: Enum_SingleMultiple = Enum_SingleMultiple.MULTIPLE
    CALLABILITY: Enum_StaticCallable = Enum_StaticCallable.CALLABLE

    def generate_items(self, count: int) -> Any | list[Any] | NoReturn:
        if self.MULTYPLICITY == Enum_SingleMultiple.SINGLE:
            if self.CALLABILITY == Enum_StaticCallable.CALLABLE:
                return self.SOURCE()
            else:
                return self.SOURCE
        elif self.MULTYPLICITY == Enum_SingleMultiple.MULTIPLE:
            result = []
            for index in range(count):
                if self.CALLABILITY == Enum_StaticCallable.CALLABLE:
                    item = self.SOURCE(index)
                else:
                    item = self.SOURCE

                result.append(item)
            return result
        else:
            msg = f"{self.MULTYPLICITY=}"
            print(msg)
            raise Exx__WrongUsage(msg)


# ---------------------------------------------------------------------------------------------------------------------
class GenItems_SingleStatic(Base_GenItems):
    SOURCE: type[Any] | Any
    MULTYPLICITY: Enum_SingleMultiple = Enum_SingleMultiple.SINGLE
    CALLABILITY: Enum_StaticCallable = Enum_StaticCallable.STATIC


class GenItems_SingleCallable(Base_GenItems):
    SOURCE: type[Any] | Callable[..., Any]
    MULTYPLICITY: Enum_SingleMultiple = Enum_SingleMultiple.SINGLE
    CALLABILITY: Enum_StaticCallable = Enum_StaticCallable.CALLABLE


# ---------------------------------------------------------------------------------------------------------------------
class GenItems_MultyStatic(Base_GenItems):
    SOURCE: type[Any] | Any
    MULTYPLICITY: Enum_SingleMultiple = Enum_SingleMultiple.MULTIPLE
    CALLABILITY: Enum_StaticCallable = Enum_StaticCallable.STATIC


class GenItems_MultyCallable(Base_GenItems):
    SOURCE: type[Any] | Callable[..., Any]
    MULTYPLICITY: Enum_SingleMultiple = Enum_SingleMultiple.MULTIPLE
    CALLABILITY: Enum_StaticCallable = Enum_StaticCallable.CALLABLE


# =====================================================================================================================
class TableItems:
    """
    GOAL
    ----
    collect all object lists in one object
    as collection for generated objects

    SPECIALLY CREATED FOR
    ---------------------
    ITEMS in TableItemsIndex as access for all lists
    """
    COUNT: int = 1
    # SINGLE1: Base_GenItems | Any = ItemSingle("single")
    # MULTY1: Base_GenItems | list[Any] = [i * 10 for i in range(3)]

    def __init__(self, count: int = None) -> None | NoReturn:
        if count is not None:
            self.COUNT = count
        self._generate_groups()
        self._check_length()

    def __contains__(self, item: str) -> bool:
        return item in self.group_names()

    def group_names(self) -> list[str]:
        result = []
        for name in AnnotsAllAux(self).iter__names_not_hidden():
            if name != "COUNT":
                result.append(name)
        return result

    def _check_length(self) -> None | NoReturn:
        groups = self.group_names()
        for group in groups:
            group_items = getattr(self, group)
            if isinstance(group_items, list):
                if len(group_items) != self.COUNT:
                    msg = f"[ERR] incorrect length {self.COUNT=}/{groups=}"
                    print(msg)
                    raise Exx__WrongUsage(msg)

    def _generate_groups(self) -> None | NoReturn:
        for group in self.group_names():
            fabric: Base_GenItems | list[Any] | Any = getattr(self, group)
            if isinstance(fabric, Base_GenItems):
                setattr(self, group, fabric.generate_items(self.COUNT))
            else:
                setattr(self, group, fabric)

    def group_get__insts(self, group: str) -> Any | list[Any] | NoReturn:
        return getattr(self, group)

    def group_call__(self, meth: str, group: str | None = None, args: list | None = None, kwargs: dict | None = None) -> Union[NoReturn, TYPING__BREED_RESULT__GROUP, TYPING__BREED_RESULT__GROUPS]:
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
        if group is None:
            results = {}
            for group_name in self.group_names():
                results.update({group_name: self.group_call__(meth, group_name, args, kwargs)})
            return results

        # if group is not exists ---------------------------------------------
        if group not in self.group_names():
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
class TableItemsIndex:
    """
    GOAL
    ----
    replace/ref breederObject!
    """
    ITEMS: TableItems = TableItems()   # access for all lists!
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


# =====================================================================================================================
