import pytest

from base_aux.breeders.m2_breeder_objects___DEPRECATE import *
from base_aux.breeders.m3_table_items import *


# =====================================================================================================================
class ItemSingle:
    result: Any

    def __init__(self):
        self.result = None
        pass

    def set_result(self, result: Any = None) -> Any:
        self.result = result
        return self.result


class ItemList(ItemSingle):
    def __init__(self, index: int):
        super().__init__()
        self.INDEX = index


# =====================================================================================================================
class Test_Single:
    def setup_method(self, method):
        class VictimItems(TableItems):
            COUNT = 2

            ATC_STATIC: Any = "ATC_STATIC"
            ATC_FUNC: Any = GenItems_SingleCallable(lambda: "ATC_FUNC")
            ATC_CLS: Any = GenItems_SingleCallable(ItemSingle)

        class VictimIndex(TableItemsIndex):
            ITEMS = VictimItems()

        self.VictimItems = VictimItems
        self.VictimIndex = VictimIndex

    def test__0(self):
        victim = self.VictimItems()
        assert victim.group_names() == ["ATC_STATIC", "ATC_FUNC", "ATC_CLS"]
        assert "ATC_STATIC" in victim
        assert victim._check_length() is None

    def test__1_types(self):
        victim = self.VictimItems()
        assert victim.ATC_STATIC == "ATC_STATIC"
        assert victim.ATC_FUNC == "ATC_FUNC"
        assert isinstance(victim.ATC_CLS, ItemSingle)

    def test__2_values(self):
        assert self.VictimItems.ATC_STATIC == self.VictimIndex.ITEMS.ATC_STATIC

        for index in range(self.VictimItems.COUNT):
            assert self.VictimIndex(index).ATC_STATIC == self.VictimItems.ATC_STATIC

            assert isinstance(self.VictimIndex(index).ATC_STATIC, str)
            assert self.VictimIndex(index).ATC_STATIC == self.VictimIndex(index).ITEMS.ATC_STATIC

            assert isinstance(self.VictimIndex(index).ATC_FUNC, str)
            assert self.VictimIndex(index).ATC_FUNC == self.VictimIndex(index).ITEMS.ATC_FUNC

            assert isinstance(self.VictimIndex(index).ATC_CLS, ItemSingle)
            assert self.VictimIndex(index).ATC_CLS == self.VictimIndex(index).ITEMS.ATC_CLS


# =====================================================================================================================
class Test_Multy:
    def setup_method(self, method):
        class VictimItems(TableItems):
            COUNT = 2

            PTB_LIST: Any = ["ptb0", "ptb1"]
            PTB_FUNC: Any = GenItems_MultyCallable(lambda index: f"ptb{index}")
            PTB_CLS: Any = GenItems_MultyCallable(ItemList)

        class VictimIndex(TableItemsIndex):
            ITEMS = VictimItems()

        self.VictimItems = VictimItems
        self.VictimIndex = VictimIndex

    def test__0(self):
        victim = self.VictimItems()
        assert victim.group_names() == ["PTB_LIST", "PTB_FUNC", "PTB_CLS"]
        assert "PTB_LIST" in victim
        assert victim._check_length() is None

    def test__1_types(self):
        victim = self.VictimItems()
        assert victim.PTB_LIST == ["ptb0", "ptb1"]
        assert victim.PTB_FUNC == ["ptb0", "ptb1"]
        assert isinstance(victim.PTB_CLS, list)
        assert isinstance(victim.PTB_CLS[0], ItemList)

    def test__2_values(self):
        for index in range(self.VictimItems.COUNT):
            assert self.VictimIndex(index).ITEMS.PTB_LIST == self.VictimIndex.ITEMS.PTB_LIST == ["ptb0", "ptb1"]
            assert self.VictimIndex(index).PTB_LIST == self.VictimIndex.ITEMS.PTB_LIST[index] == f"ptb{index}"

            assert self.VictimIndex(index).ITEMS.PTB_FUNC == self.VictimIndex.ITEMS.PTB_FUNC == ["ptb0", "ptb1"]
            assert self.VictimIndex(index).ITEMS.PTB_FUNC == self.VictimIndex(0).ITEMS.PTB_FUNC
            assert isinstance(self.VictimIndex(index).PTB_FUNC, str)
            assert self.VictimIndex(index).PTB_FUNC == self.VictimIndex(0).ITEMS.PTB_FUNC[index] == f"ptb{index}"

            assert self.VictimIndex(index).ITEMS.PTB_CLS == self.VictimIndex.ITEMS.PTB_CLS
            assert self.VictimIndex(index).ITEMS.PTB_CLS == self.VictimIndex(0).ITEMS.PTB_CLS
            assert isinstance(self.VictimIndex(index).PTB_CLS, ItemList)
            assert self.VictimIndex(index).PTB_CLS == self.VictimIndex(0).ITEMS.PTB_CLS[index]




