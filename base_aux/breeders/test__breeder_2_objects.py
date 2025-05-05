import pytest

from base_aux.breeders.m2_breeder_objects import *


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
class Test__BreederObjectList:
    # -----------------------------------------------------------------------------------------------------------------
    def test__groups_check__generated(self):
        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.groups_check__generated() is False
        Victim.generate__objects()
        assert Victim.groups_check__generated() is True

        class Victim2(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim2.groups_check__generated() is False
        Victim2.generate__objects()
        assert Victim2.groups_check__generated() is True

    # -----------------------------------------------------------------------------------------------------------------
    def test__count(self):
        for count in range(5):
            class Victim(BreederObjectList):
                COUNT = count
                CLS_SINGLE__ITEM_SINGLE = ItemSingle
                CLS_LIST__ITEM_LIST = ItemList

            Victim.generate__objects()
            assert Victim.group_get__insts("ITEM_SINGLE") is ItemSingle.INSTS
            assert Victim.group_get__insts("ITEM_LIST") is ItemList.INSTS

            assert isinstance(Victim.group_get__insts("ITEM_SINGLE"), ItemSingle)
            assert isinstance(Victim.group_get__insts("ITEM_LIST"), list)

            if count > 0:
                assert isinstance(Victim.group_get__insts("ITEM_LIST")[0], ItemList)
                assert len(Victim.group_get__insts("ITEM_LIST")) == len(ItemList.INSTS) == Victim.COUNT == count

    # -----------------------------------------------------------------------------------------------------------------
    def test__groups__get_names(self):
        class Victim(BreederObjectList):
            pass
            # CLS_SINGLE__ITEM_SINGLE = ItemSingle
            # CLS_LIST__ITEM_LIST = ItemList

        assert Victim.groups__get_names() == list()

        class Victim(BreederObjectList):
            # CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.groups__get_names() == ["ITEM_LIST", ]

        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            # CLS_LIST__ITEM_LIST = ItemList

        assert Victim.groups__get_names() == ["ITEM_SINGLE", ]

        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert set(Victim.groups__get_names()) == {"ITEM_LIST", "ITEM_SINGLE"}

    # -----------------------------------------------------------------------------------------------------------------
    def test__groups_count__generated(self):
        class Victim(BreederObjectList):
            pass
            # CLS_SINGLE__ITEM_SINGLE = ItemSingle
            # CLS_LIST__ITEM_LIST = ItemList

        assert Victim.groups_count__generated() is None
        Victim.generate__objects()
        assert Victim.groups_count__generated() == 0

        class Victim(BreederObjectList):
            # CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.groups_count__generated() is None
        Victim.generate__objects()
        assert Victim.groups_count__generated() == 1

        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            # CLS_LIST__ITEM_LIST = ItemList

        assert Victim.groups_count__generated() is None
        Victim.generate__objects()
        assert Victim.groups_count__generated() == 1

        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.groups_count__generated() is None
        Victim.generate__objects()
        assert Victim.groups_count__generated() == 2

    # -----------------------------------------------------------------------------------------------------------------
    def test__group_get__type(self):
        class Victim(BreederObjectList):
            COUNT = 2
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_get__format("ITEM_SINGLE") is Enum_Multiplicity.SINGLE
        assert Victim.group_get__format("ITEM_LIST") is Enum_Multiplicity.MULTY
        assert Victim.group_get__format("COUNT") is Enum_Multiplicity.NOT_EXISTS
        assert Victim.group_get__format("NOT_EXISTS") is Enum_Multiplicity.NOT_EXISTS

    # -----------------------------------------------------------------------------------------------------------------
    def test__group_check__exists(self):
        class Victim(BreederObjectList):
            pass
            # CLS_SINGLE__ITEM_SINGLE = ItemSingle
            # CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_check__exists("ITEM_SINGLE") is False
        assert Victim.group_check__exists("ITEM_LIST") is False

        class Victim(BreederObjectList):
            # CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_check__exists("ITEM_SINGLE") is False
        assert Victim.group_check__exists("ITEM_LIST") is True

        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            # CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_check__exists("ITEM_SINGLE") is True
        assert Victim.group_check__exists("ITEM_LIST") is False

        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_check__exists("ITEM_SINGLE") is True
        assert Victim.group_check__exists("ITEM_LIST") is True

    # -----------------------------------------------------------------------------------------------------------------
    def test__group_get__cls(self):
        class Victim(BreederObjectList):
            pass
            # CLS_SINGLE__ITEM_SINGLE = ItemSingle
            # CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_get__cls("ITEM_SINGLE") is None
        assert Victim.group_get__cls("ITEM_LIST") is None

        class Victim(BreederObjectList):
            # CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_get__cls("ITEM_SINGLE") is None
        assert Victim.group_get__cls("ITEM_LIST") is ItemList

        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            # CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_get__cls("ITEM_SINGLE") is ItemSingle
        assert Victim.group_get__cls("ITEM_LIST") is None

        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_get__cls("ITEM_SINGLE") is ItemSingle
        assert Victim.group_get__cls("ITEM_LIST") is ItemList

    # -----------------------------------------------------------------------------------------------------------------
    def test__group_get__insts(self):
        class Victim(BreederObjectList):
            pass
            # CLS_SINGLE__ITEM_SINGLE = ItemSingle
            # CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_get__insts("ITEM_SINGLE") is None
        assert Victim.group_get__insts("ITEM_LIST") is None

        # assert isinstance(Victim.group_get__insts("ITEM_SINGLE"), ItemSingle)
        # assert isinstance(Victim.group_get__insts("ITEM_LIST"), list)
        # assert isinstance(Victim.group_get__insts("ITEM_LIST")[0], ItemList)

        class Victim(BreederObjectList):
            # CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_get__insts("ITEM_SINGLE") is None
        assert Victim.group_get__insts("ITEM_LIST") is None

        Victim.generate__objects()
        assert Victim.group_get__insts("ITEM_SINGLE") is None
        assert Victim.group_get__insts("ITEM_LIST") is ItemList.INSTS

        # assert isinstance(Victim.group_get__insts("ITEM_SINGLE"), ItemSingle)
        assert isinstance(Victim.group_get__insts("ITEM_LIST"), list)
        assert isinstance(Victim.group_get__insts("ITEM_LIST")[0], ItemList)
        assert len(Victim.group_get__insts("ITEM_LIST")) == Victim.COUNT

        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            # CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_get__insts("ITEM_SINGLE") is None
        assert Victim.group_get__insts("ITEM_LIST") is None

        Victim.generate__objects()
        assert Victim.group_get__insts("ITEM_SINGLE") is ItemSingle.INSTS
        assert Victim.group_get__insts("ITEM_LIST") is None

        assert isinstance(Victim.group_get__insts("ITEM_SINGLE"), ItemSingle)
        # assert isinstance(Victim.group_get__insts("ITEM_LIST"), list)
        # assert isinstance(Victim.group_get__insts("ITEM_LIST")[0], ItemList)
        # assert len(Victim.group_get__insts("ITEM_LIST")) == Victim.COUNT

        class Victim(BreederObjectList):
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.group_get__insts("ITEM_SINGLE") is None
        assert Victim.group_get__insts("ITEM_LIST") is None

        Victim.generate__objects()
        assert Victim.group_get__insts("ITEM_SINGLE") is ItemSingle.INSTS
        assert Victim.group_get__insts("ITEM_LIST") is ItemList.INSTS

        assert isinstance(Victim.group_get__insts("ITEM_SINGLE"), ItemSingle)
        assert isinstance(Victim.group_get__insts("ITEM_LIST"), list)
        assert isinstance(Victim.group_get__insts("ITEM_LIST")[0], ItemList)
        assert len(Victim.group_get__insts("ITEM_LIST")) == Victim.COUNT

    # -----------------------------------------------------------------------------------------------------------------
    def test__group_call(self):
        class Victim(BreederObjectList):
            COUNT = 2
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        # BLANC --------------------
        try:
            assert Victim.group_call__("set_result", "ITEM_SINGLE", [123, ])
            assert False
        except:
            assert True

        # GENERATE --------------------
        Victim.generate__objects()

        # SINGLE --------------------
        assert Victim.group_call__("set_result", "ITEM_SINGLE", [111, ]) == 111
        assert Victim(0).ITEM_SINGLE.result == 111
        assert Victim.ITEM_SINGLE.result == 111
        assert Victim(0).ITEM_LIST.result is None

        assert Victim(0).group_call__("set_result", "ITEM_SINGLE", [222, ]) == 222
        assert Victim(0).ITEM_SINGLE.result == 222
        assert Victim.ITEM_SINGLE.result == 222
        assert Victim(0).ITEM_LIST.result is None

        # LIST --------------------
        assert Victim(0).group_call__("set_result", "ITEM_LIST", [333, ]) == [333, 333, ]
        assert Victim(0).ITEM_SINGLE.result == 222
        assert Victim.ITEM_SINGLE.result == 222
        for index in range(Victim.COUNT):
            assert Victim(index).ITEM_LIST.result == Victim.LIST__ITEM_LIST[index].result == 333

        # BOTH=SINGLE+LIST --------------------
        assert Victim(0).group_call__("set_result", None, [444,]) == {
            "ITEM_SINGLE": 444,
            "ITEM_LIST": [444, 444, ],
        }
        assert Victim(0).ITEM_SINGLE.result == 444
        assert Victim.ITEM_SINGLE.result == 444
        for index in range(Victim.COUNT):
            assert Victim(index).ITEM_LIST.result == Victim.LIST__ITEM_LIST[index].result == 444

    # -----------------------------------------------------------------------------------------------------------------
    pass    # ---------------------------------------------------------------------------------------------------------
    pass    # ---------------------------------------------------------------------------------------------------------
    pass    # ---------------------------------------------------------------------------------------------------------
    pass    # ---------------------------------------------------------------------------------------------------------
    pass    # ---------------------------------------------------------------------------------------------------------
    pass    # ---------------------------------------------------------------------------------------------------------
    pass    # ---------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def test__breeder_cls__and_getattr(self):
        class Victim(BreederObjectList):
            COUNT = 2
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        try:
            assert Victim.ITEM_SINGLE
            assert False
        except:
            assert True
        try:
            assert Victim.ITEM_LIST
            assert False
        except:
            assert True
        try:
            assert Victim.LIST__ITEM_LIST
            assert False
        except:
            assert True

        Victim.generate__objects()
        assert Victim.ITEM_SINGLE
        try:
            assert Victim.ITEM_LIST
            assert False
        except:
            assert True
        assert Victim.LIST__ITEM_LIST

        assert isinstance(Victim.ITEM_SINGLE, ItemSingle)
        assert isinstance(Victim.LIST__ITEM_LIST, list)
        assert isinstance(Victim.LIST__ITEM_LIST[0], ItemList)

    # -----------------------------------------------------------------------------------------------------------------
    def test__breeder_inst__and_getattr(self):
        class Victim(BreederObjectList):
            COUNT = 3
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        Victim.generate__objects()
        assert Victim.ITEM_SINGLE is ItemSingle.INSTS is Victim(0).ITEM_SINGLE is Victim(1).ITEM_SINGLE

        for index in range(Victim.COUNT):
            assert Victim(index).ITEM_SINGLE is Victim.ITEM_SINGLE is Victim.ITEM_SINGLE.INSTS
            assert Victim(index).ITEM_LIST is Victim.LIST__ITEM_LIST[index]
            assert Victim(index).ITEM_LIST is Victim(0).LIST__ITEM_LIST[index]
            assert Victim(index).ITEM_LIST is Victim(0).ITEM_LIST.INSTS[index]

    # -----------------------------------------------------------------------------------------------------------------
    def test__breeder_inst__deep(self):
        class Victim(BreederObjectList):
            COUNT = 3
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        Victim.generate__objects()

        # SINGLE -----------------
        assert Victim is Victim(0).ITEM_SINGLE.BREEDER

        assert Victim.ITEM_SINGLE is Victim(0).ITEM_SINGLE
        assert Victim.ITEM_SINGLE is Victim.ITEM_SINGLE.BREEDER.ITEM_SINGLE
        assert Victim.ITEM_SINGLE is Victim(0).ITEM_SINGLE.BREEDER.ITEM_SINGLE
        assert Victim.ITEM_SINGLE is Victim(0).ITEM_LIST.BREEDER.ITEM_SINGLE

        # LIST -------------------
        assert not Victim(0) is Victim.ITEM_SINGLE.BREEDER(0)   # just not same UID but same instances inside!
        assert Victim(0).ITEM_SINGLE is Victim.ITEM_SINGLE.BREEDER(0).ITEM_SINGLE

        assert not Victim(0) is Victim(0).ITEM_LIST.BREEDER   # just not same UID but same instances inside!
        assert Victim(0).INDEX is Victim(0).ITEM_LIST.BREEDER.INDEX
        assert Victim(0).ITEM_SINGLE is Victim(0).ITEM_LIST.BREEDER.ITEM_SINGLE is Victim(1).ITEM_LIST.BREEDER.ITEM_SINGLE

    # -----------------------------------------------------------------------------------------------------------------
    def test__generate_objects(self):
        class Victim(BreederObjectList):
            COUNT = 2
            CLS_SINGLE__ITEM_SINGLE = ItemSingle
            CLS_LIST__ITEM_LIST = ItemList

        assert Victim.LIST__ALL_GENERATED == []

        Victim.generate__objects()
        assert len(Victim.LIST__ALL_GENERATED) == 3

        victim_single_old = Victim.ITEM_SINGLE
        victim_list0_old = Victim(0).ITEM_LIST
        assert len(Victim.LIST__ITEM_LIST) == 2

        Victim.COUNT = 3
        Victim.generate__objects()
        assert Victim.ITEM_SINGLE is victim_single_old
        assert Victim(0).ITEM_LIST is victim_list0_old
        assert len(Victim.LIST__ITEM_LIST) == 2

        Victim.COUNT = 4
        Victim.generate__objects(True)          # regen instances!
        assert not Victim.ITEM_SINGLE is victim_single_old
        assert not Victim(0).ITEM_LIST is victim_list0_old
        assert len(Victim.LIST__ITEM_LIST) == 4


# =====================================================================================================================
