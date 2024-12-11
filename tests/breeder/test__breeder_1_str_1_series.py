from base_aux.base_exceptions import *
from base_aux.breeders import *


# =====================================================================================================================
class Test__BreederStrSeries:
    @classmethod
    def setup_class(cls):
        cls.Victim = BreederStrSeries

    # # @classmethod
    # # def teardown_class(cls):
    # #     pass
    # #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__START_OUTER_None(self):
        victim = self.Victim(None, 1, "test_%s", 1)
        assert victim.START_OUTER == None
        assert victim.COUNT == 1
        assert victim.TEMPLATE == "test_%s"
        assert victim.START_INNER == 1

        try:
            assert victim.get_dict__inner()
            assert False
        except Exx__StartOuterNONE_UsedInStackByRecreation:
            assert True

        try:
            assert victim.get_dict__outer()
            assert False
        except Exx__StartOuterNONE_UsedInStackByRecreation:
            assert True

    def test__init_params(self):
        victim = self.Victim(0, 1, "test_%s", 1)
        assert victim.START_OUTER == 0
        assert victim.COUNT == 1
        assert victim.TEMPLATE == "test_%s"
        assert victim.START_INNER == 1

        assert victim.get_dict__inner() == {1: "test_1"}
        assert victim.get_dict__outer() == {0: "test_1"}

        victim = self.Victim(1, 1, "test_%s", 1)
        assert victim.START_OUTER == 1
        assert victim.COUNT == 1
        assert victim.TEMPLATE == "test_%s"
        assert victim.START_INNER == 1

        victim = self.Victim(1, 2, "test_%s", 1)
        assert victim.START_OUTER == 1
        assert victim.COUNT == 2
        assert victim.TEMPLATE == "test_%s"
        assert victim.START_INNER == 1

    def test__dicts(self):
        victim = self.Victim(0, 1, "test_%s", 0)
        assert victim.get_dict__inner() == {0: "test_0"}
        assert victim.get_dict__outer() == {0: "test_0"}

        victim = self.Victim(0, 1, "test_%s", 1)
        assert victim.get_dict__inner() == {1: "test_1"}
        assert victim.get_dict__outer() == {0: "test_1"}

        victim = self.Victim(0, 2, "test_%s", 1)
        assert victim.get_dict__inner() == {1: "test_1", 2: "test_2"}
        assert victim.get_dict__outer() == {0: "test_1", 1: "test_2"}

    def test__contains(self):
        # --------------------------------------------------
        victim = self.Victim(0, 1, "test_%s", 1)

        # indexes
        assert 0 in victim
        assert 1 not in victim
        assert 2 not in victim

        # values
        assert "test_0" not in victim
        assert "test_1" in victim
        assert "test_2" not in victim

        # --------------------------------------------------
        victim = self.Victim(0, 2, "test_%s", 1)

        # indexes
        assert 0 in victim
        assert 1 in victim
        assert 2 not in victim

        # values
        assert "test_0" not in victim
        assert "test_1" in victim
        assert "test_2" in victim

        # --------------------------------------------------
        victim = self.Victim(1, 2, "test_%s", 0)

        # indexes
        assert 0 not in victim
        assert 1 in victim
        assert 2 in victim

        # values
        assert "test_0" in victim
        assert "test_1" in victim
        assert "test_2" not in victim

    def test__getitem(self):
        # --------------------------------------------------
        victim = self.Victim(0, 1, "test_%s", 0)
        # indexes
        assert victim[0] == "test_0"
        try:
            result = victim[1]
            assert False
        except:
            assert True

        # values
        assert victim["test_0"] == 0
        try:
            result = victim["test_1"]
            assert False
        except:
            assert True

        # --------------------------------------------------
        victim = self.Victim(0, 1, "test_%s", 1)
        # indexes
        try:
            result = victim[0]
            assert False
        except:
            assert True
        assert victim[1] == "test_1"


        # values
        try:
            result = victim["test_0"]
            assert False
        except:
            assert True
        assert victim["test_1"] == 1

    def test__listed_index__by_outer(self):
        # --------------------------------------------------
        victim = self.Victim(0, 2, "test_%s", 0)
        assert victim.get_dict__inner() == {0: "test_0", 1: "test_1"}
        assert victim.get_dict__outer() == {0: "test_0", 1: "test_1"}

        assert list(victim.get_dict__outer()) == [0, 1]
        assert list(victim.get_dict__inner()) == [0, 1]

        assert victim.get_listed_index__by_outer(0) == 0
        assert victim.get_listed_index__by_outer(1) == 1
        try:
            assert victim.get_listed_index__by_outer(2)
            assert False
        except:
            assert True

        # --------------------------------------------------
        victim = self.Victim(0, 2, "test_%s", 1)
        assert victim.get_dict__inner() == {1: "test_1", 2: "test_2"}
        assert victim.get_dict__outer() == {0: "test_1", 1: "test_2"}

        assert list(victim.get_dict__outer()) == [0, 1]
        assert list(victim.get_dict__inner()) == [1, 2]

        assert victim.get_listed_index__by_outer(0) == 0
        assert victim.get_listed_index__by_outer(1) == 1
        try:
            assert victim.get_listed_index__by_outer(2)
            assert False
        except:
            assert True

    def test__listed_index__by_value(self):
        # --------------------------------------------------
        victim = self.Victim(0, 2, "test_%s", 0)
        assert victim.get_dict__inner() == {0: "test_0", 1: "test_1"}
        assert victim.get_dict__outer() == {0: "test_0", 1: "test_1"}

        assert victim.get_listed_index__by_value("test_0") == 0
        assert victim.get_listed_index__by_value("test_1") == 1
        try:
            assert victim.get_listed_index__by_value("test_2")
            assert False
        except:
            assert True

        # --------------------------------------------------
        victim = self.Victim(0, 2, "test_%s", 1)
        assert victim.get_dict__inner() == {1: "test_1", 2: "test_2"}
        assert victim.get_dict__outer() == {0: "test_1", 1: "test_2"}

        try:
            assert victim.get_listed_index__by_value("test_0")
            assert False
        except:
            assert True
        assert victim.get_listed_index__by_value("test_1") == 0
        assert victim.get_listed_index__by_value("test_2") == 1


# =====================================================================================================================