#
#
#
# # =====================================================================================================================
# class Test__TableItems:
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__count(self):
#         for count in range(5):
#             class Victim(BreederObj):
#                 COUNT = count
#                 CLS_SINGLE__ITEM_SINGLE = ItemSingle
#                 CLS_LIST__ITEM_LIST = ItemList
#
#             Victim.generate__objects()
#             assert Victim.group_get__insts("ITEM_SINGLE") is ItemSingle.INSTS
#             assert Victim.group_get__insts("ITEM_LIST") is ItemList.INSTS
#
#             assert isinstance(Victim.group_get__insts("ITEM_SINGLE"), ItemSingle)
#             assert isinstance(Victim.group_get__insts("ITEM_LIST"), list)
#
#             if count > 0:
#                 assert isinstance(Victim.group_get__insts("ITEM_LIST")[0], ItemList)
#                 assert len(Victim.group_get__insts("ITEM_LIST")) == len(ItemList.INSTS) == Victim.COUNT == count
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__groups__get_names(self):
#         class Victim(BreederObj):
#             pass
#             # CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             # CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.groups__get_names() == list()
#
#         class Victim(BreederObj):
#             # CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.groups__get_names() == ["ITEM_LIST", ]
#
#         class Victim(BreederObj):
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             # CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.groups__get_names() == ["ITEM_SINGLE", ]
#
#         class Victim(BreederObj):
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert set(Victim.groups__get_names()) == {"ITEM_LIST", "ITEM_SINGLE"}
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__groups_count__generated(self):
#         class Victim(BreederObj):
#             pass
#             # CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             # CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.groups_count__generated() is None
#         Victim.generate__objects()
#         assert Victim.groups_count__generated() == 0
#
#         class Victim(BreederObj):
#             # CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.groups_count__generated() is None
#         Victim.generate__objects()
#         assert Victim.groups_count__generated() == 1
#
#         class Victim(BreederObj):
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             # CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.groups_count__generated() is None
#         Victim.generate__objects()
#         assert Victim.groups_count__generated() == 1
#
#         class Victim(BreederObj):
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.groups_count__generated() is None
#         Victim.generate__objects()
#         assert Victim.groups_count__generated() == 2
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__group_get__type(self):
#         class Victim(BreederObj):
#             COUNT = 2
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_get__format("ITEM_SINGLE") is Enum_SingleMultiple.SINGLE
#         assert Victim.group_get__format("ITEM_LIST") is Enum_SingleMultiple.MULTIPLE
#         assert Victim.group_get__format("COUNT") is Enum_SingleMultiple.NOT_EXISTS
#         assert Victim.group_get__format("NOT_EXISTS") is Enum_SingleMultiple.NOT_EXISTS
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__group_check__exists(self):
#         class Victim(BreederObj):
#             pass
#             # CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             # CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_check__exists("ITEM_SINGLE") is False
#         assert Victim.group_check__exists("ITEM_LIST") is False
#
#         class Victim(BreederObj):
#             # CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_check__exists("ITEM_SINGLE") is False
#         assert Victim.group_check__exists("ITEM_LIST") is True
#
#         class Victim(BreederObj):
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             # CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_check__exists("ITEM_SINGLE") is True
#         assert Victim.group_check__exists("ITEM_LIST") is False
#
#         class Victim(BreederObj):
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_check__exists("ITEM_SINGLE") is True
#         assert Victim.group_check__exists("ITEM_LIST") is True
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__group_get__cls(self):
#         class Victim(BreederObj):
#             pass
#             # CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             # CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_get__cls("ITEM_SINGLE") is None
#         assert Victim.group_get__cls("ITEM_LIST") is None
#
#         class Victim(BreederObj):
#             # CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_get__cls("ITEM_SINGLE") is None
#         assert Victim.group_get__cls("ITEM_LIST") is ItemList
#
#         class Victim(BreederObj):
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             # CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_get__cls("ITEM_SINGLE") is ItemSingle
#         assert Victim.group_get__cls("ITEM_LIST") is None
#
#         class Victim(BreederObj):
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_get__cls("ITEM_SINGLE") is ItemSingle
#         assert Victim.group_get__cls("ITEM_LIST") is ItemList
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__group_get__insts(self):
#         class Victim(BreederObj):
#             pass
#             # CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             # CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_get__insts("ITEM_SINGLE") is None
#         assert Victim.group_get__insts("ITEM_LIST") is None
#
#         # assert isinstance(Victim.group_get__insts("ITEM_SINGLE"), ItemSingle)
#         # assert isinstance(Victim.group_get__insts("ITEM_LIST"), list)
#         # assert isinstance(Victim.group_get__insts("ITEM_LIST")[0], ItemList)
#
#         class Victim(BreederObj):
#             # CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_get__insts("ITEM_SINGLE") is None
#         assert Victim.group_get__insts("ITEM_LIST") is None
#
#         Victim.generate__objects()
#         assert Victim.group_get__insts("ITEM_SINGLE") is None
#         assert Victim.group_get__insts("ITEM_LIST") is ItemList.INSTS
#
#         # assert isinstance(Victim.group_get__insts("ITEM_SINGLE"), ItemSingle)
#         assert isinstance(Victim.group_get__insts("ITEM_LIST"), list)
#         assert isinstance(Victim.group_get__insts("ITEM_LIST")[0], ItemList)
#         assert len(Victim.group_get__insts("ITEM_LIST")) == Victim.COUNT
#
#         class Victim(BreederObj):
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             # CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_get__insts("ITEM_SINGLE") is None
#         assert Victim.group_get__insts("ITEM_LIST") is None
#
#         Victim.generate__objects()
#         assert Victim.group_get__insts("ITEM_SINGLE") is ItemSingle.INSTS
#         assert Victim.group_get__insts("ITEM_LIST") is None
#
#         assert isinstance(Victim.group_get__insts("ITEM_SINGLE"), ItemSingle)
#         # assert isinstance(Victim.group_get__insts("ITEM_LIST"), list)
#         # assert isinstance(Victim.group_get__insts("ITEM_LIST")[0], ItemList)
#         # assert len(Victim.group_get__insts("ITEM_LIST")) == Victim.COUNT
#
#         class Victim(BreederObj):
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.group_get__insts("ITEM_SINGLE") is None
#         assert Victim.group_get__insts("ITEM_LIST") is None
#
#         Victim.generate__objects()
#         assert Victim.group_get__insts("ITEM_SINGLE") is ItemSingle.INSTS
#         assert Victim.group_get__insts("ITEM_LIST") is ItemList.INSTS
#
#         assert isinstance(Victim.group_get__insts("ITEM_SINGLE"), ItemSingle)
#         assert isinstance(Victim.group_get__insts("ITEM_LIST"), list)
#         assert isinstance(Victim.group_get__insts("ITEM_LIST")[0], ItemList)
#         assert len(Victim.group_get__insts("ITEM_LIST")) == Victim.COUNT
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__group_call(self):
#         class Victim(BreederObj):
#             COUNT = 2
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         # BLANC --------------------
#         try:
#             assert Victim.group_call__("set_result", "ITEM_SINGLE", [123, ])
#             assert False
#         except:
#             assert True
#
#         # GENERATE --------------------
#         Victim.generate__objects()
#
#         # SINGLE --------------------
#         assert Victim.group_call__("set_result", "ITEM_SINGLE", [111, ]) == 111
#         assert Victim(0).ITEM_SINGLE.result == 111
#         assert Victim.ITEM_SINGLE.result == 111
#         assert Victim(0).ITEM_LIST.result is None
#
#         assert Victim(0).group_call__("set_result", "ITEM_SINGLE", [222, ]) == 222
#         assert Victim(0).ITEM_SINGLE.result == 222
#         assert Victim.ITEM_SINGLE.result == 222
#         assert Victim(0).ITEM_LIST.result is None
#
#         # LIST --------------------
#         assert Victim(0).group_call__("set_result", "ITEM_LIST", [333, ]) == [333, 333, ]
#         assert Victim(0).ITEM_SINGLE.result == 222
#         assert Victim.ITEM_SINGLE.result == 222
#         for index in range(Victim.COUNT):
#             assert Victim(index).ITEM_LIST.result == Victim.LIST__ITEM_LIST[index].result == 333
#
#         # BOTH=SINGLE+LIST --------------------
#         assert Victim(0).group_call__("set_result", None, [444,]) == {
#             "ITEM_SINGLE": 444,
#             "ITEM_LIST": [444, 444, ],
#         }
#         assert Victim(0).ITEM_SINGLE.result == 444
#         assert Victim.ITEM_SINGLE.result == 444
#         for index in range(Victim.COUNT):
#             assert Victim(index).ITEM_LIST.result == Victim.LIST__ITEM_LIST[index].result == 444
#
#     # -----------------------------------------------------------------------------------------------------------------
#     pass    # ---------------------------------------------------------------------------------------------------------
#     pass    # ---------------------------------------------------------------------------------------------------------
#     pass    # ---------------------------------------------------------------------------------------------------------
#     pass    # ---------------------------------------------------------------------------------------------------------
#     pass    # ---------------------------------------------------------------------------------------------------------
#     pass    # ---------------------------------------------------------------------------------------------------------
#     pass    # ---------------------------------------------------------------------------------------------------------
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__breeder_cls__and_getattr(self):
#         class Victim(BreederObj):
#             COUNT = 2
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         try:
#             assert Victim.ITEM_SINGLE
#             assert False
#         except:
#             assert True
#         try:
#             assert Victim.ITEM_LIST
#             assert False
#         except:
#             assert True
#         try:
#             assert Victim.LIST__ITEM_LIST
#             assert False
#         except:
#             assert True
#
#         Victim.generate__objects()
#         assert Victim.ITEM_SINGLE
#         try:
#             assert Victim.ITEM_LIST
#             assert False
#         except:
#             assert True
#         assert Victim.LIST__ITEM_LIST
#
#         assert isinstance(Victim.ITEM_SINGLE, ItemSingle)
#         assert isinstance(Victim.LIST__ITEM_LIST, list)
#         assert isinstance(Victim.LIST__ITEM_LIST[0], ItemList)
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__breeder_inst__and_getattr(self):
#         class Victim(BreederObj):
#             COUNT = 3
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         Victim.generate__objects()
#         assert Victim.ITEM_SINGLE is ItemSingle.INSTS is Victim(0).ITEM_SINGLE is Victim(1).ITEM_SINGLE
#
#         for index in range(Victim.COUNT):
#             assert Victim(index).ITEM_SINGLE is Victim.ITEM_SINGLE is Victim.ITEM_SINGLE.INSTS
#             assert Victim(index).ITEM_LIST is Victim.LIST__ITEM_LIST[index]
#             assert Victim(index).ITEM_LIST is Victim(0).LIST__ITEM_LIST[index]
#             assert Victim(index).ITEM_LIST is Victim(0).ITEM_LIST.INSTS[index]
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__breeder_inst__deep(self):
#         class Victim(BreederObj):
#             COUNT = 3
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         Victim.generate__objects()
#
#         # SINGLE -----------------
#         assert Victim is Victim(0).ITEM_SINGLE.BREEDER
#
#         assert Victim.ITEM_SINGLE is Victim(0).ITEM_SINGLE
#         assert Victim.ITEM_SINGLE is Victim.ITEM_SINGLE.BREEDER.ITEM_SINGLE
#         assert Victim.ITEM_SINGLE is Victim(0).ITEM_SINGLE.BREEDER.ITEM_SINGLE
#         assert Victim.ITEM_SINGLE is Victim(0).ITEM_LIST.BREEDER.ITEM_SINGLE
#
#         # LIST -------------------
#         assert not Victim(0) is Victim.ITEM_SINGLE.BREEDER(0)   # just not same UID but same instances inside!
#         assert Victim(0).ITEM_SINGLE is Victim.ITEM_SINGLE.BREEDER(0).ITEM_SINGLE
#
#         assert not Victim(0) is Victim(0).ITEM_LIST.BREEDER   # just not same UID but same instances inside!
#         assert Victim(0).INDEX is Victim(0).ITEM_LIST.BREEDER.INDEX
#         assert Victim(0).ITEM_SINGLE is Victim(0).ITEM_LIST.BREEDER.ITEM_SINGLE is Victim(1).ITEM_LIST.BREEDER.ITEM_SINGLE
#
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__generate_objects(self):
#         class Victim(BreederObj):
#             COUNT = 2
#             CLS_SINGLE__ITEM_SINGLE = ItemSingle
#             CLS_LIST__ITEM_LIST = ItemList
#
#         assert Victim.LIST__ALL_GENERATED == []
#
#         Victim.generate__objects()
#         assert len(Victim.LIST__ALL_GENERATED) == 3
#
#         victim_single_old = Victim.ITEM_SINGLE
#         victim_list0_old = Victim(0).ITEM_LIST
#         assert len(Victim.LIST__ITEM_LIST) == 2
#
#         Victim.COUNT = 3
#         Victim.generate__objects()
#         assert Victim.ITEM_SINGLE is victim_single_old
#         assert Victim(0).ITEM_LIST is victim_list0_old
#         assert len(Victim.LIST__ITEM_LIST) == 2
#
#         Victim.COUNT = 4
#         Victim.generate__objects(True)          # regen instances!
#         assert not Victim.ITEM_SINGLE is victim_single_old
#         assert not Victim(0).ITEM_LIST is victim_list0_old
#         assert len(Victim.LIST__ITEM_LIST) == 4
#
#
# # =====================================================================================================================
