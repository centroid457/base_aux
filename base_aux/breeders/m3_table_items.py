from typing import *
from enum import Enum, auto

from base_aux.base_statics.m2_exceptions import *
from base_aux.aux_attr.m1_annot_attr1_aux import *

from base_aux.base_nest_dunders.m3_calls import *
from base_aux.base_nest_dunders.m1_init1_source import *


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
        if self.MULTYPLICITY == Enum_Multiplicity.SINGLE:
            if self.CALLABILITY == Enum_StaticCallable.CALLABLE:
                return self.SOURCE()
            else:
                return self.SOURCE
        elif self.MULTYPLICITY == Enum_Multiplicity.MULTY:
            result = []
            for index in range(count):
                if self.CALLABILITY == Enum_StaticCallable.CALLABLE:
                    item = self.SOURCE(index)
                else:
                    item = self.SOURCE

                result.append(item)
            return result


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
        return item in list(self._iter_group_names())

    def _iter_group_names(self) -> Iterable[str]:
        for name in AnnotsAllAux(self).iter__names_not_hidden():
            if name != "COUNT":
                yield name

    def _check_length(self) -> None | NoReturn:
        groups = list(self._iter_group_names())
        for group in groups:
            group_items = getattr(self, group)
            if isinstance(group_items, list):
                if len(group_items) != self.COUNT:
                    msg = f"[ERR] incorrect length {self.COUNT=}/{groups=}"
                    print(msg)
                    raise Exx__WrongUsage(msg)

    def _generate_groups(self) -> None | NoReturn:
        for group in self._iter_group_names():
            fabric: Base_GenItems | list[Any] | Any = getattr(self.__class__, group)
            if isinstance(fabric, Base_GenItems):
                setattr(self, group, fabric.generate_items(self.COUNT))
            else:
                setattr(self, group, fabric)


# =====================================================================================================================
class TableItemsIndex:
    """
    GOAL
    ----
    replace/ref breederObject!
    """
    ITEMS: TableItems = TableItems(3)   # access for all lists!
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
def test__example():
    class Example__TableItems(TableItems):
        COUNT = 2
        ATC1 = "atc1"
        ATC2 = GenItems_SingleCallable(lambda: "atc2")

        PTB1 = ["ptb0", "ptb1"]
        PTB2 = GenItems_MultyCallable(lambda index: f"ptb{index}")


    class Example__TableItemsIndex(TableItemsIndex):
        ITEMS = Example__TableItems()


    assert Example__TableItemsIndex(0).ATC1 == Example__TableItems.ATC1
    assert Example__TableItemsIndex(0).ATC1 == Example__TableItemsIndex(0).ITEMS.ATC1
    assert Example__TableItemsIndex(1).ATC1 == Example__TableItems.ATC1
    assert Example__TableItemsIndex(1).ATC1 == Example__TableItemsIndex(1).ITEMS.ATC1


# =====================================================================================================================
